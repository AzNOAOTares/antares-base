from setuptools import setup, find_packages

setup(
    name='Antares',
    version='1.0.0',
    description='Antares Project',
    author='Antares Team',
    author_email='antares@noao.edu',
    url='http://www.cs.arizona.edu/projects/tau/antares/',
#    packages=['antares',]
    packages=find_packages(),
    install_requires=[
        'flask',
        'numpy',
        'pandas',
        'paramiko',
        'pymysql',
        'pyyaml',
        'requests',
        'scipy',
        'gatspy',
        'george',
        'astropy'
    ],
)
