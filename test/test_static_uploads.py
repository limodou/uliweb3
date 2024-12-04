from uliweb import manage
from uliweb.utils.test import client_from_application
import os, sys, shutil

def test_static_uploads():
    """
    >>> path = os.path.dirname(os.path.dirname(__file__))
    >>> sys.path.insert(0, path)
    >>> if os.path.exists('TestProject'):shutil.rmtree('TestProject', ignore_errors=True)
    >>> manage.call('uliweb makeproject -y TestProject')
    >>> os.chdir('TestProject')
    >>> path = os.getcwd()
    >>> app = manage.make_simple_application(project_dir=path, include_apps=['uliweb.contrib.upload','uliweb.contrib.staticfiles'])
    >>> c = client_from_application(app)
    >>> c.test_url('/static/..%5Csetup.py', ok_test=403)
    Testing /static/..%5Csetup.py...OK
    True
    >>> c.test_url('/uploads/..%5C..%5setup.py', ok_test=403)
    Testing /uploads/..%5C..%5setup.py...OK
    True
    """


# if __name__ == '__main__':
#     path = os.path.dirname(os.path.dirname(__file__))
#     sys.path.insert(0, path)
#     if os.path.exists('TestProject'):shutil.rmtree('TestProject', ignore_errors=True)
#     manage.call('uliweb makeproject -y TestProject')
#     os.chdir('TestProject')
#     print (os.getcwd())
#     path = os.getcwd()
#     app = manage.make_simple_application(project_dir=path, include_apps=['uliweb.contrib.upload','uliweb.contrib.staticfiles'])
#     c = client_from_application(app)
#     c.test_url('/static/..%5Csetup.py', ok_test=403)