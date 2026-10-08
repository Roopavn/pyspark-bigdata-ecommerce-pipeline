import json
from pathlib import Path


def read_watermark(state_file: str, dataset: str) -> str | None:
    path = Path(state_file)
    if not path.exists():
        return None

    state = json.loads(path.read_text(encoding="utf-8"))
    return state.get(dataset)


def write_watermark(state_file: str, dataset: str, watermark: str) -> None:
    path = Path(state_file)
    path.parent.mkdir(parents=True, exist_ok=True)

    state = {}
    if path.exists():
        state = json.loads(path.read_text(encoding="utf-8"))

    state[dataset] = watermark

    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    temp_path.replace(path)
