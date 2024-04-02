from setuptools import setup, find_packages

setup(
    name='suggestions_matrecord',
    version='0.1',
    packages=find_packages(),
    package_data={'suggestions_matrecord': ['autocorrect book.txt']},
    author='Nida Deshmukh',
    author_email='nidadeshmukh7@email.com',
    description='A Python package for providing word suggestions.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/Nida-Deshmukh123/suggestions_matrecord',
    install_requires=[
        'textdistance',
        'pandas'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
