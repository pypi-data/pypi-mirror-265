from setuptools import find_packages, setup

setup(
    name='sakebow-enhancer',
    version="0.2.2",
    description="enhance datasets(including segement and detect, endswith txt) with rotate, \
                 flip and adjustion with color and noise",
    keywords='enhance datasets',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Utilities',
    ],
    url='https://github.com/sakebow/enhance-image',
    author='sakebow',
    author_email='sakebowljx@gmail.com',
    python_requires='>=3.5',
    include_package_data=True,
    packages=find_packages(include=['datadealer.py', 'reinforce.py', 'transforms.py', 'validate.py',
                                    'sakebow-enhancer.py', 'sakebow-enhancer-cli.py',
                                    'default.yaml', 'LICENSE', 'README.md', 'requirements.txt']),
    install_requires=['numpy', 'opencv-python', 'tqdm', 'PyYAML', 'tabulate'],
    zip_safe=False)