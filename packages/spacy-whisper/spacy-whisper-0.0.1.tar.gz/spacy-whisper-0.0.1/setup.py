from setuptools import setup, find_packages

setup(
    name='spacy-whisper',
    version='0.0.1',
    author='Their Story',
    description='Integrate Whisper transcriptions with spaCy for advanced NLP tasks',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/theirstory/spacy-whisper',
    packages=find_packages(),
    install_requires=[
        'spacy>=3.0',
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic',
    ],
    keywords='NLP, spaCy, Whisper, transcription'
)
