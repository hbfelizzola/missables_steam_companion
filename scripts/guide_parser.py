#!/usr/bin/env python3
"""Shared Steam-guide markdown → missables JSON parser."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable


@dataclass
class GuideConfig:
    source: Path
    output: Path
    sessions: list[str]
    game_id: str
    title: str
    short_title: str
    steam_app_id: int
    source_title: str
    source_author: str
    source_url: str
    start_marker: str = "\n Introduction \n"
    duplicate_renames: dict[tuple[str, int], str] = field(default_factory=dict)
    drop_titles: set[str] = field(
        default_factory=lambda: {"Thank You", "Thank you", "Comments"}
    )
    heading_extras: set[str] = field(default_factory=set)
    optional_prefixes: tuple[str, ...] = ("+", "⚠")
    comments_markers: tuple[str, ...] = (
        "\n54 Comments",
        "\n Comments \n",
        "\nComments\n",
    )


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "item"


def clean_inline(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text).strip()
    text = (
        text.replace("♥♥♥♥♥♥♥", "***")
        .replace("♥♥♥♥♥♥", "***")
        .replace("♥♥♥♥", "****")
        .replace("⚠", "⚠")
    )
    return text


def parse_rich_text(text: str) -> list[dict]:
    text = clean_inline(text)
    if not text:
        return []

    blocks: list[dict] = []
    spoiler_pat = re.compile(r"\[spoilers\](.*?)\[/spoilers\]", re.I | re.S)
    parts = spoiler_pat.split(text)
    for i, part in enumerate(parts):
        if not part:
            continue
        if i % 2 == 1:
            blocks.append({"type": "spoiler", "text": clean_inline(part)})
            continue
        bold_pat = re.compile(r"\*\*(.+?)\*\*")
        cursor = 0
        for m in bold_pat.finditer(part):
            before = part[cursor : m.start()]
            if before.strip():
                blocks.append({"type": "text", "text": clean_inline(before)})
            blocks.append({"type": "bold", "text": clean_inline(m.group(1))})
            cursor = m.end()
        after = part[cursor:]
        if after.strip():
            blocks.append({"type": "text", "text": clean_inline(after)})
    return blocks or [{"type": "text", "text": text}]


def extract_title_from_bullet(text: str) -> tuple[str, str]:
    text = clean_inline(text)
    # Strip leading warning marker for title extraction
    bare = re.sub(r"^⚠\s*", "", text)
    m = re.match(r"^(\+?[A-Za-z0-9][^:]{0,80}?):\s*(.*)$", bare)
    if m and len(m.group(1)) < 80:
        return m.group(1).strip(), m.group(2).strip()
    m = re.match(r"^(\*?M?\d+[A-Z]?)\s*[-–—]\s*(.+)$", bare)
    if m:
        rest = m.group(2).strip()
        title_part = rest.split(".")[0].strip()
        return f"ATE {m.group(1).lstrip('*')} - {title_part}", text
    if len(bare) <= 70:
        return bare, ""
    return bare[:67].rstrip() + "…", text


def find_session_spans(content: str, cfg: GuideConfig) -> list[tuple[str, int, int]]:
    idx = content.find(cfg.start_marker)
    if idx < 0:
        # Try without leading newline padding variants
        alt = cfg.start_marker.strip()
        m = re.search(rf"\n\s*{re.escape(alt)}\s*\n", content)
        if not m:
            raise SystemExit(
                f"Could not find start marker {cfg.start_marker!r} in {cfg.source}"
            )
        idx = m.start()

    body = content[idx:]
    body_offset = idx
    occurrences: dict[str, int] = {t: 0 for t in cfg.sessions}

    titles_sorted = sorted(cfg.sessions, key=len, reverse=True)
    heading_re = re.compile(
        r"\n (" + "|".join(re.escape(t) for t in titles_sorted) + r") \n",
    )

    abs_matches: list[tuple[str, int, int]] = []
    for m in heading_re.finditer(body):
        title = m.group(1)
        occurrences[title] = occurrences.get(title, 0) + 1
        occ = occurrences[title]
        display = cfg.duplicate_renames.get((title, occ), title)
        abs_matches.append((display, body_offset + m.start(1), body_offset + m.end(1)))

    spans: list[tuple[str, int, int]] = []
    for i, (title, _start, end) in enumerate(abs_matches):
        content_start = end
        while content_start < len(content) and content[content_start] in " \t\r":
            content_start += 1
        if content_start < len(content) and content[content_start] == "\n":
            content_start += 1
        content_end = (
            abs_matches[i + 1][1] if i + 1 < len(abs_matches) else len(content)
        )
        for marker in cfg.comments_markers:
            stop = content.find(marker, content_start)
            if stop != -1 and stop < content_end:
                content_end = stop
        spans.append((title, content_start, content_end))
    return spans


DEFAULT_HEADINGS = {
    "ATE",
    "Exploration",
    "Optional Content",
    "Self esteem booster",
    "Save Slots",
    "Missables",
    "Cheats",
    "Sphere Grid",
    "Cloister of Trials",
    "Gold Saucer Date",
    "Materia Overlord",
    "Achievements",
    "Ultimate Weapons",
    "Limit Breaks",
    "Chocobo Racing",
    "Celestial Weapons",
    "Overdrives",
    "Blitzball",
    "Bosses",
    "Monster Arena",
    "Airship",
}


TABLE_SCHEMAS = [
    # (header tuple, columns per row, title_cols, body_cols)
    (("Character", "Weapon", "Description"), 3, (0, 1), (2,)),
    (("Position", "Player", "Location", "Comment"), 4, (0, 1), (2, 3)),
    (("Monster", "Location", "Item"), 3, (0,), (1, 2)),
]


def _make_item(
    session_id: str,
    item_counter: int,
    title: str,
    body: str,
    *,
    optional: bool = False,
    missable: bool = False,
    category: str | None = None,
) -> dict:
    return {
        "type": "item",
        "id": f"{session_id}-{item_counter:03d}",
        "title": title,
        "optional": optional,
        "missable": missable,
        "category": category,
        "richText": parse_rich_text(body if body else title),
        "images": [],
    }


BLITZ_POSITIONS = {"LF", "RF", "MF", "LD", "RD", "GL"}


def extract_table_items(body: str, session_id: str, start_at: int) -> list[dict]:
    """Turn flattened Steam-guide tables into trackable checklist items."""
    values = [ln.strip() for ln in body.splitlines() if ln.strip()]
    if not values:
        return []

    items: list[dict] = []
    counter = start_at

    # Character / Weapon / Description (FFVII Ultimate Weapons)
    for start in range(0, len(values) - 2):
        if values[start : start + 3] == ["Character", "Weapon", "Description"]:
            cursor = start + 3
            while cursor + 2 < len(values):
                character, weapon, desc = values[cursor : cursor + 3]
                if character in {"Character", "Position", "Monster"} or character in DEFAULT_HEADINGS:
                    break
                if character.startswith("¹") or character.startswith("Thank"):
                    break
                counter += 1
                items.append(
                    _make_item(
                        session_id,
                        counter,
                        clean_inline(f"{character} — {weapon}"),
                        clean_inline(f"{character} — {weapon}: {desc}"),
                        category="Weapon",
                    )
                )
                cursor += 3
            break

    # Blitzball roster: Position codes with variable-length comments
    if "Position" in values and "Player" in values:
        try:
            header_at = values.index("Position")
            if values[header_at : header_at + 4] == [
                "Position",
                "Player",
                "Location",
                "Comment",
            ]:
                cursor = header_at + 4
                while cursor < len(values):
                    pos = values[cursor]
                    if pos.startswith("¹") or pos.startswith("²") or pos in DEFAULT_HEADINGS:
                        break
                    if pos not in BLITZ_POSITIONS:
                        cursor += 1
                        continue
                    if cursor + 2 >= len(values):
                        break
                    player = values[cursor + 1]
                    location = values[cursor + 2]
                    cursor += 3
                    comment_parts: list[str] = []
                    while cursor < len(values) and values[cursor] not in BLITZ_POSITIONS:
                        if values[cursor].startswith("¹") or values[cursor].startswith("²"):
                            break
                        if values[cursor] in DEFAULT_HEADINGS | {
                            "Refresh Prizes",
                            "Recruit Busy Players",
                            "Durren",
                            "Blitzball Team",
                        }:
                            break
                        comment_parts.append(values[cursor])
                        cursor += 1
                    comment = " ".join(comment_parts)
                    counter += 1
                    title = clean_inline(f"{pos} — {player}")
                    body_text = clean_inline(
                        f"{title} @ {location}" + (f" — {comment}" if comment else "")
                    )
                    items.append(
                        _make_item(
                            session_id,
                            counter,
                            title,
                            body_text,
                            category="Blitzball",
                        )
                    )
        except ValueError:
            pass

    # Monster / Location / Item
    for start in range(0, len(values) - 2):
        if values[start : start + 3] == ["Monster", "Location", "Item"]:
            cursor = start + 3
            while cursor + 2 < len(values):
                monster, location, item = values[cursor : cursor + 3]
                if monster in {"Monster", "Character", "Position"} or monster in DEFAULT_HEADINGS:
                    break
                counter += 1
                items.append(
                    _make_item(
                        session_id,
                        counter,
                        clean_inline(monster),
                        clean_inline(f"{monster} @ {location} — {item}"),
                        category="Monster",
                    )
                )
                cursor += 3
            break

    return items


def parse_session_body(
    title: str, body: str, session_id: str, cfg: GuideConfig
) -> dict:
    lines = body.splitlines()
    blocks: list[dict] = []
    item_counter = 0
    note_buf: list[str] = []
    bullet_buf: list[str] | None = None
    headings = DEFAULT_HEADINGS | cfg.heading_extras

    def flush_note() -> None:
        nonlocal note_buf
        text = clean_inline(" ".join(note_buf))
        note_buf = []
        if text:
            blocks.append({"type": "note", "richText": parse_rich_text(text)})

    def flush_bullet() -> None:
        nonlocal bullet_buf, item_counter
        if not bullet_buf:
            return
        raw = clean_inline(" ".join(bullet_buf))
        bullet_buf = None
        if not raw:
            return
        item_counter += 1
        item_title, _rest = extract_title_from_bullet(raw)
        optional = any(
            item_title.startswith(p) or raw.startswith(p) for p in cfg.optional_prefixes
        )
        missable = raw.lstrip().startswith("⚠")
        category = None
        cat_src = re.sub(r"^⚠\s*", "", item_title.lstrip("+")).strip()
        cat_m = re.match(r"^([A-Za-z][A-Za-z /]+?)(?:\s*\(|:)", cat_src)
        if cat_m:
            category = cat_m.group(1).strip()
        title_clean = re.sub(r"^⚠\s*", "", item_title.lstrip("+")).strip()
        blocks.append(
            _make_item(
                session_id,
                item_counter,
                title_clean,
                raw,
                optional=optional and not missable,
                missable=missable,
                category=category,
            )
        )

    for line in lines:
        stripped = line.strip()
        if not stripped:
            flush_bullet()
            continue
        is_bullet = bool(re.match(r"^[\*\-•]\s+", stripped))
        if is_bullet or (stripped.startswith("⚠") and ":" in stripped[:90]):
            flush_note()
            flush_bullet()
            bullet_buf = [re.sub(r"^[\*\-•]\s+", "", stripped)]
            continue
        if bullet_buf is not None and (
            line.startswith(" ")
            or line.startswith("\t")
            or re.match(r"^\d+\.", stripped)
        ):
            bullet_buf.append(stripped)
            continue
        flush_bullet()
        # Numbered checklist steps as their own items when not continuing a bullet
        if re.match(r"^\d+\.\s+\S", stripped) and len(stripped) > 8:
            flush_note()
            item_counter += 1
            step_title = stripped
            if len(step_title) > 70:
                step_title = step_title[:67].rstrip() + "…"
            blocks.append(
                _make_item(
                    session_id,
                    item_counter,
                    step_title,
                    stripped,
                    optional=True,
                    category="Step",
                )
            )
            continue
        if (
            len(stripped) < 70
            and not stripped.endswith(".")
            and (
                stripped.isupper()
                or stripped in headings
                or stripped.startswith("ATE")
                or stripped.startswith("Exploration")
                or (stripped.startswith("**") and stripped.endswith("**"))
            )
        ):
            flush_note()
            label = stripped.strip("*").strip()
            blocks.append({"type": "heading", "text": label})
            continue
        note_buf.append(stripped)

    flush_bullet()
    flush_note()

    # If bullets/notes left a table unparsed, synthesize items from known tables.
    if not any(b.get("type") == "item" for b in blocks) or title in {
        "Ultimate Weapons",
        "Blitzball",
    }:
        table_items = extract_table_items(body, session_id, item_counter)
        if table_items:
            existing = {b.get("title") for b in blocks if b.get("type") == "item"}
            for item in table_items:
                if item["title"] not in existing:
                    item_counter += 1
                    item["id"] = f"{session_id}-{item_counter:03d}"
                    blocks.append(item)

    # Promote notable prose subsections (heading + following note) into checklist items
    # for reference sessions that are otherwise hard to track.
    if title in {"Blitzball", "Ultimate Weapons", "FFX-2: Introduction"}:
        promoted: list[dict] = []
        i = 0
        while i < len(blocks):
            b = blocks[i]
            if (
                b.get("type") == "heading"
                and i + 1 < len(blocks)
                and blocks[i + 1].get("type") == "note"
                and b.get("text")
                not in {"Blitzball Team", "Mode", "Celestial Mirror", "Celestial Weapons"}
            ):
                item_counter += 1
                note_text = " ".join(
                    p.get("text", "") for p in blocks[i + 1].get("richText", [])
                )
                promoted.append(
                    _make_item(
                        session_id,
                        item_counter,
                        b["text"],
                        note_text or b["text"],
                        missable=b["text"].lower() == "durren",
                        optional=b["text"].lower() != "durren",
                        category=title,
                    )
                )
                i += 2
                continue
            promoted.append(b)
            i += 1
        blocks = promoted

    warning = None
    for b in blocks:
        if b.get("type") == "note":
            joined = " ".join(p.get("text", "") for p in b.get("richText", []))
            low = joined.lower()
            if (
                "one time area" in low
                or "unrevisitable" in low
                or "point of no return" in low
            ):
                warning = joined
                break

    items = [b for b in blocks if b.get("type") == "item"]
    return {
        "id": session_id,
        "title": title,
        "warning": warning,
        "blocks": blocks,
        "itemCount": len(items),
    }


def parse_guide(cfg: GuideConfig) -> dict:
    content = cfg.source.read_text(encoding="utf-8")
    spans = find_session_spans(content, cfg)
    if not spans:
        raise SystemExit(f"No sessions found in {cfg.source}")

    sessions = []
    seen_ids: dict[str, int] = {}
    for title, start, end in spans:
        body = content[start:end]
        base = slugify(title)
        seen_ids[base] = seen_ids.get(base, 0) + 1
        sid = base if seen_ids[base] == 1 else f"{base}-{seen_ids[base]}"
        sessions.append(parse_session_body(title, body, sid, cfg))

    sessions = [
        s
        for s in sessions
        if s["title"] not in cfg.drop_titles or s["itemCount"] > 0
    ]

    game = {
        "id": cfg.game_id,
        "title": cfg.title,
        "shortTitle": cfg.short_title,
        "steamAppId": cfg.steam_app_id,
        "source": {
            "title": cfg.source_title,
            "author": cfg.source_author,
            "url": cfg.source_url,
            "note": "Bundled for offline use. All credit to the original guide author.",
        },
        "sessions": sessions,
    }

    cfg.output.parent.mkdir(parents=True, exist_ok=True)
    cfg.output.write_text(
        json.dumps(game, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    total_items = sum(s["itemCount"] for s in sessions)
    print(f"Wrote {cfg.output}")
    print(f"Sessions: {len(sessions)} | Trackable items: {total_items}")
    for s in sessions[:4]:
        print(f"  - {s['title']}: {s['itemCount']} items")
    print("  ...")
    for s in sessions[-3:]:
        print(f"  - {s['title']}: {s['itemCount']} items")
    return game
