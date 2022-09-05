import setuptools

VERSION = '1.0.0'
REQUIRES = ['crc16>=0.1.1']

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybuspro",
    version=VERSION,
    author="Audun Simonsen",
    author_email="audun.simonsen@gmail.com",
    description="An Asynchronous Library for the Buspro protocol",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eyesoft/pybuspro",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Topic :: System :: Hardware :: Hardware Drivers',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',
    install_requires=REQUIRES,
    keywords='hdl buspro home automation',
)
