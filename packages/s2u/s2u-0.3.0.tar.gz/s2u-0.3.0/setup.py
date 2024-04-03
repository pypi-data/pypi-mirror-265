from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
    
setup(
    name='s2u',
    version='0.3.0',
    description='This is a kind of bridge that exchanges serial streams and UDP packets for xkit.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='chanmin.park',
    author_email='devcamp@gmail.com',
    url='https://github.com/planxstudio/xkit',
    install_requires=['click', 'python-dotenv', 'pyserial', 'genlib'],
    packages=find_packages(exclude=[]),
    keywords=['xkit', 'genlib'],
    python_requires='>=3.8',
    package_data={},
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            's2u = s2u.s2u:main',            
        ],
    },    
)
