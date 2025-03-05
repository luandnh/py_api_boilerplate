from typing import Callable

from sqlmodel import create_engine, Session

from ..config import DBSettings

import logging

logger = logging.getLogger('uvicorn.error')


def create_sqlmodel_engine(settings: DBSettings, **kwargs):
    """Creates a SQLModel engine.

    Args:
        settings (Settings): Application settings.
        **kwargs: Engine parameters.

    Returns:
        Engine: SQLModel engine.
    """

    db_uri = settings.MYSQL_URI
    db_prefix = settings.MYSQL_SYNC_PREFIX
    database_connection_str = f"{db_prefix}{db_uri}"
    
    logger.debug(f"Database connection string: {database_connection_str}")
    
    return create_engine(database_connection_str, **kwargs)


def sqlmodel_session_maker(engine) -> Callable[[], Session]:
    """Returns a SQLModel session maker function.

    Args:
        engine (_type_): SQLModel engine.

    Returns:
        Callable[[], Session]: Session maker function.
    """
    return lambda: Session(bind=engine, autocommit=False, autoflush=False)
