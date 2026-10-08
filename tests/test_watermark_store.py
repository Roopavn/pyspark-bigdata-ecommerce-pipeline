from src.ingestion.watermark_store import read_watermark, write_watermark


def test_missing_watermark_returns_none(tmp_path):
    state_file = tmp_path / "watermarks.json"

    assert read_watermark(str(state_file), "orders") is None


def test_watermark_can_be_written_and_read(tmp_path):
    state_file = tmp_path / "watermarks.json"

    write_watermark(str(state_file), "orders", "2026-10-08T09:30:00")

    assert read_watermark(str(state_file), "orders") == "2026-10-08T09:30:00"
