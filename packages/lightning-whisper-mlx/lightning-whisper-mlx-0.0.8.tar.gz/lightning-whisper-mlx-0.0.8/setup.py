from setuptools import setup, find_packages

setup(
    name='lightning-whisper-mlx',
    version='0.0.8',
    packages=find_packages(),
    install_requires=[
        'huggingface_hub',
        "mlx",
        "numba",
        "numpy",
        "torch",
        "tqdm",
        "more-itertools",
        "tiktoken==0.3.3",
        "scipy"
    ],
)