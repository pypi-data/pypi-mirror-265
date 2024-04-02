from setuptools import setup, find_packages

setup(
    name='lightning-whisper-mlx',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'huggingface_hub',
        "mlx>=0.8",
        "numba",
        "numpy",
        "torch",
        "tqdm",
        "more-itertools",
        "tiktoken==0.3.3",
        "scipy"
    ],
)