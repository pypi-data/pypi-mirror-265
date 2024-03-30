from setuptools import setup, find_packages

setup(
    name='chromastone', 
    version='0.1.1',
    author='Tarmica Chiwara',  
    author_email='lilskyforever@gmail.com',  
    description='A Python application for powering other python applications to send SMS messages globally with number validation and restrictions',
    long_description=open('readme.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/lordskyzw/chromastone', 
    packages=find_packages(),
    install_requires=[
        'requests', 
        'pydantic',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
