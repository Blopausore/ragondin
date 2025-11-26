from typing import Optional, List
from pathlib import Path

from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
    PythonCodeTextSplitter,
    RecursiveJsonSplitter,
    
    Language

)
from langchain_community.document_loaders import TextLoader, PythonLoader
from langchain_core.documents import Document


import csv

def split_python_file_old(text) -> List[Document]:
    import re
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=100
    )

    # On insère des marqueurs avant les defs et classes
    marked = re.sub(r"(\nclass .+?:)", r"\n### \1", text)
    marked = re.sub(r"(\ndef .+?:)", r"\n### \1", marked)

    return splitter.create_documents([marked])


def split_python_file(text) -> List[Document]:
    splitter = PythonCodeTextSplitter(
        chunk_size=1200,
        chunk_overlap=100
    )
    return splitter.create_documents([text])

def split_markdown_file(text) -> List[Document]:
    splitter = MarkdownHeaderTextSplitter(
        [
            ("#", "Header1"),
            ("##", "Header2"),
            ("###", "Header3"),
        ],
        strip_headers=False
    )
    return splitter.split_text(text)

def split_json_file(text) -> List[Document]:
    splitter = RecursiveJsonSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    return splitter.create_documents([text])



def split_yaml_file(text):
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n", " ", "-"],
        chunk_size=800,
        chunk_overlap=100
    )
    return splitter.create_documents([text])

def split_toml_file(text) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n", " ", "."],
        chunk_size=800,
        chunk_overlap=100
    )
    return splitter.create_documents([text])


def split_shell_file(text) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n", " ", ";"],
        chunk_size=800,
        chunk_overlap=100
    )
    return splitter.create_documents([text])

def extract_data_header(text, max_lines=5) -> List[Document]:
    """Extract first N lines as a header. For CSV files."""
    lines = text.splitlines()
    selected = "\n".join(lines[:max_lines])
    return [Document(page_content=selected)]

def split_xml_file(text) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n", " ", ">"],
        chunk_size=800,
        chunk_overlap=100
    )
    return splitter.create_documents([text])

# Special files
def split_dockerfile(text) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n", " ", "#"],
        chunk_size=800,
        chunk_overlap=100
    )
    return splitter.create_documents([text])

def split_makefile(text) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n", " ", "\t"],
        chunk_size=800,
        chunk_overlap=100
    )
    return splitter.create_documents([text])

# Map extensions / special filenames to splitter functions

split_map = {
    # Text files
    ".txt": split_markdown_file,
    ".md": split_markdown_file,
    ".markdown": split_markdown_file,
    ".py": split_python_file,
    ".json": split_json_file,
    ".yaml": split_yaml_file,
    ".yml": split_yaml_file,
    ".toml": split_toml_file,
    ".sh": split_shell_file,
    ".xml": split_xml_file,
    ".csv": extract_data_header,
    # Special files
    "README": split_markdown_file,
    "LICENSE": split_markdown_file,
    "Dockerfile": split_dockerfile,
    "Makefile": split_makefile,
}

banned_extensions = {".exe", ".bin", ".dll", ".so", ".o", ".class", ".jar",
                     ".png", ".jpg", ".jpeg", ".gif", ".bmp"
                     }


def add_header(content, path: Path, source_root: Path) -> str:
    path = Path(path)
    if source_root :
        source_root = Path(source_root)
        rel = path.relative_to(source_root)
        header = f"# FILE: {rel}\n# PATH: {rel.parent}\n\n"
    else:
        header = f"# FILE: {path.name}\n# PATH: .\n\n"
    return header + content

def load_and_split_file(path: Path, source_root=None) -> list[Document]:
    """ Load a file in path, split it and create chunk from them  with specific headers.
    """
    if isinstance(path, str):
        path = Path(path)
    if source_root is not None:
        source_root = Path(source_root)
    suffix = path.suffix.lower()

    if suffix in banned_extensions:
        raise ValueError(f"File extension {suffix} is banned for processing.")    
    
    # 1. Load text
    text = path.read_text(errors="ignore")

    # 2. Choose splitter by extension
    splitter_func = split_map.get(suffix, None)
    if splitter_func is None:
        # Fallback: generic splitter
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )
        docs = splitter.create_documents([text])
    else:
        docs = splitter_func(text)  
        
    # 3. Add headers for context
    wrapped = []
    for d in docs:
        rel = path.relative_to(source_root) if source_root else path.name
        d.metadata["path"] = str(rel)
        d.metadata["file"] = path.name
        d.metadata["source"] = str(path)
        d.page_content = add_header(d.page_content, path, source_root)
        
        wrapped.append(d)

    return wrapped
