from setuptools import setup


readme = open("./README.md", "r")

setup(
    name = 'cesarmodulo',
    packages = ['cesarmodulo'],
    version = '0.1',
    description = 'Esta es la descripcion de mi paquete',
    long_description = readme.read(),
    long_description_content_type='text/markdown',
    author = 'Cesar Crespo',
    author_email= 'cesar2crespo@gmail.com',
    #github url
    url = 'https://github.com/Cesar-Crespo/cesarmodulo.git',
    keywords = ['testing', 'logging', 'example'],
    classifiers = [ ],
    license = 'MIT',
    include_package_data = True
)
