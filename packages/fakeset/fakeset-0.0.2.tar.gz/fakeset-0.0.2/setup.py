from setuptools import setup, find_packages

setup(
    name = 'fakeset',
    packages = find_packages(exclude=['examples']),
    version = '0.0.2',
    license='MIT',
    description = 'Fake Dataset',
    author = 'JiauZhang',
    author_email = 'jiauzhang@163.com',
    url = 'https://github.com/JiauZhang/fakeset',
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type = 'text/markdown',
    keywords = [
        'Deep Learning',
        'Fake Dataset',
        'Artificial Intelligence',
    ],
    install_requires=[
        'numpy>=1.19.5',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)