import time, sys
sys.path.insert(0, '../uliweb/lib')
from uliweb import expose
from uliweb.core import rules

def test_1():
    """
    >>> def view():pass
    >>> f = expose('!/')(view)
    >>> rules.merge_rules()
    [('test_url', 'test_url.view', '/', {})]
    >>> f = expose('/hello')(view)
    >>> rules.merge_rules()
    [('test_url', 'test_url.view', '/', {}), ('test_url', 'test_url.view', '/hello', {})]
    >>> @expose('/test')
    ... class TestView(object):
    ...     @expose('')
    ...     def index(self):
    ...         return {}
    ... 
    ...     @expose('!/ttt')
    ...     def ttt(self):
    ...         return {}
    ... 
    ...     @expose('/print')
    ...     def pnt(self):
    ...         return {}
    >>> rules.merge_rules()
    [('test_url', 'test_url.view', '/', {}), ('test_url', 'test_url.view', '/hello', {}), ('test_url', 'test_url.TestView.index', '/test', {}), ('test_url', 'test_url.TestView.pnt', '/print', {}), ('test_url', 'test_url.TestView.ttt', '/ttt', {})]
    """