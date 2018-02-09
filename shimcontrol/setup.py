"""
Instala o shimcontrol
"""


from setuptools import setup

import shimcontrol

setup(
    name='shimcontrol',
    version=shimcontrol.__version__,
    description='Interact with the shimming subsystem',
    install_requires=[
        'spidev < 3.2',
        'gpiozero < 1.3',
        'RPi.GPIO < 0.7',
        'tabulate < 0.8',
    ],
    entry_points={
        'console_scripts': [
            'shimcontrol = shimcontrol.cli:main'
        ],
    },
)
