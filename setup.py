from setuptools import setup

setup(name = 'ptchem',
      version = '0.2',
      description = 'Tools for Chemical file',
      url = 'https://github.com/zeldery/ptchem',
      author = 'Thien-Phuc Tu-Nguyen',
      licence = 'GNU',
      packages = ['ptchem'],
      install_requires = ['pandas'],
      include_package_data = True,
      zip_safe = False)
