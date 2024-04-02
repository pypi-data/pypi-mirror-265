from setuptools import setup

setup(
    name='sinc',
    version='0.0.0',
    packages=["sinc"],
    description="Reserved name for future use",
    author='Alireza Afzal Aghaei',
    author_email='alirezaafzalaghaei@gmail.com',
    url='https://github.com/alirezaafzalaghaei',
    python_needed='>=3.9',
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires=[
        'numpy',
        'scipy',
        'numba'
    ],
    license='BSD',
)
