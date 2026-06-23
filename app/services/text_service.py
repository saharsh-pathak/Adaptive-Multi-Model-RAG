def read_text(file_path: str) -> str:
    """Reads and returns the entire contents of a text file."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()
