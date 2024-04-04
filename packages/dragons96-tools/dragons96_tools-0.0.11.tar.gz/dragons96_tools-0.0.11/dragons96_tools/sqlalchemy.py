from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession
from contextlib import contextmanager, asynccontextmanager
from typing import Any, Type, TypeVar
from pydantic import BaseModel

_T = TypeVar('_T', bound='BaseModel')
_BASE = TypeVar('_BASE', bound='Base')


class Base(DeclarativeBase):
    """ orm model 基础类 """

    def to_dict(self) -> dict:
        """
        将当前model转为dict对象
        """
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

    def to_model(self, modelclass: Type[BaseModel]) -> _T:
        """
        将当前model转为pydantic的model对象
        :param modelclass: 具体的模型类型
        """
        return modelclass(**(self.to_dict()))

    @classmethod
    def from_model(cls,
                   model: BaseModel,
                   ignore_absent_fields: bool = True,
                   include: Any = None,
                   exclude: Any = None,
                   by_alias: bool = False,
                   exclude_unset: bool = False,
                   exclude_defaults: bool = False,
                   exclude_none: bool = False,
                   round_trip: bool = False,
                   ) -> _BASE:
        """
        将pydantic的model转为当前类型model
        :param model: pydantic的模型值
        :param ignore_absent_fields: 忽略当前model中不存在的pydantic model的属性
        :param include: A list of fields to include in the output.
        :param exclude: A list of fields to exclude from the output.
        :param by_alias: Whether to use the field's alias in the dictionary key if defined.
        :param exclude_unset: Whether to exclude fields that have not been explicitly set.
        :param exclude_defaults: Whether to exclude fields that are set to their default value.
        :param exclude_none: Whether to exclude fields that have a value of `None`.
        :param round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
        """
        model_dict = model.model_dump(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip
        )
        if ignore_absent_fields:
            for key in list(model_dict.keys()):
                if not hasattr(cls, key):
                    del model_dict[key]
        return cls(**model_dict)


class SqlAlchemyClient:
    """
    SqlAlchemy工具客户端
    """
    def __init__(self, url: str, echo: bool = False, **kwargs: Any):
        """
        创建sqlalchemy工具客户端
        :param url: 连接串
            示例:
                sqlite:///dbname
                mysql+pymysql://username:password@host:port/dbname
        :param echo: The echo=True parameter indicates that SQL emitted by connections will be logged to standard out.
        """
        self._engine = create_engine(url, echo=echo, **kwargs)
        self._session_maker = sessionmaker(bind=self._engine, expire_on_commit=False)

    @contextmanager
    def session(self) -> Session:
        """
        获取session上下文对象
        使用示例:
            helper = SqlAlchemyHelper('xxxx')
            with helper.session() as session:
                session.execute()
                session.get()
        """
        session = self._session_maker()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
        finally:
            if session:
                session.close()

    def engine(self) -> Engine:
        """ 获取引擎 """
        return self._engine


class AsyncSqlAlchemyClient:
    """
    SqlAlchemy异步工具客户端
    """
    def __init__(self, url: str, echo: bool = False, **kwargs: Any):
        """
        创建sqlalchemy异步工具客户端
        :param url: 连接串
            示例:
                sqlite:///dbname
                mysql+pymysql://username:password@host:port/dbname
        :param echo: The echo=True parameter indicates that SQL emitted by connections will be logged to standard out.
        """
        self._engine = create_async_engine(url, echo=echo, **kwargs)
        self._session_maker = async_sessionmaker(bind=self._engine)

    @asynccontextmanager
    async def session(self) -> AsyncSession:
        """
        获取session上下文对象
        使用示例:
            helper = SqlAlchemyHelper('xxxx')
            with helper.session() as session:
                session.execute()
                session.get()
        """
        session = self._session_maker()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
        finally:
            if session:
                await session.close()

    def engine(self) -> AsyncEngine:
        """ 获取引擎 """
        return self._engine
