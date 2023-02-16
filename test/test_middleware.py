import os
import sys
import shutil
from uliweb import manage

path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path)


def teardown():
    os.chdir('..')
    if os.path.exists('TestMiddleware'):
        shutil.rmtree('TestMiddleware', ignore_errors=True)


INI_MIDDLEWARE_SAME_ORDER = '''
[MIDDLEWARES]
auth = 'uliweb.contrib.auth.middle_auth.AuthMiddle', 500
csrf = 'uliweb.contrib.csrf.middleware.CSRFMiddleware', 500
'''


def test_middleware():
    """
    >>> if os.path.exists('TestMiddleware'):shutil.rmtree('TestMiddleware', ignore_errors=True)
    >>> manage.call('uliweb makeproject -y TestMiddleware')
    >>> os.chdir('TestMiddleware')
    >>> path = os.getcwd()
    >>> f = open("apps/settings.ini", "a").write(INI_MIDDLEWARE_SAME_ORDER)
    >>> app = manage.make_simple_application(project_dir=path)
    >>> print(type(app))
    <class 'uliweb.core.SimpleFrame.Dispatcher'>
    """
