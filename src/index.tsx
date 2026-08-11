import {
  definePlugin,
  callable,
} from "@decky/api";
import { staticClasses } from "@decky/ui";
import { useEffect, useState } from "react";
import { FaClipboardCheck } from "react-icons/fa";
import { GameList } from "./components/GameList";
import { GameTracker } from "./components/GameTracker";
import { GAMES, getGame } from "./data/games";
import type { AllProgress, GameProgress } from "./types";

const loadProgress = callable<[], AllProgress>("load_progress");
const saveProgress = callable<[progress: AllProgress], void>("save_progress");

function Content() {
  const [ready, setReady] = useState(false);
  const [selectedGameId, setSelectedGameId] = useState<string | null>(null);
  const [progress, setProgress] = useState<AllProgress>({});

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const data = await loadProgress();
        if (!cancelled) setProgress(data || {});
      } catch (e) {
        console.error("Missables: failed to load progress", e);
      } finally {
        if (!cancelled) setReady(true);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const updateGameProgress = async (gameId: string, next: GameProgress) => {
    const updated: AllProgress = { ...progress, [gameId]: next };
    setProgress(updated);
    try {
      await saveProgress(updated);
    } catch (e) {
      console.error("Missables: failed to save progress", e);
    }
  };

  const shellStyle = {
    maxWidth: "100%" as const,
    overflowX: "hidden" as const,
    boxSizing: "border-box" as const,
  };

  if (!ready) {
    return (
      <div style={{ ...shellStyle, padding: 12, color: "#8f98a0", fontSize: 13 }}>
        Loading…
      </div>
    );
  }

  const game = selectedGameId ? getGame(selectedGameId) : undefined;

  if (game) {
    return (
      <div style={shellStyle}>
        <GameTracker
          game={game}
          progress={progress[game.id] || { checked: {}, collapsed: {} }}
          onBack={() => setSelectedGameId(null)}
          onChange={(next) => updateGameProgress(game.id, next)}
        />
      </div>
    );
  }

  return (
    <div style={shellStyle}>
      <GameList
        games={GAMES}
        progress={progress}
        onSelect={setSelectedGameId}
      />
    </div>
  );
}

export default definePlugin(() => {
  return {
    name: "Missables Tracker",
    titleView: <div className={staticClasses.Title}>Missables Tracker</div>,
    content: <Content />,
    icon: <FaClipboardCheck />,
    onDismount() {
      // no-op
    },
  };
});
