**[English](README.md), [中文](README_ZH.md).**

# UnDatasIO Python SDK 文档

<p align="center">
  <a href="https://undatas.io">
    <img src="content/undatasio.png" width="100%" alt="UnDatasIO" />
  </a>
</p>

[![License](https://img.shields.io/npm/l/mithril.svg)](https://github.com/MithrilJS/mithril.js/blob/main/LICENSE) &nbsp;
[![Supported Python versions](https://shields.mitmproxy.org/pypi/pyversions/mitmproxy.svg)](https://pypi.python.org/pypi/mitmproxy)

💫欢迎使用 UnDatasIO Python SDK!
=================================

**官方地址:** https://undatas.io/

UnDatasIO  为您提供强大的文件解析能力，让您轻松提取各种类型文件中的数据。此 Python SDK 简化了与  UnDatasIO 平台的交互，使您能够专注于数据分析和应用开发，而无需担心底层 API 调用的复杂性。

## 主要功能
------------

* **文件上传:**  轻松上传您的文件到 UnDatasIO 平台，支持各种常见文件格式。
* **自动解析:**  UnDatasIO  会自动识别文件类型并进行解析。
* **结果下载:**  下载解析结果，提供一个下载链接，其中包含解析的pdf生成的md文件以及其中的image图片。
* **版本查看:**  方便地管理不同版本的解析结果。
* **结果查询:**  根据您的需求，灵活查询特定类型的数据。

## 安装
------------

🤖使用  `pip`  可以轻松安装 UnDatasIO Python SDK：

```bash
pip install undatasio
```

## 快速入门
------------

🥇让我们用一个简单的例子来说明如何使用 UnDatasIO Python SDK:

```python
from undatasio import UnDatasIO

# 1. 初始化 UnDatasIO 客户端
client = UnDatasIO(token='您的 API 密钥', task_name='您的任务名称')

# 2. 上传文件
upload_response = client.upload(file_dir_path='./示例文件')
if upload_response['code'] == 200:
    print("文件上传成功！")
else:
    print(f"文件上传失败: {upload_response['msg']}")

# 3. 查看上传的全部文件
upload_filename_response = client.show_upload()
if upload_filename_response['code'] == 200:
    print(upload_filename_response.json())
else:
    print(f"文件上传失败: {upload_filename_response['msg']}")

# 4. 解析文件
parse_response = client.parser(file_name_list=['示例文件.pdf'], lang='en', parameter='fast')
if parse_response['code'] == 200:
    print("文件解析成功")
else:
    print(f"文件解析请求失败: {parse_response['msg']}")

# 5. 查看历史解析结果
parse_filename_response = client.show_version()
if parse_filename_response['code'] == 200:
    print(parse_filename_response.json())
else:
    print(f"文件上传失败: {parse_filename_response['msg']}")


# 6. 查看解析结果 (假设您已知版本号为 'v1'，希望得到解析结果中的title以及table信息)
results = client.get_result_type(type_info=['title', 'table'], file_name='示例文件.pdf', version='v1')
if results['code'] == 200:
    print(f"解析结果: {results.json()}")
else:
    print(f"获取解析结果失败: {results['msg']}")
```

## API 参考
------------

🔥UnDatasIO Python SDK 提供了以下方法:

* **``UnDatasIO(token: str, task_name: str = "")``**

    - 🛠️初始化 UnDatasIO 客户端。
        -  ``token (str)``: 您的 API 密钥，在 UnDatasIO 平台获取。
        -  ``task_name (str, 可选)``:  您为此次任务指定的名称，默认为系统生成的默认任务。

* **``upload(self, file_dir_path: str) -> Dict``**

    - 🔄上传指定目录下的文件。
        -  ``file_dir_path (str)``:  包含要上传文件的目录的路径。
        - 返回值:  ``Dict`` - 包含服务器响应的字典，例如： ``{'code': 200, 'msg': 'success'}``

* **``parser(self, lang: str, parameter: str, file_name_list: List) -> Dict``**

    -  🌟提交解析请求，解析指定的文件。
        - ``lang(str)``: 输入解析语言的简称
        - ``parameter(str)``: 填写解析的参数
        - ``file_name_list (List)``:  要解析的文件名列表，例如： ``['file1.pdf', 'file2.pdf']``
        - 返回值: ``Dict`` - 包含服务器响应的字典。

* **``download(self, version: str) -> Dict``**

    - 👨‍💻下载指定版本的解析结果。
        -  ``version (str)``: 要下载的版本号。
        - 返回值: ``Dict`` - 包含服务器响应的字典。

* **``show_version(self) -> Dict``**

    - 📈获取当前任务可用的版本信息。
        - 返回值:  ``Dict`` - 包含服务器响应的字典，其中包含版本信息。

* **``show_upload(self) -> Dict``**

    - 🌍获取当前任务已上传的文件列表。
        - 返回值:  ``Dict`` - 包含服务器响应的字典，其中包含已上传文件的信息。

* **``get_result_type(self, type_info: List, file_name: str, version: str) -> Dict``**

    - 📊获取指定文件中特定类型的解析结果。
        -  ``type_info (List)``:  要获取的结果类型列表，例如： ``['title', 'table', 'text', 'image', 'interline_equation']``
        -  ``file_name (str)``:  目标文件名。
        -  ``version (str)``:  目标版本号。
        - 返回值:  ``Dict`` - 包含服务器响应的字典，其中包含解析结果数据。

## Colab示例文件。
------------

📄下面的所有的ipynb文件都是在colab的环境中运行的，点击之后可以直接在colab中运行。

- [complex_table_to_json.ipynb](https://colab.research.google.com/drive/1QSQJ7P21vSzRK14rMZ7lJdVkf1dHzL2P?usp=sharing)


## 错误处理
------------

📚所有方法都会返回一个字典，其中包含服务器的响应信息。请务必检查 'code' 字段的值：

-  `code` 为 200 表示请求成功。
-  `code`  不为 200  表示请求失败，您可以查看 `msg` 字段获取详细的错误信息。

## 联系我们
------------
