from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="voice-converter-pro",
    version="1.0.0",
    author="Harshit Pande",
    author_email="harshitpande938@gmail.com",
    description="Advanced Text-to-Speech and Speech-to-Text converter with modern GUI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/harshit001-2023/voice-converter-pro",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pyttsx3>=2.90",
        "SpeechRecognition>=3.10.0",
        "gTTS>=2.3.2",
        "pygame>=2.5.2",
        "pyaudio>=0.2.11",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "voice-converter=voice_converter:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
