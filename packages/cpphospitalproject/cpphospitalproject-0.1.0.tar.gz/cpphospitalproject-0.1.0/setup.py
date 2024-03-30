from setuptools import setup, find_packages

setup(
    name='cpphospitalproject',  # Name of your package
    version='0.1.0',  # Version number
    author='hardik',  # Your name
    author_email='hardiknavadiya@gmail.com',  # Your email address
    description='Hospital Management Package',  # Short description
    long_description='A custom library for hospital management.',  # Long description (if any)
    long_description_content_type='text/markdown',  # Long description content type
    packages=find_packages(),  # Find all Python packages in the current directory
    classifiers=[  # Classifiers help categorize your package
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    install_requires=[],
)
