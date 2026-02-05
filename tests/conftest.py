"""
Pytest configuration and fixtures.
"""

import pytest
from pathlib import Path


@pytest.fixture
def project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def sample_cwd(tmp_path: Path) -> Path:
    """Create a temporary directory with basic project structure."""
    # Create minimal project structure for testing
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    (src_dir / "__init__.py").write_text("")
    (src_dir / "sample.py").write_text('def hello() -> str:\n    return "Hello"\n')
    
    # Create .git directory to simulate git repo
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    
    # Create .gitignore
    (tmp_path / ".gitignore").write_text("__pycache__/\n*.pyc\n")
    
    return tmp_path
