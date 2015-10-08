try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='docpy',
    version='0.1.2',
    packages=['docpy'],
    install_requires=[
        'jinja2',
        'pyyaml',
    ],
    tests_require=[
        'pytest',
        'six',
    ],
    test_suite='py.test',
    dependency_links=[],
    description='Python documentation generator using docstrings',
    author='Jeff Nagasuga',
    url='https://github.com/nagasuga/docpy.git',
    keywords=[],
    classifiers=[],
)
