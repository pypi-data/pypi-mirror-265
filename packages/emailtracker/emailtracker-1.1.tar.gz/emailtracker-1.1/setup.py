from setuptools import setup, find_packages

setup(
    name='emailtracker',
    version='1.1',
    packages=find_packages(),
    install_requires=[
        'customtkinter',  # Example of a required package with a minimum version
        'CTkMessagebox',  # Example of a required package with an exact version
        'requests',     
    ],
    entry_points={
        'console_scripts': [
            'emailtracker = emailtracker.emailtracker:extract',
        ],
    },
    author='AKM Korishee Apurbo',
    author_email='bandinvisible8@gmail.com',
    description='A graphical email tracking tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/IMApurbo/emailtracker',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
