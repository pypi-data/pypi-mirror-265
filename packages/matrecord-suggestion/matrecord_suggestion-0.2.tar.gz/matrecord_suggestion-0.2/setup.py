from setuptools import setup, find_packages

setup(
    name='matrecord_suggestion',
    version='0.2',
    packages=find_packages(),
    package_data={'matrecord_suggestion': ['autocorrect book.txt']},
    author='Nida Deshmukh',
    author_email='nidadeshmukh7@email.com',
    description='A Python package for providing word suggestions.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/Nida-Deshmukh123/matrecord_suggestion',
    install_requires=[
        'textdistance',
        'pandas'
    ],
    classifiers=[
        
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
