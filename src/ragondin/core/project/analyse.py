import os
from pathlib import Path

TEXT_EXTENSIONS = {
    ".md", ".txt", ".tex", ".py", ".rst", ".json", ".yaml", ".yml", ".csv"
}

def collect_file_paths(path: Path):
    """Return list of file paths for indexing (recursive if folder)."""
    if path.is_file():
        return [path]

    files = []
    for root, dirs, filenames in os.walk(path):
        for fname in filenames:
            f = Path(root) / fname
            files.append(f)
    return files

def is_text_file(path: Path):
    return path.suffix.lower() in TEXT_EXTENSIONS


def estimate_source_recursive(path: Path, chunk_size=800, chunk_overlap=100):
    path = Path(path)
    all_files = collect_file_paths(path)
    
    text_files = [f for f in all_files if is_text_file(f)]
    
    total_chars = 0
    total_tokens = 0
    total_size_bytes = 0
    
    for f in text_files:
        try:
            text = f.read_text(errors="ignore")
        except Exception:
            continue
        
        size = f.stat().st_size
        total_size_bytes += size
        
        total_chars += len(text)
        total_tokens += len(text) // 4  # approx
        
    stride = chunk_size - chunk_overlap
    total_chunks = max(1, total_chars // stride)
    
    return {
        "files": len(text_files),
        "total_size_bytes": total_size_bytes,
        "chars": total_chars,
        "tokens": total_tokens,
        "chunks": total_chunks,
    }
