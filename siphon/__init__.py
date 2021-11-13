"""Top-level package for siphon."""

__author__ = """Mitchell Lisle"""
__email__ = 'm.lisle90@gmail.com'
__version__ = '0.4.0'


from siphon.database.mysql import AioMySQL, MySQLConfig  # noqa: F401
from siphon.database.postgres import (AioPostgres,  # noqa: F401
                                      PostgresConfig, Record)
from siphon.queue.aioqueue import CollectedError  # noqa: F401
from siphon.queue.aioqueue import AioQueue, TypedAioQueue, queuecollect
from siphon.queue.violations import (DiscardOnViolation, RaiseOnViolation,
                                     ViolationStrategy)
