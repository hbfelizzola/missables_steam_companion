import { ButtonItem, PanelSection, PanelSectionRow } from "@decky/ui";
import type { CSSProperties } from "react";
import type { AllProgress, GameData } from "../types";

interface Props {
  games: GameData[];
  progress: AllProgress;
  onSelect: (gameId: string) => void;
}

const cardStyle: CSSProperties = {
  display: "flex",
  gap: 10,
  alignItems: "center",
  maxWidth: "100%",
  overflow: "hidden",
};

export function GameList({ games, progress, onSelect }: Props) {
  return (
    <div style={{ maxWidth: "100%", overflowX: "hidden" }}>
      <PanelSection title="Missables Tracker">
        <PanelSectionRow>
          <div
            style={{
              color: "#8f98a0",
              fontSize: "12px",
              lineHeight: 1.4,
              wordBreak: "break-word",
              paddingBottom: 8,
            }}
          >
            Pick a game to track missable and optional content. Progress is saved
            on this Deck.
          </div>
        </PanelSectionRow>
      </PanelSection>

      <PanelSection title="Games">
        {games.map((game) => {
          const checked = progress[game.id]?.checked || {};
          const total = game.sessions.reduce((n, s) => n + s.itemCount, 0);
          const done = Object.values(checked).filter(Boolean).length;
          return (
            <PanelSectionRow key={game.id}>
              <ButtonItem layout="below" onClick={() => onSelect(game.id)}>
                <div style={cardStyle}>
                  {game.coverUrl && (
                    <img
                      src={game.coverUrl}
                      alt=""
                      style={{
                        width: 40,
                        height: 60,
                        objectFit: "cover",
                        borderRadius: 3,
                        flexShrink: 0,
                      }}
                    />
                  )}
                  <div style={{ minWidth: 0, flex: 1, textAlign: "left" }}>
                    <div
                      style={{
                        fontWeight: 600,
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                        whiteSpace: "nowrap",
                      }}
                    >
                      {game.title}
                    </div>
                    <div style={{ fontSize: 12, color: "#8f98a0" }}>
                      {done}/{total} checked · {game.sessions.length} sessions
                    </div>
                  </div>
                </div>
              </ButtonItem>
            </PanelSectionRow>
          );
        })}
      </PanelSection>
    </div>
  );
}
