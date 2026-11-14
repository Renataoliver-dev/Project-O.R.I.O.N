from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.engine import URL

database_path = Path(__file__).resolve().with_name("orion.db")
engine = create_engine(URL.create("sqlite", database=str(database_path)))
@event.listens_for(engine, "connect")
def enable_foreign_keys(connection, _connection_record):
    connection.execute("PRAGMA foreign_keys = ON")