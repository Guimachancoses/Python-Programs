from setuptools import setup, find_packages
import py2exe

options = {
    'py2exe': {
        'bundle_files': 1,
        'compressed': True
    }
}

setup(
    console=[{r'C:\Users\SAMSUMG\OneDrive\Documentos\GitHub\-Python-Programs\3CX_Auto_Open': 'main.py'}],
    options=options,
    zipfile=None,
    name='3cx-app-launcher',
    version='1.0.0',
    description='Application to check and launch 3CX Desktop App automatically',
    author='Guilherme Machancoses',
    author_email='guilherme.machancoses@gmail.com',
    packages=find_packages(),
    install_requires=['psutil'],
    entry_points={
        'console_scripts': [
            '3cx-app-launcher = 3cx_app_launcher.main:main',
            '3cx-app-launcher-user = 3cx_app_launcher.main:main --username'
        ]
    }   
)
