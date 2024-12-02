# How to test it?
# easy_install nose
# cd test
# nosetests test_manage.py

import os


class TestMakeProject:
    def setup(self):
        import shutil
        if os.path.exists('maketest'):
            print("remove maketest when setup")
            shutil.rmtree('maketest', ignore_errors=True)
        print('setup')
            
    def teardown(self):
        import shutil
        if os.path.exists('maketest'):
            print("remove maketest when teardown")
            shutil.rmtree('maketest', ignore_errors=True)
        print('teardown')

    def test_makeproject(self):
        from uliweb import manage

        manage.call('uliweb makeproject -y maketest')
        assert os.path.exists('maketest')
        
    def test_makeapp(self):
        from uliweb import manage
        
        cdir = os.getcwd()
        manage.call('uliweb makeproject -y maketest')
        os.chdir('maketest')
        manage.call('uliweb makeapp Hello')
        os.chdir(cdir)
        assert os.path.exists('maketest/apps/Hello')
