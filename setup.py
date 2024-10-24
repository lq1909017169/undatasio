from distutils.core import setup
from setuptools import find_packages
import pathlib
import re
import os

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

package = 'undatasio'


def get_version():
    """
    从包的 __init__.py 文件中提取版本号.

    参数:
      package: 包的名称.

    返回:
      版本号字符串, 如果找不到则返回 '0.0.0'.
    """
    init_py = os.path.join(package, '__init__.py')
    with open(init_py, 'r') as f:
        content = f.read()

    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M)
    if version_match:
        return version_match.group(1)
    else:
        raise RuntimeError(f"无法在 '{init_py}' 中找到版本号")


setup(name=package,
      version=get_version(),
      description='python sdk for the undatasio platform',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='1909017169',
      author_email='1909017169@qq.com',
      url='',
      install_requires=[
          "requests~=2.32.3",
          "requests_toolbelt==1.0.0",
          "llama_index",
          "langchain_core",
          "pandas"
      ],
      license='MIT',
      python_requires=">=3.10",
      packages=find_packages()
      )
