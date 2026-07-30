from __future__ import annotations

import json
import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


def _load_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        values[key] = value
        os.environ.setdefault(key, value)
    return values


@dataclass(slots=True)
class Settings:
    root: Path
    raw: dict[str, Any]
    taxonomy: dict[str, Any]
    local_env: dict[str, str] = field(default_factory=dict)

    def section(self, name: str) -> dict[str, Any]:
        return self.raw.get(name, {})

    def project_path(self, key: str) -> Path:
        value = self.section("project")[key]
        return (self.root / value).resolve()

    def llm_value(self, key: str) -> str:
        llm = self.section("llm")
        env_key = llm.get(f"{key}_env", "")
        if env_key and self.local_env.get(env_key):
            return self.local_env[env_key].strip()
        if env_key and os.getenv(env_key):
            return os.environ[env_key].strip()
        return str(llm.get(key, "")).strip()


def load_settings(path: str | Path) -> Settings:
    config_path = Path(path).resolve()
    local_env = _load_env_file(config_path.parent / ".env")
    with config_path.open("rb") as handle:
        raw = tomllib.load(handle)
    root = config_path.parent
    taxonomy_path = root / raw["project"].get("taxonomy_file", "taxonomy.json")
    taxonomy = json.loads(taxonomy_path.read_text(encoding="utf-8"))
    return Settings(root=root, raw=raw, taxonomy=taxonomy, local_env=local_env)
