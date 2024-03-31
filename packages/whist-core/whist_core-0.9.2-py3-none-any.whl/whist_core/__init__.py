"""
Retrieves envs for the whist core module.
"""
import os

# remember to also update the version in pyproject.toml and docs/source/conf.py!
__version__ = '0.9.2'

ALGORITHM = os.getenv('ALGORITHM', 'HS256')
SECRET_KEY = os.getenv('SECRET_KEY', 'geheim')
