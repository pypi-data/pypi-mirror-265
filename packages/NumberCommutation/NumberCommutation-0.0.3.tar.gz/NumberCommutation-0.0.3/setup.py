from setuptools import setup

with open("README.md", "r", encoding='utf-8') as arq:
    readme = arq.read()

setup(name='NumberCommutation',
    version='0.0.3',
    license='MIT License',
    author='Pedro Cavalcante',
    long_description= readme,
    long_description_content_type="text/markdown",
    author_email='ph.cavalcante29@gmail.com',
    keywords=['Matemática Atuarial' , 'Números de comutação'],
    description='Um agrupamento de calculos atuariais',
    packages=['NumberCommutation'],
    install_requires=['pandas', 'numpy'],)