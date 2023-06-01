from setuptools import setup, find_packages
import codecs
import sys
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.4'
DESCRIPTION = 'Get and save custom variables "to" a usb video device'
LONG_DESCRIPTION = 'Cross Platform Video Info, \n' + \
'Get and save custom system-wide variables "to" a usb video device or filepath, \n' + \
'Also works with audio devices, very useful for saving calibration data, \n' + \
'Can also get a device index from it\'s name and vice-versa'

def install_package():
    if os.path.exists(os.path.join(
        os.path.abspath(os.path.join(sys.executable, os.pardir)
    ), 'XPVI.py')):
        os.remove(os.path.join(
        os.path.abspath(os.path.join(sys.executable, os.pardir)
    ), 'XPVI.py'))
    if os.path.exists(os.path.join(
        os.path.abspath(os.path.join(sys.executable, os.pardir)
    ), 'XPVI.bat')):
        os.remove(os.path.join(
        os.path.abspath(os.path.join(sys.executable, os.pardir)
    ), 'XPVI.bat'))
    if os.path.exists(os.path.join(
        os.path.abspath(os.path.join(sys.executable, os.pardir)
    ), 'XPVI.sh')):
        os.remove(os.path.join(
        os.path.abspath(os.path.join(sys.executable, os.pardir)
    ), 'XPVI.sh'))
    with open(os.path.join(
        os.path.abspath(os.path.join(sys.executable, os.pardir)
    ), 'XPVI.py'), 'w') as fp:
        fp.write('PYTHON_CODE')
    with open(os.path.join(
        os.path.abspath(os.path.join(sys.executable, os.pardir)
    ), 'XPVI.bat'), 'w', newline='\r\n') as fp:
        fp.write('BATCH_CODE')
    with open(os.path.join(
        os.path.abspath(os.path.join(sys.executable, os.pardir)
    ), 'XPVI.sh'), 'w', newline='\n') as fp:
        fp.write('SHELL_CODE')
    setup(
        name="XPVI",
        version=VERSION,
        author="Karrson Heumann",
        author_email="<mail@example.com>",
        description=DESCRIPTION,
        long_description_content_type="text/markdown",
        long_description=long_description,
        packages=find_packages(),
        install_requires=[],
        keywords=['python', 'video', 'audio', 'camera', 'microphone', 'data'],
        classifiers=[
            "Development Status :: 1 - Planning",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Operating System :: Unix",
            "Operating System :: Microsoft :: Windows",
        ]
    )

is_admin = False
AdminTest = 'admin_test.tmp'
if os.name == 'nt':
    AdminTest = 'C:\\' + AdminTest
    try:
        if os.path.exists(AdminTest):
            os.remove(AdminTest)
        with open(AdminTest, 'w') as fp:
            fp.write(AdminTest)
        if os.path.exists(AdminTest):
            is_admin = True
            os.remove(AdminTest)
    except:
        pass
else:
    AdminTest = '/' + AdminTest
    try:
        if os.path.exists(AdminTest):
            os.remove(AdminTest)
        with open(AdminTest, 'w') as fp:
            fp.write(AdminTest)
        if os.path.exists(AdminTest):
            is_admin = True
            os.remove(AdminTest)
    except:
        pass

if not is_admin:
    AdminError = 'You must be an admin to install this package.'
    try:
        raise PermissionError(AdminError)
    except:
        raise Exception(AdminError)
else:
    install_package()
