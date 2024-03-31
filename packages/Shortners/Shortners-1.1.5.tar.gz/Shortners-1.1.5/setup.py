from setuptools import setup, find_packages

with open("README.md", "r") as o:
    long_description = o.read()

DATA01 = "clintonabrahamc@gmail.com"

DATA02 = ['Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules']

setup(
    name='Shortners',
    version='1.1.5',
    author='Clinton Abraham',
    author_email=DATA01,
    classifiers=DATA02,
    zip_safe=False,
    license='MIT',
    python_requires='~=3.7',
    packages=find_packages(),
    install_requires=['aiohttp'],
    description='Python url shortner',
    long_description=long_description,
    keywords=['url', 'shortner', 'telegram'],
    long_description_content_type="text/markdown",
    url='https://github.com/Clinton-Abraham/SHORTNER',)
