from setuptools import setup, find_packages

setup(
    name='optima-robotics',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'serial'
    ],
    author='TTH',
    author_email='trantrunghieu1497@gmail.com',
    description='A library for robotics.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/TrungHieuTDC/robotics-lib',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
