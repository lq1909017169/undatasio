from distutils.core import setup
from setuptools import find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(name='undatasio',                      # 包名
      version='0.1.7',                      # 版本号
      description='test pip upload',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='lily',
      author_email='1909017169@qq.com',
      url='',
      install_requires=["requests~=2.32.3", "requests_toolbelt==1.0.0", "llama_index", "langchain_core"],	                # 依赖包会同时被安装
      license='MIT',
      python_requires=">=3.8",  # 项目依赖的 Python 版本
      packages=find_packages())
