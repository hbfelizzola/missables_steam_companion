#!/usr/bin/env python3
"""Parse the FFX Steam guide markdown into structured missables JSON."""

from pathlib import Path

from guide_parser import GuideConfig, parse_guide

ROOT = Path(__file__).resolve().parents[1]

SESSIONS = [
    "FFX: Introduction",
    "Ruins",
    "Salvage Ship",
    "Besaid",
    "S.S. Liki",
    "Kilika",
    "S.S. Winno",
    "Luca",
    "Mi'ihen Highroad",
    "Mushroom Rock",
    "Djose Highroad",
    "Moonflow",
    "Guadosalam",
    "Thunder Plains",
    "Macalania",
    "Sanubia Desert",
    "Home",
    "Bevelle",
    "Calm Lands",
    "Remiem Temple",
    "Cavern of the Stolen Fayth",
    "Mt. Gagazet",
    "Zanarkand",
    "POINT OF NO RETURN: Inside Sin",
    "Airship",
    "Monster Arena",
    "Celestial Weapons",
    "Overdrives",
    "Blitzball",
    "Bosses",
    "FFX-2: Introduction",
    "Thank You",
]

CONFIG = GuideConfig(
    source=ROOT / "scripts" / "ffx-guide-source.md",
    output=ROOT / "src" / "data" / "games" / "final-fantasy-x.json",
    sessions=SESSIONS,
    game_id="final-fantasy-x",
    title="Final Fantasy X / X-2 HD Remaster",
    short_title="FF X",
    steam_app_id=359870,
    source_title="FFX - Missable & Optional Content",
    source_author="Abyss",
    source_url="https://steamcommunity.com/sharedfiles/filedetails/?id=3044396628",
    start_marker="\n FFX: Introduction \n",
    drop_titles={"Thank You", "Thank you", "Comments"},
    heading_extras={
        "Sphere Grid",
        "Missables",
        "Cheats",
        "Cloister of Trials",
        "Celestial Weapons",
        "Celestial Mirror",
        "Overdrives",
        "Blitzball",
        "Blitzball Team",
        "Bosses",
        "Monster Arena",
        "Airship",
        "Refresh Prizes",
        "Recruit Busy Players",
        "Durren",
        "Mode",
    },
    optional_prefixes=("+",),
)

if __name__ == "__main__":
    parse_guide(CONFIG)
