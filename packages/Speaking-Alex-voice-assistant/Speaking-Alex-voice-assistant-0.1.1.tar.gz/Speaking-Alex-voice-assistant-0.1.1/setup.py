from setuptools import setup, find_packages

VERSION = '0.1.1'
DESCRIPTION = 'Assistant'

setup(
    name="Speaking-Alex-voice-assistant",
    version=VERSION,
    author="Ammar Yusri",
    author_email="amaryusri@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyjokes.jokes_es', 'speech_recognition', 'pyttsx3', 'pywhatkit', 'datetime', 'wikipedia'],
    keywords=['python', 'speech_recognition', 'voice assistant'],
)