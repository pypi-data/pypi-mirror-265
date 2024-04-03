from setuptools import setup, find_packages

setup(
    name='sajjad',
    version='2.1',
    packages=find_packages(),
    description='Sajjad developer creatd this library',
    author='sajjad seyedi',
    author_email='sajjad.seyedi.88@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=[
        'colorama==0.4.6',
    ],
)
