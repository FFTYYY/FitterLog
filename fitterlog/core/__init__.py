'''核心概念模块。这个模块提供名词、谓词、从句和值的定义。
'''

from .morphology import Noun , Predicate
from .semasiology import Value
from .syntax import Clause

__all__ = [
	Noun , Predicate , Value , Clause
]
