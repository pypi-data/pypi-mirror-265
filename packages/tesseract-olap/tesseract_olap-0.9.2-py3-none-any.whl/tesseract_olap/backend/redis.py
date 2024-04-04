from io import BytesIO
from typing import TYPE_CHECKING, Union

import polars as pl
import redis

from tesseract_olap.backend import Result
from tesseract_olap.common import hide_dsn_password
from tesseract_olap.exceptions.backend import UpstreamInternalError, UpstreamNotPrepared

from .cache import CacheConnection, CacheConnectionStatus, CacheProvider

if TYPE_CHECKING:
    from tesseract_olap.query import AnyQuery


class RedisProvider(CacheProvider):
    def __init__(self, dsn: str, **kwargs):
        self.dsn = dsn
        self.pool = redis.ConnectionPool.from_url(dsn, **kwargs)

    def __repr__(self):
        return f"{type(self).__name__}(dsn='{hide_dsn_password(self.dsn)}')"

    def connect(self):
        try:
            return RedisConnection(self.pool, single_connection_client=True)
        except redis.ConnectionError as exc:
            raise UpstreamNotPrepared(*exc.args).with_traceback(exc.__traceback__)
        except redis.RedisError as exc:
            raise UpstreamInternalError(*exc.args).with_traceback(exc.__traceback__)


class RedisConnection(CacheConnection):
    def __init__(self, pool: redis.ConnectionPool, **kwargs):
        self.redis = redis.Redis(connection_pool=pool, **kwargs)

    @property
    def status(self) -> CacheConnectionStatus:
        return (
            CacheConnectionStatus.CONNECTED
            if self.redis.connection is not None and self.redis.ping()
            else CacheConnectionStatus.CLOSED
        )

    def close(self) -> None:
        return self.redis.close()

    def exists(self, query: "AnyQuery") -> bool:
        return self.redis.exists(query.key) == 1

    def store(self, query: "AnyQuery", result: "Result[pl.DataFrame]") -> None:
        dfio = result.data.write_ipc(file=None, compression="lz4")
        try:
            self.redis.set(query.key, dfio.getvalue())
        except redis.ConnectionError as exc:
            raise UpstreamNotPrepared(*exc.args).with_traceback(exc.__traceback__)
        except redis.RedisError as exc:
            raise UpstreamInternalError(*exc.args).with_traceback(exc.__traceback__)

    def retrieve(self, query: "AnyQuery") -> Union["Result[pl.DataFrame]", None]:
        try:
            res: bytes = self.redis.get(query.key)  # type: ignore
        except redis.ConnectionError as exc:
            raise UpstreamNotPrepared(*exc.args).with_traceback(exc.__traceback__)
        except redis.RedisError as exc:
            raise UpstreamInternalError(*exc.args).with_traceback(exc.__traceback__)

        if res is None:
            return None

        return Result(data=pl.read_ipc(BytesIO(res)), columns=query.columns)

    def ping(self) -> bool:
        return self.redis.ping()  # type: ignore
