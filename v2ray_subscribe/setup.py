from setuptools import setup, find_packages
import sys, os

version = "0.0.0.2"

setup(
    name="v2ray_subscribe",
    version=version,
    description="Grab and detect available over the wall nodes",
    long_description="""\
""",
    classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords="",
    author="Luoxin",
    author_email="luoxin.ttt@gmail.com",
    url="https://gitee.com/luoxinY/v2ray_subscribe",
    license="",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points="""
      # -*- Entry points: -*-
      """,
)
