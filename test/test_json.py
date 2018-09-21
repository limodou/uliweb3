#coding=utf8
from __future__ import print_function, absolute_import, unicode_literals
from uliweb.utils._compat import u

def test():
    """
    >>> from uliweb import json_dumps
    >>> print(json_dumps({'a':'中文'}))
    {"a":"中文"}
    >>> print(json_dumps({'a':'中文'}, unicode=True))
    {"a":"\u4e2d\u6587"}
    >>> import datetime
    >>> print(json_dumps({1:1}))
    {"1":1}
    >>> print(json_dumps([1,2,3]))
    [1,2,3]
    >>> print(json_dumps((1,2,3)))
    [1,2,3]
    >>> print(json_dumps(12.2))
    12.2
    >>> import decimal
    >>> print(json_dumps(decimal.Decimal("12.3")))
    "12.3"
    >>> print(json_dumps(datetime.datetime(2011, 11, 8)))
    "2011-11-08 00:00:00"
    >>> print(json_dumps(['中文', u('中文', 'utf-8')]))
    ["中文","中文"]
    >>> from uliweb.core.html import Builder
    >>> b = Builder('head', 'body', 'end')
    >>> b.head << '<h1>'
    >>> b.body << 'test'
    >>> b.end << '</h1>'
    >>> print(str(b))
    <h1>
    test
    </h1>
    <BLANKLINE>
    """

from uliweb import json_dumps
print(json_dumps({'a':'中文'}, unicode=True))