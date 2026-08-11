import type { ContentBlock, GameData } from "../../types";
import finalFantasyIx from "./final-fantasy-ix.json";
import finalFantasyVii from "./final-fantasy-vii.json";
import finalFantasyX from "./final-fantasy-x.json";

function withCover(game: GameData, coverUrl: string): GameData {
  return { ...game, coverUrl };
}

function withDemoImages(game: GameData): GameData {
  // Showcase image embedding on the first game's introduction session.
  if (game.id !== "final-fantasy-ix") return game;
  const sessions = game.sessions.map((session) => {
    if (session.id !== "introduction") return session;
    const demo: ContentBlock = {
      type: "item",
      id: "introduction-cover",
      title: "Guide cover / reference art",
      optional: true,
      category: "Misc",
      richText: [
        {
          type: "text",
          text: "Example image embedding using Steam store artwork. Images always scale to the panel width so the sidebar never scrolls horizontally.",
        },
      ],
      images: [
        "https://cdn.cloudflare.steamstatic.com/steam/apps/377840/header.jpg",
        "https://cdn.cloudflare.steamstatic.com/steam/apps/377840/library_hero.jpg",
      ],
    };
    const blocks = [...session.blocks, demo];
    return {
      ...session,
      blocks,
      itemCount: blocks.filter((b) => b.type === "item").length,
    };
  });
  return { ...game, sessions };
}

export const GAMES: GameData[] = [
  withCover(
    finalFantasyVii as GameData,
    "https://cdn.cloudflare.steamstatic.com/steam/apps/39140/library_600x900.jpg"
  ),
  withCover(
    withDemoImages(finalFantasyIx as GameData),
    "https://cdn.cloudflare.steamstatic.com/steam/apps/377840/library_600x900.jpg"
  ),
  withCover(
    finalFantasyX as GameData,
    "https://cdn.cloudflare.steamstatic.com/steam/apps/359870/library_600x900.jpg"
  ),
];

export function getGame(id: string): GameData | undefined {
  return GAMES.find((g) => g.id === id);
}
