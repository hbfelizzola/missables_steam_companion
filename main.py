import json
import os
from typing import Any, Dict

import decky


SETTINGS_FILE = "missables_progress.json"


class Plugin:
    def _settings_path(self) -> str:
        return os.path.join(decky.DECKY_PLUGIN_SETTINGS_DIR, SETTINGS_FILE)

    async def load_progress(self) -> Dict[str, Any]:
        path = self._settings_path()
        if not os.path.isfile(path):
            return {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                return data
        except Exception as e:
            decky.logger.error(f"Failed to load progress: {e}")
        return {}

    async def save_progress(self, progress: Dict[str, Any]) -> None:
        path = self._settings_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(progress, f, indent=2)
        os.replace(tmp, path)

    async def _main(self):
        decky.logger.info("Missables Tracker loaded")

    async def _unload(self):
        decky.logger.info("Missables Tracker unloading")

    async def _uninstall(self):
        pass

    async def _migration(self):
        pass
