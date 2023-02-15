from setuptools import setup

setup(
    name="exrates",
    version="0.1.0",
    description="Exrates CLI",
    classifiers=["Programming Language :: Python :: 3.9"],
    install_requires=[
        "requests==2.28.2",
    ],
    extras_require=[
        "pytest"
    ],
    entry_points="""
    [console_scripts]
    exrates=exrates:main
    """,
    packages=["exrates"]
)
