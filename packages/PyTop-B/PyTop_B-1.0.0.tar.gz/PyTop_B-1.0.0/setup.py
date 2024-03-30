from setuptools import setup, find_packages

setup(
    name='PyTop_B',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'psutil'
    ],
    entry_points={
        'console_scripts': [
            'pytop = pytop.monitor:main'
        ]
    },
    author='Azaz Ahmed Lipu',
    author_email='lipuahmedazaz79@gmail.com',
    description='A Python-based system resource monitor as like Htop in Linux',
    license='MIT',
    keywords='system resource monitor curses htop linux pytop python',
    url='https://github.com/AzazAhmedLipu79/PyTop',
)
