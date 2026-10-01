from pathlib import Path

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime
)

from sqlalchemy.orm import (
    declarative_base,
    sessionmaker
)

from datetime import datetime


# ---------------------------------------
# DATABASE LOCATION
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "legalese.db"


# ---------------------------------------
# DATABASE URL
# ---------------------------------------

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


# ---------------------------------------
# DATABASE ENGINE
# ---------------------------------------

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)


# ---------------------------------------
# SESSION
# ---------------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ---------------------------------------
# BASE MODEL
# ---------------------------------------

Base = declarative_base()


# ---------------------------------------
# DOCUMENT TABLE
# ---------------------------------------

class Document(Base):

    __tablename__ = "documents"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    document_type = Column(
        String(200),
        nullable=False
    )

    parties = Column(
        Text,
        nullable=False
    )

    terms = Column(
        Text,
        nullable=False
    )

    dates = Column(
        String(200),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    mode = Column(
        String(50),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# ---------------------------------------
# CREATE TABLES
# ---------------------------------------

def create_tables():

    Base.metadata.create_all(
        bind=engine
    )


# ---------------------------------------
# DATABASE SESSION
# ---------------------------------------

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()