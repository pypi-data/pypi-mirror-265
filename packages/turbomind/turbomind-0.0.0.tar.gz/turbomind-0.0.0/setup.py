from setuptools import setup, find_packages

setup(
    name='turbomind',
    version='0.0.0',
    author='OpenMMLab',
    author_email='openmmlab@gmail.com',
    description='An accelerator of LLM inference',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
    ],
    python_requires='>=3.8',
)

