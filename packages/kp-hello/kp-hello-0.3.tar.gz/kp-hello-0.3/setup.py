from setuptools import setup, find_packages

setup(
    name='kp-hello',
    version='0.3',
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