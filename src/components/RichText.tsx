import { useState, type CSSProperties } from "react";
import type { RichPart } from "../types";

const wrapStyle: CSSProperties = {
  color: "#c6d4df",
  fontSize: "13px",
  lineHeight: 1.45,
  wordBreak: "break-word",
  overflowWrap: "anywhere",
  whiteSpace: "pre-wrap",
  maxWidth: "100%",
};

export function RichText({ parts }: { parts: RichPart[] }) {
  if (!parts?.length) return null;

  return (
    <div style={wrapStyle}>
      {parts.map((part, i) => {
        if (part.type === "bold") {
          return (
            <strong key={i} style={{ color: "#e5e5e5", fontWeight: 600 }}>
              {part.text}{" "}
            </strong>
          );
        }
        if (part.type === "spoiler") {
          return <Spoiler key={i} text={part.text} />;
        }
        return <span key={i}>{part.text} </span>;
      })}
    </div>
  );
}

function Spoiler({ text }: { text: string }) {
  const [revealed, setRevealed] = useState(false);
  return (
    <span
      onClick={(e) => {
        e.stopPropagation();
        setRevealed((v) => !v);
      }}
      style={{
        display: "inline",
        cursor: "pointer",
        background: revealed ? "transparent" : "#1b2838",
        color: revealed ? "#c6d4df" : "#1b2838",
        borderRadius: 3,
        padding: "0 4px",
        border: "1px solid #3d4450",
      }}
      title={revealed ? "Hide spoiler" : "Reveal spoiler"}
    >
      {text}
    </span>
  );
}

export function FitImage({ src, alt }: { src: string; alt: string }) {
  return (
    <img
      src={src}
      alt={alt}
      style={{
        display: "block",
        width: "100%",
        maxWidth: "100%",
        height: "auto",
        borderRadius: 4,
        marginTop: 8,
        marginBottom: 4,
        objectFit: "contain",
      }}
    />
  );
}
