# tests/conftest.py

import pytest
import sys
import os

# Add the parent directory to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
