# Missables Tracker (Decky)

A Steam Deck [Decky Loader](https://github.com/SteamDeckHomebrew/decky-loader) plugin for tracking missable and optional content.

Pick a bundled game, expand location/session sections as you play, mark items done, and expand details for rich text (and images when present). The sidebar layout stays within the Decky panel width — no horizontal scrolling.

## Included games

| Game | Source |
| --- | --- |
| Final Fantasy VII | [FFVII - Missable & Optional Content](https://steamcommunity.com/sharedfiles/filedetails/?id=2836675266) by Abyss |
| Final Fantasy IX | [FFIX - Missable & Optional Content](https://steamcommunity.com/sharedfiles/filedetails/?id=2988011418) by Abyss |
| Final Fantasy X / X-2 HD Remaster | [FFX - Missable & Optional Content](https://steamcommunity.com/sharedfiles/filedetails/?id=3044396628) by Abyss |

Guide text is bundled offline for use on Deck. All credit belongs to the original author.

## Features

- Game picker (extensible — add more JSON packs under `src/data/games/`)
- Collapsible sessions with per-session progress (`done/total`)
- Toggle checkmarks for each missable / optional item
- Expandable rich text details (bold, spoilers, wrapped text)
- Image support via `images[]` on items (`max-width: 100%`)
- Progress saved on-device through the plugin Python backend

## Develop

Requirements: Node.js 16.14+, [pnpm](https://pnpm.io/) v9.

```bash
pnpm install
pnpm run build
```

Rebuild guide data from the scraped Steam guide markdown:

```bash
pnpm run parse:all
# or individually:
pnpm run parse:ffvii
pnpm run parse:ffix
pnpm run parse:ffx
```

## Package for Steam Deck

```bash
pnpm run package
```

That runs `pnpm install`, `pnpm run build`, zips the Decky install files, and prints the zip path (under `out/`).

Then copy the zip to your Deck and install via Decky → Developer → **Install Plugin from ZIP**, or extract it into `~/homebrew/plugins/missables-tracker`.

## Adding another game

1. Create `src/data/games/<game-id>.json` using the same schema as `final-fantasy-ix.json`
2. Register it in `src/data/games/index.ts`
3. Rebuild

### Schema sketch

```json
{
  "id": "my-game",
  "title": "My Game",
  "shortTitle": "MG",
  "source": { "title": "...", "author": "...", "url": "..." },
  "sessions": [
    {
      "id": "town",
      "title": "Town",
      "warning": "One-time area",
      "itemCount": 1,
      "blocks": [
        { "type": "heading", "text": "Exploration" },
        {
          "type": "item",
          "id": "town-001",
          "title": "Key Item",
          "optional": false,
          "richText": [{ "type": "text", "text": "Found behind the inn." }],
          "images": ["https://example.com/shot.jpg"]
        }
      ]
    }
  ]
}
```
