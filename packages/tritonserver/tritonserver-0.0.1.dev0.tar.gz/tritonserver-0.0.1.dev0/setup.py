from setuptools import setup
from setuptools.command.install import install


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        raise RuntimeError(open('README.md').read())


setup(cmdclass={'install': PostInstallCommand})
