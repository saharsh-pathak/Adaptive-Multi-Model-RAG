import re

def read_markdown(file_path: str) -> str:
    """Reads and returns the entire contents of a markdown file."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def extract_links(content: str) -> list[str]:
    """
    Extracts Obsidian-style links (e.g. [[NoteName]], [[NoteName#Section]], [[NoteName|Alias]])
    from the markdown content. Returns a unique list of note names.
    """
    # Regex captures target note name before '#', '|' or ']]'
    pattern = r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]"
    matches = re.findall(pattern, content)
    
    # Strip whitespace, deduplicate, and remove empty links
    seen = set()
    unique_links = []
    for match in matches:
        cleaned = match.strip()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            unique_links.append(cleaned)
            
    return unique_links
