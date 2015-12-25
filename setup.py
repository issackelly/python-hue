from setuptools import setup, find_packages

setup(
    version='0.1.2',
    name='python-hue',
    description='Python client for Philips Hue',
    license='MIT',
    author='Issac Kelly',
    author_email='issac.kelly@gmail.com',
    install_requires=['requests', 'ColorPy', 'numpy'],
    url='https://github.com/issackelly/python-hue',
    keywords=['phillips hue', 'client'],
    packages=find_packages()
)
