#!/usr/bin/env python3
"""Parse the FFVII Steam guide markdown into structured missables JSON."""

from pathlib import Path

from guide_parser import GuideConfig, parse_guide

ROOT = Path(__file__).resolve().parents[1]

SESSIONS = [
    "Introduction",
    "Sector 7",
    "Sector 5",
    "Wall Market: Dress",
    "Train Graveyard",
    "Wall Market: Revisit",
    "Shinra Building",
    "Overworld: Yuffie Kisaragi",
    "Fort Condor: Minigame",
    "Cargo Ship",
    "Costa del Sol",
    "Mt. Corel",
    "Corel Prison",
    "Gold Saucer",
    "Gongaga Village",
    "Overworld: Misc",
    "Cave of the Gi",
    "Nibelheim",
    "Rocket Town",
    "Overworld: Sidequest",
    "Gold Saucer: Date Night",
    "Temple of the Ancients",
    "Sleeping Forest",
    "Gaea Cliffs",
    "Crater",
    "Whirlwind Maze",
    "Mideel",
    "Mt. Corel: Train",
    "Fort Condor",
    "Mideel: Ultimate Weapon",
    "Underwater Reactor",
    "Optional: Sunken Gelnika & Stat Maxing",
    "Optional: Return to Midgar",
    "Optional: Wutai Village",
    "Rocket Town: Revisit",
    "Cosmo Canyon: Huge Materia",
    "Overworld: Diamond Weapon",
    "Midgar Raid",
    "Point of no Return: Northern Cave",
    "Chocobo Racing",
    "Ultimate Weapons",
    "Limit Breaks",
    "Thank you",
]

CONFIG = GuideConfig(
    source=ROOT / "scripts" / "ffvii-guide-source.md",
    output=ROOT / "src" / "data" / "games" / "final-fantasy-vii.json",
    sessions=SESSIONS,
    game_id="final-fantasy-vii",
    title="Final Fantasy VII",
    short_title="FF VII",
    steam_app_id=39140,
    source_title="FFVII - Missable & Optional Content",
    source_author="Abyss",
    source_url="https://steamcommunity.com/sharedfiles/filedetails/?id=2836675266",
    start_marker="\n Introduction \n",
    duplicate_renames={
        ("Overworld: Sidequest", 2): "Overworld: Sidequest (Post-Reactor)",
        ("Overworld: Sidequest", 3): "Overworld: Sidequest (Pre-Northern Cave)",
    },
    drop_titles={"Thank You", "Thank you", "Comments"},
    heading_extras={
        "Gold Saucer Date",
        "Materia Overlord",
        "Chocobo Racing",
        "Ultimate Weapons",
        "Limit Breaks",
    },
)

if __name__ == "__main__":
    parse_guide(CONFIG)
