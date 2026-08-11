import { ButtonItem, PanelSectionRow, ToggleField } from "@decky/ui";
import type { CSSProperties } from "react";
import { useState } from "react";
import type { ContentBlock } from "../types";
import { FitImage, RichText } from "./RichText";

type ItemBlock = Extract<ContentBlock, { type: "item" }>;

interface Props {
  item: ItemBlock;
  checked: boolean;
  onToggle: (id: string, value: boolean) => void;
}

const detailStyle: CSSProperties = {
  padding: "0 4px 10px 4px",
  maxWidth: "100%",
  overflow: "hidden",
};

export function MissableItem({ item, checked, onToggle }: Props) {
  const [expanded, setExpanded] = useState(false);
  const hasDetail =
    item.richText.length > 0 || (item.images && item.images.length > 0);

  return (
    <div style={{ maxWidth: "100%", overflow: "hidden" }}>
      <PanelSectionRow>
        <ToggleField
          label={item.title}
          description={
            [
              item.missable ? "Missable" : null,
              item.optional ? "Optional" : null,
              item.category || null,
            ]
              .filter(Boolean)
              .join(" · ") || undefined
          }
          checked={checked}
          onChange={(value) => onToggle(item.id, value)}
          bottomSeparator="none"
        />
      </PanelSectionRow>
      {hasDetail && (
        <>
          <PanelSectionRow>
            <ButtonItem layout="below" onClick={() => setExpanded((v) => !v)}>
              {expanded ? "Hide details ▴" : "Show details ▾"}
            </ButtonItem>
          </PanelSectionRow>
          {expanded && (
            <div style={detailStyle}>
              <RichText parts={item.richText} />
              {(item.images || []).map((src) => (
                <FitImage key={src} src={src} alt={item.title} />
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}
