from setuptools import setup
from setuptools.command.install import install

class PostInstallCommand(install):
    def run(self):
        import os
        os.system("echo 'This is just a test' > /tmp/test00013.txt")
        install.run(self)

setup(
    cmdclass={
        'install': PostInstallCommand,
    },
    name='otc-metadata',
    version='0.0.1',
    author='',
    author_email='',
    description='A short description of your package',
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    ]
)
