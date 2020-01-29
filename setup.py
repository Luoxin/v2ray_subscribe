from setuptools import setup, find_packages

setup(
    name="v2ray_subscribe",  # 包名字
    version="0.0.0.2",  # 包版本
    description="Grab and detect available over the wall nodes",  # 简单描述
    author="Luoxin",  # 作者
    author_email="luoxin.ttt@gmail.com",  # 作者邮箱
    url="https://gitee.com/luoxinY/v2ray_subscribe",  # 包的主页
    packages=find_packages(
        exclude=["ez_setup", "examples", "tests"], install_requires=["requests"],
    ),
)
