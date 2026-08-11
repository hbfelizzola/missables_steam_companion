import { ButtonItem, PanelSectionRow } from "@decky/ui";
import type { Session } from "../types";
import { MissableItem } from "./MissableItem";
import { RichText } from "./RichText";

interface Props {
  session: Session;
  checked: Record<string, boolean>;
  collapsed: boolean;
  progressDone: number;
  progressTotal: number;
  onToggleCollapse: () => void;
  onToggleItem: (id: string, value: boolean) => void;
}

export function SessionSection({
  session,
  checked,
  collapsed,
  progressDone,
  progressTotal,
  onToggleCollapse,
  onToggleItem,
}: Props) {
  const progressLabel =
    progressTotal > 0 ? `${progressDone}/${progressTotal}` : "notes";
  const chevron = collapsed ? "▸" : "▾";

  return (
    <div
      style={{
        marginBottom: 4,
        borderBottom: "1px solid rgba(255,255,255,0.08)",
        maxWidth: "100%",
        overflow: "hidden",
      }}
    >
      <PanelSectionRow>
        <ButtonItem layout="below" onClick={onToggleCollapse}>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              gap: 8,
              maxWidth: "100%",
              overflow: "hidden",
              color: "#c7b08b",
              fontWeight: 700,
              letterSpacing: "0.03em",
              textTransform: "uppercase",
              fontSize: 13,
            }}
          >
            <span
              style={{
                minWidth: 0,
                overflow: "hidden",
                textOverflow: "ellipsis",
                whiteSpace: "nowrap",
              }}
            >
              {chevron} {session.title}
            </span>
            <span style={{ color: "#8f98a0", flexShrink: 0, fontWeight: 500 }}>
              {progressLabel}
            </span>
          </div>
        </ButtonItem>
      </PanelSectionRow>

      {!collapsed && (
        <div style={{ maxWidth: "100%", overflow: "hidden", paddingBottom: 8 }}>
          {session.warning && (
            <PanelSectionRow>
              <div
                style={{
                  color: "#e0a060",
                  fontSize: "12px",
                  lineHeight: 1.4,
                  wordBreak: "break-word",
                  overflowWrap: "anywhere",
                  padding: "0 4px 8px",
                }}
              >
                {session.warning}
              </div>
            </PanelSectionRow>
          )}

          {session.blocks.map((block, idx) => {
            if (block.type === "heading") {
              return (
                <div
                  key={`h-${idx}`}
                  style={{
                    color: "#67c1f5",
                    fontSize: "12px",
                    fontWeight: 600,
                    letterSpacing: "0.03em",
                    textTransform: "uppercase",
                    padding: "8px 4px 4px",
                    wordBreak: "break-word",
                  }}
                >
                  {block.text}
                </div>
              );
            }
            if (block.type === "note") {
              return (
                <div key={`n-${idx}`} style={{ padding: "2px 4px 8px" }}>
                  <RichText parts={block.richText} />
                </div>
              );
            }
            return (
              <MissableItem
                key={block.id}
                item={block}
                checked={!!checked[block.id]}
                onToggle={onToggleItem}
              />
            );
          })}
        </div>
      )}
    </div>
  );
}
