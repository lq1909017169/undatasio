# undatasio
.. UnDatasIO Python SDK Documentation

Welcome to the UnDatasIO Python SDK!
=================================

UnDatasIO provides powerful file parsing capabilities, allowing you to easily extract data from various file types. This Python SDK simplifies interaction with the UnDatasIO platform, enabling you to focus on data analysis and application development without worrying about the complexities of low-level API calls.

Key Features
------------

* **File Upload:** Easily upload your files to the UnDatasIO platform, supporting a variety of common file formats.
* **Automatic Parsing:** UnDatasIO automatically identifies file types and parses them to extract key information.
* **Result Download:** Download parsing results, providing a download link that includes the parsed PDF-generated MD file and its images.
* **Version Management:** Easily manage different versions of parsing results.
* **Result Query:** Flexibly query specific types of data based on your needs.

Installation
------------

You can easily install the UnDatasIO Python SDK using `pip`:

```bash
pip install undatasio
```
Quick Start
------------

Let's illustrate how to use the UnDatasIO Python SDK with a simple example:

```python
from undatasio import UnDatasIO

# 1. Initialize the UnDatasIO client
client = UnDatasIO(token='your API key', task_name='your task name')

# 2. Upload files
upload_response = client.upload(file_dir_path='./example_files')
if upload_response['code'] == 200:
    print("File upload successful!")
else:
    print(f"File upload failed: {upload_response['msg']}")

# 3. View all uploaded files
upload_filename_response = client.show_upload()
if upload_filename_response['code'] == 200:
    print(upload_filename_response.json())
else:
    print(f"File upload failed: {upload_filename_response['msg']}")

# 4. Parse files
parse_response = client.parser(file_name_list=['example_file.pdf'])
if parse_response['code'] == 200:
    print("File parsing successful")
else:
    print(f"File parsing request failed: {parse_response['msg']}")

# 5. View historical parsing results
parse_filename_response = client.show_version()
if parse_filename_response['code'] == 200:
    print(parse_filename_response.json())
else:
    print(f"File upload failed: {parse_filename_response['msg']}")


# 6. View parsing results (assuming you know the version number is 'v1' and want to get the title and table information in the parsing results)
results = client.get_result_type(type_info=['title', 'table'], file_name='example_file.pdf', version='v1')
if results['code'] == 200:
    print(f"Parsing results: {results.json()}")
else:
    print(f"Failed to get parsing results: {results['msg']}")
```
API Reference
------------

The UnDatasIO Python SDK provides the following methods:

* **``UnDatasIO(token: str, task_name: str = "")``**

    - Initializes the UnDatasIO client.
        -  ``token (str)``: Your API key, obtained from the UnDatasIO platform.
        -  ``task_name (str, optional)``: The name you specify for this task, defaults to the system-generated default task.

* **``upload(self, file_dir_path: str) -> Dict``**

    - Uploads files from the specified directory.
        -  ``file_dir_path (str)``: The path to the directory containing the files to upload.
        - Returns: ``Dict`` - A dictionary containing the server response, for example: ``{'code': 200, 'msg': 'success'}``

* **``parser(self, file_name_list: List) -> Dict``**

    - Submits a parsing request to parse the specified files.
        -  ``file_name_list (List)``: A list of file names to parse, for example: ``['file1.pdf', 'file2.pdf']``
        - Returns: ``Dict`` - A dictionary containing the server response.

* **``download(self, version: str) -> Dict``**

    - Downloads the parsing results for the specified version.
        -  ``version (str)``: The version number to download.
        - Returns: ``Dict`` - A dictionary containing the server response.

* **``show_version(self) -> Dict``**

    - Retrieves available version information for the current task.
        - Returns: ``Dict`` - A dictionary containing the server response, including version information.

* **``show_upload(self) -> Dict``**

    - Retrieves the list of files uploaded for the current task.
        - Returns: ``Dict`` - A dictionary containing the server response, including information about the uploaded files.

* **``get_result_type(self, type_info: List, file_name: str, version: str) -> Dict``**

    - Gets specific types of parsing results from the specified file.
        -  ``type_info (List)``: A list of result types to retrieve, for example: ``['title', 'table', 'text', 'image', 'interline_equation']``
        -  ``file_name (str)``: The target file name.
        -  ``version (str)``: The target version number.
        - Returns: ``Dict`` - A dictionary containing the server response, including the parsed result data.

Error Handling
------------

All methods return a dictionary containing the server's response information. Be sure to check the value of the 'code' field:

- `code` of 200 indicates a successful request.
- `code` other than 200 indicates a failed request, and you can view the `msg` field for detailed error information.

Contact Us
------------
