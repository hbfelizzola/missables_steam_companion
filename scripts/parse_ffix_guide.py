#!/usr/bin/env python3
"""Parse the FFIX Steam guide markdown into structured missables JSON."""

from pathlib import Path

from guide_parser import GuideConfig, parse_guide

ROOT = Path(__file__).resolve().parents[1]

SESSIONS = [
    "Introduction",
    "Alexandria",
    "Evil Forest",
    "Ice Cavern",
    "Dali",
    "Lindblum",
    "Qu's Marsh",
    "Overworld: Blu Mag 01",
    "Garnet: South Gate",
    "Overworld: Blu Mag 02",
    "Burmecia",
    "Garnet: Summit Station",
    "Garnet: Dali",
    "Steiner: Treno",
    "Garnet: Gargan Roo",
    "Cleyra",
    "Red Rose",
    "Alexandria Castle",
    "Pinnacle Rocks",
    "Lindblum: Revisit",
    "Qu's Marsh: Revisit",
    "Fossil Roo",
    "Overworld: Outer Continent",
    "Conde Petie",
    "Mage Village",
    "Conde Petie: Revisit",
    "Mountain Path",
    "Madain Sari",
    "Iifa Tree",
    "Alexandria: Revisit",
    "Treno: Revisit",
    "Overworld: Detour",
    "Treno: Tournament",
    "Alexandria Castle: Revisit",
    "Lindblum: 2nd Revisit",
    "Overworld: Sidequests",
    "Qu's Marsh: Forgotten Continent",
    "Oeilvert",
    "Desert Palace",
    "Esto Gaza",
    "Mount Gulug",
    "Lindblum Castle",
    "Ipsen's Castle",
    "Point of No Return: Shimmering Island",
    "Bran Bal",
    "Pandemonium",
    "Overworld: Sidequests Part 1",
    "Overworld: Sidequests Part 2",
    "Memoria",
    "Point of No Return: Crystal World",
    "Sidequests",
    "Minigames",
    "Thank You",
]

CONFIG = GuideConfig(
    source=ROOT / "scripts" / "ffix-guide-source.md",
    output=ROOT / "src" / "data" / "games" / "final-fantasy-ix.json",
    sessions=SESSIONS,
    game_id="final-fantasy-ix",
    title="Final Fantasy IX",
    short_title="FF IX",
    steam_app_id=377840,
    source_title="FFIX - Missable & Optional Content",
    source_author="Abyss",
    source_url="https://steamcommunity.com/sharedfiles/filedetails/?id=2988011418",
    start_marker="\n Introduction \n",
    duplicate_renames={
        ("Overworld: Sidequests", 2): "Overworld: Sidequests (Post-Gulug)",
    },
)

if __name__ == "__main__":
    parse_guide(CONFIG)
