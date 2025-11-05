from setuptools import setup, find_packages

setup(
    name='distancias-googlemaps',
    version='0.1.0',
    description='Calcula a distância entre pares de coordenadas em uma planilha usando a API do Google Maps',
    packages=find_packages(),
    install_requires=[
        'googlemaps==4.5.3',
        'pandas==1.3.4'
    ],
    entry_points={
        'console_scripts': [
            'distancias=distancias:main'
        ]
    }
)
