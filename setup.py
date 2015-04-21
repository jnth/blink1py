from setuptools import setup

setup(
    name='blink1py',
    url='https://github.com/TronPaul/blink1py',
    version='0.1.0',
    author='Mark McGuire',
    author_email='mark.b.mcg@gmail.com',
    packages=['blink1py'],
    license='Apache2',
    description='blink(1) library wrapper',
    long_description=open('README.rst').read(),
    include_package_data=True,
    package_data={'blink1py': ['blink1py/blink1-lib.dll']}
)
