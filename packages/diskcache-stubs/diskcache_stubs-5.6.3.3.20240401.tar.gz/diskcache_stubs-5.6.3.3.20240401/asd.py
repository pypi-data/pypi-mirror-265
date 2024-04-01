from __future__ import annotations

import diskcache
import sqlite3
from diskcache.core import MODE_RAW, DEFAULT_SETTINGS
from diskcache.persistent import Deque, Index

a = diskcache.Cache()

disk = a.disk
b=disk.fetch(3, '', 123, True)
a.pull()
d = Deque([1,2,3, "Qwe"])
diskcache.Averager(a, 'asd')

b = a.get(1)
aaa = Index()
from diskcache import core

a = DEFAULT_SETTINGS['size_limit']