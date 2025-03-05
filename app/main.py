from sqlmodel import SQLModel
from sqlmodel.pool import StaticPool

from .api import router
from .core.config import settings
from .core.app import init_app
from .core.db.database import create_sqlmodel_engine, sqlmodel_session_maker
import logging

logger = logging.getLogger('uvicorn.error')

# Create SQLModel engine
engine = create_sqlmodel_engine(settings=settings, poolclass=StaticPool)
SQLModel.metadata.create_all(engine)
session_maker = sqlmodel_session_maker(engine)


# Create FastAPI app
app = init_app(router=router, settings=settings)
