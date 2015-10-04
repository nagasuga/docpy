from distutils.core import setup

setup(
    name='docpy',
    version='0.1.1',
    packages=['docpy'],
    install_requires=[
        'jinja2',
        'pyyaml',
    ],
    dependency_links=[],
    description='Python documentation generator using docstrings',
    author='Jeff Nagasuga',
    url='https://github.com/nagasuga/docpy.git',
    keywords=[],
    classifiers=[],
)
