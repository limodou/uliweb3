import time, sys, os
path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path)
from uliweb import manage, functions

cdir = None


def setup():
    global cdir
    cdir = os.getcwd()


def teardown():
    import shutil
    if cdir:
        os.chdir(cdir)
    if os.path.exists('TestProject'):
        shutil.rmtree('TestProject', ignore_errors=True)


def test_file():
    """
    >>> manage.call('uliweb makeproject -y TestProject')
    >>> os.chdir('TestProject')
    >>> path = os.getcwd()
    >>> app = manage.make_simple_application(project_dir=path, include_apps=['uliweb.contrib.cache'])
    >>> cache = functions.get_cache()
    >>> cache.get('name', None)
    >>> def set_name():
    ...     return 'test'
    >>> cache.get('name', creator=set_name)
    'test'
    >>> cache.get('name')
    'test'
    >>> cache.get('hello', 'default')
    'default'
    >>> cache['test'] = 'ooo'
    >>> cache['test']
    'ooo'
    >>> del cache['test']
    >>> cache.setdefault('a', set_name)
    'test'
    >>> cache['a']
    'test'
    >>> cache.inc('count')
    1
    >>> cache.dec('count')
    0
    >>> cache.inc('count')
    1
    >>> cache.get('count')
    1
    >>> cache.set('count', 2)
    True
    >>> cache.inc('count', 2)
    4
    >>> teardown()
    """

def test_redis():
    """
    >>> manage.call('uliweb makeproject -y TestProject')
    >>> os.chdir('TestProject')
    >>> path = os.getcwd()
    >>> app = manage.make_simple_application(project_dir=path, include_apps=['uliweb.contrib.cache'])
    >>> cache = functions.get_cache(storage_type='redis', options={'connection_pool':{'host':'localhost', 'port':6379}})
    >>> cache.get('name', None)
    >>> def set_name():
    ...     return 'test'
    >>> cache.get('name', creator=set_name)
    'test'
    >>> cache.get('name')
    'test'
    >>> cache.get('hello', 'default')
    'default'
    >>> cache['test'] = 'ooo'
    >>> cache['test']
    'ooo'
    >>> del cache['test']
    >>> cache.setdefault('a', set_name)
    'test'
    >>> cache['a']
    'test'
    >>> cache.inc('count')
    1
    >>> cache.dec('count')
    0
    >>> cache.inc('count')
    1
    >>> cache.get('count')
    1
    >>> cache.set('count', 2)
    True
    >>> cache.inc('count', 2)
    4
    >>> cache.set('a', 1.0)
    True
    >>> cache.get('a')
    1.0
    >>> cache.delete('name')
    True
    >>> cache.delete('count')
    True
    >>> cache.delete('a')
    True
    >>> teardown()
    """
