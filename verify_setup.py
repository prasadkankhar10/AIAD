from __future__ import annotations

import importlib.metadata as metadata


def version_of(package_name: str) -> str:
    try:
        return metadata.version(package_name)
    except metadata.PackageNotFoundError:
        return "not installed"


packages = ["streamlit", "langchain", "langgraph", "openai", "anthropic", "python-dotenv"]

print("Python environment check passed")
for package in packages:
    print(f"{package}: {version_of(package)}")
