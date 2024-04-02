from setuptools import setup, find_packages

setup(
    name='FastAPI-TemplateWizard',
    version='0.1.1',
    packages=find_packages(),
    url='https://github.com/pybalt/FastAPI-TemplateWizard',
    author='pybalt',
    author_email='96897286+pybalt@users.noreply.github.com',
    description='A CLI to generate FastAPI templates',
    install_requires=[
        'typer',
        'questionary'
    ],
    entry_points='''
        [console_scripts]
        fastcli=FastCLI.main:app
    '''
)
