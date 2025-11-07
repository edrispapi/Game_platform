from pathlib import Path

__path__ = [str(Path(__file__).resolve().parent)]
from ..orm.declarative import declarative_base

__all__ = ["declarative_base"]
