from setuptools import setup, find_packages
import pathlib

VERSION = '0.1.2'
DESCRIPTION = 'Assistant'
LONG_DESCRIPTION = 'A program that enables voice command functionality'

setup(
    name="Speaking-Alex-voice-assistant",
    version=VERSION,
    author="Ammar Yusri",
    author_email="amaryusri@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['pyjokes.jokes_es', 'speech_recognition', 'pyttsx3', 'pywhatkit', 'datetime', 'wikipedia'],
    keywords=['python', 'speech_recognition', 'voice assistant'],
)