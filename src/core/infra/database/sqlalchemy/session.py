import abc

from asyncio import current_task
from contextlib import asynccontextmanager
import contextvars
import logging
from typing import TYPE_CHECKING, Any, AsyncContextManager, AsyncIterator, Dict, Optional, cast

from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import settings


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio.engine import AsyncEngine


logger = logging.getLogger(__name__)


db_session_context: contextvars.ContextVar = contextvars.ContextVar('db_ctx', default={'session': None, 'level': 0})


class AbstractDatabase(abc.ABC):
    @abc.abstractmethod
    def session(self) -> AsyncContextManager[AsyncSession]:
        ...


def _get_current_task_id() -> int:
    return id(current_task())


# @singleton
class Database(AbstractDatabase):
    def __init__(self) -> None:
        self.engine: AsyncEngine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)
        session_local: sessionmaker = sessionmaker(
            self.engine, class_=AsyncSession, autocommit=False, autoflush=False, expire_on_commit=False
        )
        # SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, class_=AsyncSession)
        self._session_factory = async_scoped_session(session_local, scopefunc=_get_current_task_id)

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        db_session: Optional[Dict[str, Any]] = None
        db_session = db_session_context.get() or {'session': None, 'level': 0}
        if db_session['level'] == 0:
            session: AsyncSession = cast(AsyncSession, self._session_factory())
            db_session['session'] = session
            # await session.begin()
            logger.debug('session begin', extra={'level': db_session['level']})

        else:
            session = db_session['session']
            db_session['level'] = (db_session['level'] or 0) + 1
        db_session_context.set(db_session)

        try:
            yield session
        except Exception:
            logger.exception('Session rollback because of exception')
            await session.rollback()
            logger.debug('session rollback')
            raise
        else:
            # db_session = db_session_context.get() or {'session': None, 'level': 0}
            if db_session['level'] == 0:
                await session.commit()
                logger.debug('session commit', extra={'level': db_session['level']})
        finally:
            # db_session = db_session_context.get() or {'session': None, 'level': 0}
            if db_session['level'] == 0:
                await session.close()
                logger.debug('session close', extra={'level': db_session['level']})
                db_session_context.set(None)
            else:
                db_session['level'] = (db_session['level'] or 0) - 1
                db_session_context.set(db_session)
