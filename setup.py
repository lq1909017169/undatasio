from distutils.core import setup
from setuptools import find_packages

# with open("README.rst", "r") as f:
#     long_description = f.read()

with open("README.md", "r") as f:
    long_description = f.read()

setup(name='undatasio',                      # 包名
      version='0.1.7',                      # 版本号
      description='test pip upload',
      long_description=long_description,
      author='lily',
      author_email='1909017169@qq.com',
      url='',
      install_requires=["requests~=2.32.3", "requests_toolbelt==1.0.0"],	                # 依赖包会同时被安装
      license='MIT',
      python_requires=">=3.8",  # 项目依赖的 Python 版本
      packages=find_packages())
