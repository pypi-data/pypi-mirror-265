"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(

    name="migoapiclient",  # Required 项目名称
    version="1.0.1",  # Required 发布版本号
    description="用于米果内部请求获取数据",  # Optional 项目简单描述
    long_description='自定义项目，用来做内部请求使用',  # Optional 详细描述
    long_description_content_type="text/markdown",  # 内容类型
    url="https://github.com/pypa/migoapiclient",  # Optional github项目地址
    author="kira_lueng",  # Optional 作者
    author_email="2920167524@qq.com",  # Optional 作者邮箱
    classifiers=[  # Optional 分类器通过对项目进行分类来帮助用户找到项目, 以下除了python版本其他的 不需要改动

        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],

    keywords="migo",  # Optional 搜索关键字

    package_dir={"": "src"},  # Optional 手动指定包目录

    packages=find_packages(where="src"),  # Required

    python_requires=">=3.5, <4",  # python 版本要求

    install_requires=["requests"],  # Optional 第三方依赖库

)
