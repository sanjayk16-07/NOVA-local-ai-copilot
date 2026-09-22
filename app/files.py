from pathlib import Path
from typing import List, Dict


# Files and folders that NOVA must never index
IGNORED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".idea",
    ".vscode",
}


# Sensitive files that should never enter the local semantic index
SENSITIVE_FILES = {
    ".env",
    ".env.local",
    ".env.production",
    ".env.development",
}


# File extensions NOVA is currently allowed to read
SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".cs",
    ".go",
    ".rs",
    ".php",
    ".rb",
    ".swift",
    ".kt",
    ".html",
    ".css",
    ".scss",
    ".json",
    ".yaml",
    ".yml",
    ".md",
    ".txt",
}


def is_sensitive_file(path: Path) -> bool:
    """
    Check whether a file contains potentially sensitive information.
    """

    filename = path.name.lower()

    # Directly ignore known secret/config files
    if filename in SENSITIVE_FILES:
        return True

    # Ignore common private key / credential files
    sensitive_extensions = {
        ".pem",
        ".key",
        ".p12",
        ".pfx",
    }

    if path.suffix.lower() in sensitive_extensions:
        return True

    return False


def is_supported_file(path: Path) -> bool:
    """
    Check whether NOVA supports this file type.
    """

    return path.suffix.lower() in SUPPORTED_EXTENSIONS


def should_ignore_directory(path: Path) -> bool:
    """
    Check whether NOVA should skip this directory.
    """

    return path.name.lower() in IGNORED_DIRS


def read_project_files(project_path: str) -> List[Dict[str, str]]:
    """
    Scan a local project and return safe, supported files.

    Sensitive files and ignored directories are excluded
    before the files are returned to the rest of NOVA.
    """

    root = Path(project_path)

    if not root.exists():
        raise FileNotFoundError(
            f"Project path does not exist: {project_path}"
        )

    documents = []

    for path in root.rglob("*"):

        # Skip directories that should never be scanned
        if path.is_dir():
            continue

        # Skip files inside ignored directories
        if any(should_ignore_directory(parent) for parent in path.parents):
            continue

        # Security check happens before reading the file
        if is_sensitive_file(path):
            continue

        # Only process supported source/document files
        if not is_supported_file(path):
            continue

        try:
            content = path.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            documents.append(
                {
                    "path": str(path.relative_to(root)),
                    "content": content,
                }
            )

        except (OSError, UnicodeError):
            # If a file cannot safely be read, skip it.
            continue

    return documents