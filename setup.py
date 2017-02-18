from setuptools import setup

setup(
    name='spectrum-console',
    packages=['spectrum_console'],
    version='0.5',
    author='mic159',

    install_requires=[
        'numpy>=1.11',
        'PyAudio>=0.2.8',
    ],

    entry_points={
        'console_scripts': [
            'spectrum-console=spectrum_console.main:run',
        ],
    },
)
