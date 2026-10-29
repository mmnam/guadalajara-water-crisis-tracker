import os
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
ROOT = Path(__file__).resolve().parent.parent

def database_path():
    path = Path(os.getenv("DATABASE_PATH", "data/memoria.sqlite3"))
    return path if path.is_absolute() else ROOT / path

class ManagedConnection(sqlite3.Connection):
    def __exit__(self, *args):
        try:
            return super().__exit__(*args)
        finally:
            self.close()


def connect(read_only=False):
    path = database_path()
    if read_only:
        conn = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True, factory=ManagedConnection)
        conn.execute("PRAGMA query_only=ON")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(path, factory=ManagedConnection)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def initialize():
    with connect() as conn:
        conn.executescript((ROOT / "database/schema.sql").read_text())
