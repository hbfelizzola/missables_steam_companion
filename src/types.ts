export type RichPart =
  | { type: "text"; text: string }
  | { type: "bold"; text: string }
  | { type: "spoiler"; text: string };

export type ContentBlock =
  | { type: "heading"; text: string }
  | { type: "note"; richText: RichPart[] }
  | {
      type: "item";
      id: string;
      title: string;
      optional?: boolean;
      missable?: boolean;
      category?: string | null;
      richText: RichPart[];
      images?: string[];
    };

export interface Session {
  id: string;
  title: string;
  warning?: string | null;
  blocks: ContentBlock[];
  itemCount: number;
}

export interface GameSource {
  title: string;
  author: string;
  url: string;
  note?: string;
}

export interface GameData {
  id: string;
  title: string;
  shortTitle: string;
  steamAppId?: number;
  coverUrl?: string;
  source: GameSource;
  sessions: Session[];
}

export type ProgressMap = Record<string, boolean>;

export interface GameProgress {
  checked: ProgressMap;
  collapsed?: Record<string, boolean>;
}

export interface AllProgress {
  [gameId: string]: GameProgress;
}
