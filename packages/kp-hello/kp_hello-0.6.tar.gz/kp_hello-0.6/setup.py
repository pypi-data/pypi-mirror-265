from setuptools import setup, find_packages

setup(
    name='kp_hello',
    version='0.6',
    packages=find_packages(),
    install_requires=[
        # Add dependencies here.
    ],
    entry_points={
        "console_scripts" : [
            "kp-hello = kp_hello:hello",
        ],
    },
)