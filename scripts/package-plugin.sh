#!/usr/bin/env bash
# Build Missables Tracker and create a Decky-installable zip.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! command -v pnpm >/dev/null 2>&1; then
  echo "error: pnpm is not installed or not on PATH" >&2
  exit 1
fi

if ! command -v zip >/dev/null 2>&1; then
  echo "error: zip is not installed or not on PATH" >&2
  exit 1
fi

PLUGIN_NAME="$(node -p "require('./package.json').name")"
VERSION="$(node -p "require('./package.json').version")"
OUT_DIR="$ROOT/out"
STAGE_DIR="$OUT_DIR/stage/$PLUGIN_NAME"
ZIP_PATH="$OUT_DIR/${PLUGIN_NAME}-v${VERSION}.zip"

echo "==> Installing dependencies"
pnpm install

echo "==> Building frontend"
pnpm run build

if [[ ! -f "$ROOT/dist/index.js" ]]; then
  echo "error: dist/index.js was not created" >&2
  exit 1
fi

echo "==> Staging plugin files"
rm -rf "$OUT_DIR/stage"
mkdir -p "$STAGE_DIR/dist"

copy_if_exists() {
  local src="$1"
  local dest="$2"
  if [[ -e "$src" ]]; then
    cp -R "$src" "$dest"
  fi
}

cp "$ROOT/plugin.json" "$STAGE_DIR/"
cp "$ROOT/package.json" "$STAGE_DIR/"
cp "$ROOT/main.py" "$STAGE_DIR/"
cp "$ROOT/dist/index.js" "$STAGE_DIR/dist/"

copy_if_exists "$ROOT/LICENSE" "$STAGE_DIR/"
copy_if_exists "$ROOT/README.md" "$STAGE_DIR/"
copy_if_exists "$ROOT/assets" "$STAGE_DIR/"
copy_if_exists "$ROOT/defaults" "$STAGE_DIR/"
copy_if_exists "$ROOT/py_modules" "$STAGE_DIR/"

# Optional compiled backend binaries (not used by this plugin today)
if [[ -d "$ROOT/backend/out" ]]; then
  mkdir -p "$STAGE_DIR/bin"
  cp -R "$ROOT/backend/out/." "$STAGE_DIR/bin/"
fi

echo "==> Creating zip"
rm -f "$ZIP_PATH"
(
  cd "$OUT_DIR/stage"
  zip -r "$ZIP_PATH" "$PLUGIN_NAME" >/dev/null
)

# Keep the zip; drop the staging tree to avoid clutter
rm -rf "$OUT_DIR/stage"

if command -v pbcopy >/dev/null 2>&1; then
  printf '%s' "$ZIP_PATH" | pbcopy
  echo "Copied to clipboard: $ZIP_PATH"
elif command -v xclip >/dev/null 2>&1; then
  printf '%s' "$ZIP_PATH" | xclip -selection clipboard
  echo "Copied to clipboard: $ZIP_PATH"
elif command -v wl-copy >/dev/null 2>&1; then
  printf '%s' "$ZIP_PATH" | wl-copy
  echo "Copied to clipboard: $ZIP_PATH"
else
  echo "$ZIP_PATH"
fi
