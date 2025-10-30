from setuptools import setup, find_packages

setup(
    name='ai_music_gen',
    version='0.1.0',
    description='AI Music Generation Library',
    author='True North Audio',
    packages=find_packages(),
    install_requires=[
        'mido',
        'psutil',
    ],
)
