
from setuptools import setup, find_packages

setup(
    name = 'Mensajes-sebasmi19',
    version = '6.0',
    description = 'Un paquete para saludar y despedir',
    long_description= open('README.md').read(),
    long_description_content_type='text/markdown',
    author = 'ZBIX',
    author_email= 'sebasmi1920@gmail.com',
    url= 'https://www.zbix.com',
    license_files= ['LICENSE'],
    packages = find_packages(),
    scripts =[],
    test_suite= 'tests',
    install_requires= [paquete.strip() 
                       for paquete in open('requirement.txt').readlines()],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python ',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities']
)

