"""
Configuration for RAG chatbot tests.
Handles import paths and test setup.
"""

import sys
import os

# Add the project root to Python path
project_root = os.path.join(os.path.dirname(__file__), "../../..")
if project_root not in sys.path:
    sys.path.insert(0, project_root)
