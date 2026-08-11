import {
  ButtonItem,
  PanelSection,
  PanelSectionRow,
  ToggleField,
} from "@decky/ui";
import { useMemo, useState } from "react";
import type { GameData, GameProgress } from "../types";
import { SessionSection } from "./SessionSection";

interface Props {
  game: GameData;
  progress: GameProgress;
  onBack: () => void;
  onChange: (next: GameProgress) => void;
}

export function GameTracker({ game, progress, onBack, onChange }: Props) {
  const [hideDone, setHideDone] = useState(false);
  const checked = progress.checked || {};
  const collapsed = progress.collapsed || {};

  const totals = useMemo(() => {
    const total = game.sessions.reduce((n, s) => n + s.itemCount, 0);
    const done = Object.values(checked).filter(Boolean).length;
    return { total, done };
  }, [game.sessions, checked]);

  const setItem = (id: string, value: boolean) => {
    onChange({
      ...progress,
      checked: { ...checked, [id]: value },
    });
  };

  const toggleSession = (sessionId: string) => {
    const currentlyCollapsed = collapsed[sessionId] ?? true;
    onChange({
      ...progress,
      collapsed: { ...collapsed, [sessionId]: !currentlyCollapsed },
    });
  };

  const expandAll = () => {
    const next: Record<string, boolean> = {};
    for (const s of game.sessions) next[s.id] = false;
    onChange({ ...progress, collapsed: next });
  };

  const collapseAll = () => {
    const next: Record<string, boolean> = {};
    for (const s of game.sessions) next[s.id] = true;
    onChange({ ...progress, collapsed: next });
  };

  return (
    <div style={{ maxWidth: "100%", overflowX: "hidden" }}>
      <PanelSection title={game.shortTitle || game.title}>
        <PanelSectionRow>
          <ButtonItem layout="below" onClick={onBack}>
            ← Games
          </ButtonItem>
        </PanelSectionRow>
        <PanelSectionRow>
          <div
            style={{
              color: "#c6d4df",
              fontSize: 13,
              padding: "4px 0 8px",
              wordBreak: "break-word",
            }}
          >
            {totals.done}/{totals.total} items complete
          </div>
        </PanelSectionRow>
        <PanelSectionRow>
          <ToggleField
            label="Hide completed"
            checked={hideDone}
            onChange={setHideDone}
            bottomSeparator="none"
          />
        </PanelSectionRow>
        <PanelSectionRow>
          <ButtonItem layout="below" onClick={expandAll}>
            Expand all sessions
          </ButtonItem>
        </PanelSectionRow>
        <PanelSectionRow>
          <ButtonItem layout="below" onClick={collapseAll}>
            Collapse all sessions
          </ButtonItem>
        </PanelSectionRow>
      </PanelSection>

      <PanelSection title="Sessions">
        {game.sessions.map((session) => {
          if (hideDone && session.itemCount > 0) {
            const allDone = session.blocks.every(
              (b) => b.type !== "item" || checked[b.id]
            );
            if (allDone) return null;
          }

          // Default collapsed = true for compact first view
          const isCollapsed = collapsed[session.id] ?? true;

          const filtered = hideDone
            ? (() => {
                const blocks = session.blocks.filter(
                  (b) => b.type !== "item" || !checked[b.id]
                );
                return {
                  ...session,
                  blocks,
                  itemCount: blocks.filter((b) => b.type === "item").length,
                };
              })()
            : session;

          const progressDone = session.blocks.filter(
            (b) => b.type === "item" && checked[b.id]
          ).length;

          return (
            <SessionSection
              key={session.id}
              session={filtered}
              checked={checked}
              collapsed={isCollapsed}
              progressDone={progressDone}
              progressTotal={session.itemCount}
              onToggleCollapse={() => toggleSession(session.id)}
              onToggleItem={setItem}
            />
          );
        })}
      </PanelSection>

      <PanelSection title="Source">
        <PanelSectionRow>
          <div
            style={{
              color: "#8f98a0",
              fontSize: 11,
              lineHeight: 1.4,
              wordBreak: "break-word",
              overflowWrap: "anywhere",
              paddingBottom: 8,
            }}
          >
            {game.source.title} by {game.source.author}.{" "}
            {game.source.note || ""}
          </div>
        </PanelSectionRow>
      </PanelSection>
    </div>
  );
}
