import os
from app.services.pdf_service import extract_text as read_pdf
from app.services.markdown_service import read_markdown, extract_links
from app.services.text_service import read_text

def extract_content(file_path: str) -> tuple[str, list[str]]:
    """
    Decides the correct service to use based on file extension.
    
    Returns:
        tuple[str, list[str]]: (extracted_text, list_of_obsidian_links)
    """
    _, ext = os.path.splitext(file_path.lower())
    
    if ext == ".pdf":
        return read_pdf(file_path), []
    elif ext in (".md", ".markdown"):
        content = read_markdown(file_path)
        links = extract_links(content)
        return content, links
    elif ext in (".txt", ".text"):
        return read_text(file_path), []
    else:
        # Fallback to reading as generic text file
        try:
            return read_text(file_path), []
        except Exception:
            return "", []
