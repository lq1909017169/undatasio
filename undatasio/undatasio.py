import time

from requests_toolbelt.multipart.encoder import MultipartEncoder
from langchain_core.documents import Document as lcDocument
from langchain_text_splitters import CharacterTextSplitter
from llama_index.core.schema import Document
from pydantic import BaseModel
from typing import List, Dict
from typing import Callable
import pandas as pd
import requests
import os
import json

from undatasio.utils import DictField


class Response:

    def __init__(self, code: int | None = None, msg: str | None = None,
                 data: List | None | Dict | str | pd.DataFrame = None):
        self.code = code
        self.msg = msg
        self.data = data


# class Response(BaseModel):
#     code: int | None = None
#     msg: str | None = None
#     data: List | None | Dict | str | pd.DataFrame = None


class UnDatasIO:

    def __init__(self, token: str, task_name: str = ""):
        self.token = token
        self.task_name = task_name
        self.base_url = 'https://backend.undatas.io/api/api'
        self.allowed_extensions = {'.pdf', '.png', '.jpg', '.pptx', '.ppt', '.doc', '.docx'}

    def upload(self, file_dir_path: str) -> Response:
        """
        Upload a single file or all files in a specified folder.

        :param file_dir_path: Path to a file or folder
        :return: Response object
        """
        files_to_upload = []

        # Check if the path is a file or a folder
        if os.path.isfile(file_dir_path):
            # Single file
            if self._is_file_allowed(file_dir_path):
                files_to_upload.append(file_dir_path)
        elif os.path.isdir(file_dir_path):
            # Folder
            for file_name in os.listdir(file_dir_path):
                file_path = os.path.join(file_dir_path, file_name)
                if os.path.isfile(file_path) and self._is_file_allowed(file_path):
                    files_to_upload.append(file_path)
        else:
            return Response(code=403, msg="Invalid path: must be a file or folder")

        if not files_to_upload:
            return Response(code=403, msg="No valid files to upload")

        # Upload files
        uploaded_files = []
        for file_path in files_to_upload:
            file_name = os.path.basename(file_path)
            with open(file_path, "rb") as file:
                fields = {
                    "user_id": self.token,
                    "task_name": self.task_name,
                    "file": (file_name, file, "application/octet-stream"),
                }
                m = MultipartEncoder(fields=fields)
                headers = {"Content-Type": m.content_type}
                response = requests.post(f"{self.base_url}/upload", data=m, headers=headers)

                if response.status_code != 200:
                    return Response(code=403, msg=f"Failed to upload {file_name}: response status code is not 200")
                uploaded_files.append(file_name)

        return Response(code=200, msg="Upload successful", data=uploaded_files)

    def _is_file_allowed(self, file_path: str) -> bool:
        """
        Check if the file extension is allowed.

        :param file_path: Path to the file
        :return: True if the file is allowed, False otherwise
        """
        _, ext = os.path.splitext(file_path)
        return ext.lower() in self.allowed_extensions

    # def upload(self, file_dir_path: str) -> Response:
    #     """
    #     :param file_dir_path: Upload specified folder
    #     :return:
    #     """
    #     files = []
    #     for file_path in os.listdir(file_dir_path):
    #         file_read_path = os.path.join(file_dir_path, file_path)
    #         if file_path.endswith(".pdf") and os.path.isfile(file_read_path):
    #             files.append(file_path)
    #             with open(file_read_path, "rb") as file:
    #                 fields = {
    #                     "user_id": self.token,
    #                     "task_name": self.task_name,
    #                     "file": (file_path, file, "application/octet-stream"),
    #                 }
    #                 m = MultipartEncoder(fields=fields)
    #
    #                 # 发送 POST 请求
    #                 headers = {"Content-Type": m.content_type}
    #                 response = requests.post(
    #                     f"{self.base_url}/upload", data=m, headers=headers
    #                 )
    #                 if response.status_code == 200:
    #                     Base_response = Response(**response.json())
    #                     return Base_response
    #                 else:
    #                     return Response(code=403, msg='response status code is not 200')
    #     return Response(code=200, msg="upload success", data=files)

    def parser(self, lang: str, parameter: str, file_name_list: List) -> Response:
        """
        :param lang: The abbreviation for input parsing language[en, ch, korean, japan, chinese_cht]
        :param parameter: Fill in the parsing parameters
        :param file_name_list: List of parsed file names
        :return:
        """
        API_ENDPOINT = f"{self.base_url}/task_return_list"
        data = {
            "user_id": self.token,
            "task_name": self.task_name,
            "fileName": file_name_list,
            "parameter": parameter,
            "lang": lang,
        }

        try:
            response = requests.post(API_ENDPOINT, data=data)
            if response.status_code == 200:
                Base_response = Response(**response.json())
                return Base_response
            else:
                return Response(code=403, msg='response status code is not 200')
        except requests.exceptions.RequestException as e:
            return Response(code=403, msg=e)

    def download(self, version: str) -> Response:
        """
        :param version: Download the specified version
        :return:
        """
        API_ENDPOINT = f"{self.base_url}/download"
        data = {
            "user_id": self.token,
            "task_name": self.task_name,
            "version": version,
        }

        try:
            response = requests.post(API_ENDPOINT, data=data)
            if response.status_code == 200:
                Base_response = Response(**response.json())
                return Base_response
            else:
                return Response(code=403, msg='response status code is not 200')
        except requests.exceptions.RequestException as e:
            return Response(code=403, msg=e)

    def show_version(self) -> Response:
        """
        :return:
        """
        API_ENDPOINT = f"{self.base_url}/version_info"
        data = {"user_id": self.token, "task_name": self.task_name}

        try:
            response = requests.post(API_ENDPOINT, data=data)
            if response.status_code == 200:
                Base_response = Response(**response.json())
                if Base_response.code != 200:
                    return Base_response
                else:
                    Base_response.data = pd.DataFrame.from_records(Base_response.data)
                    return Base_response
            else:
                return Response(code=403, msg='response status code is not 200')
        except requests.exceptions.RequestException as e:
            return Response(code=403, msg=e)

    def show_upload(self) -> Response:
        """
        :return:
        """
        API_ENDPOINT = f"{self.base_url}/view_upload_file"
        data = {"user_id": self.token, "task_name": self.task_name}

        try:
            response = requests.post(API_ENDPOINT, data=data)
            if response.status_code == 200:
                Base_response = Response(**response.json())
                return Base_response
            else:
                return Response(code=403, msg='response status code is not 200')
        except requests.exceptions.RequestException as e:
            return Response(code=403, msg=e)

    def get_result_type(
            self, type_info: List, file_name: str, version: str
    ):
        """
        :param type_info: Please select from title, table, text, image, interline_equation
        :param file_name: file name
        :param version: version
        :return:
        """
        API_ENDPOINT = f"{self.base_url}/get_type_info"
        data = {
            "user_id": self.token,
            "type_info": type_info,
            "file_name": file_name,
            "version": version,
            "task_name": self.task_name,
        }
        try:
            response = requests.post(API_ENDPOINT, data=data)
            if response.status_code == 200:
                Base_response = Response(**response.json())
                return Base_response
            else:
                return Response(code=403, msg='response status code is not 200')
        except requests.exceptions.RequestException as e:
            return Response(code=403, msg=e)

    def get_result_to_files(
            self, file_name_list: List, version: str
    ) -> Response:
        """
        :param file_name_list: file names
        :param version: version
        :return: List[str]
        """
        API_ENDPOINT = f"{self.base_url}/md_url"
        data = {
            "user_id": self.token,
            "file_name_list": file_name_list,
            "version": version,
            "task_name": self.task_name,
        }
        try:
            response = requests.post(API_ENDPOINT, data=data)
            if response.status_code == 200:
                Base_response = Response(**response.json())
                return Base_response
            else:
                return Response(code=403, msg='response status code is not 200')
        except requests.exceptions.RequestException as e:
            return Response(code=403, msg=e)

    def get_structured_data(self, version, file_name, chunk_size, chunk_overlap, field_list):

        field_list_data = []

        def analysis_to_json(data_list, fields):
            for field in fields:
                if not isinstance(field, DictField):
                    data = {
                        'name': field.name,
                        'rule': field.rule,
                        'attribute': field.attribute
                    }
                    data_list.append(data)
                else:
                    data = {
                        'name': field.name,
                        'rule': field.rule,
                        'attribute': field.attribute,
                        'keys': []
                    }
                    data_list.append(data)
                    analysis_to_json(data['keys'], field.keys)

        analysis_to_json(field_list_data, field_list)

        API_ENDPOINT = f"{self.base_url}/return_json"
        data = {
            "user_id": self.token,
            "version": version,
            "task_name": self.task_name,
            "file_name": file_name,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "field_list_data": json.dumps(field_list_data)
        }
        try:
            response = requests.post(API_ENDPOINT, data=data)
            if response.status_code == 200:
                Base_response = Response(**response.json())
                return Base_response
            else:
                return Response(code=403, msg='response status code is not 200')
        except requests.exceptions.RequestException as e:
            return Response(code=403, msg=e)

    def new_parser(self, file_name_list: List) -> Response:
        """
        :param file_name_list: List of parsed file names
        :return:
        """
        API_ENDPOINT_parser = f"{self.base_url}/return_parser_pdf"
        API_ENDPOINT_download = f"{self.base_url}/download_parser_pdf"
        API_ENDPOINT_version = f"{self.base_url}/get_version_parser"
        parser_data = {
            "user_id": self.token,
            "task_name": self.task_name,
            "fileName": file_name_list,
        }
        version_data = {
            "user_id": self.token,
            "task_name": self.task_name
        }

        res_version = requests.post(API_ENDPOINT_version, data=version_data)
        version = res_version.json()['data']['version']

        try:
            requests.post(API_ENDPOINT_parser, data=parser_data)
        except:
            pass
        while True:
            time.sleep(30)
            download_data = {
                "user_id": self.token,
                "task_name": self.task_name,
                "version": version
            }
            response = requests.post(API_ENDPOINT_download, data=download_data)
            if response.json()['code'] == 200:
                Base_response = Response(**response.json())
                return Base_response
            else:
                print(response.json()['code'])
                continue
                # return Response(code=403, msg='response status code is not 200')

    def get_result_to_langchain_document(
            self, type_info: List, file_name: str, version: str
    ) -> lcDocument:
        """
        :param type_info: Please select from title, table, text, image, interline_equation
        :param file_name: file name
        :param version: version
        :return: langchain_core.Document
        """
        result = self.get_result_type(type_info, file_name, version).data
        return lcDocument(
            page_content=result,
            metadata={
                "source": f"{self.task_name}_{version}_{file_name}_[{','.join(type_info)}]"
            },
        )

    def get_result_to_llama_index_document(
            self, type_info: List, file_name: str, version: str
    ) -> Document:
        """
        :param type_info: Please select from title, table, text, image, interline_equation
        :param file_name: file name
        :param version: version
        :return: langchain_core.Document
        """
        result = self.get_result_type(type_info, file_name, version).data
        return Document(
            text=result,
            metadata={
                "source": f"{self.task_name}_{version}_{file_name}_[{','.join(type_info)}]"
            },
        )

    def complex_table_parse(self, file_path):
        """
        :param file_path: file local path
        :return
        """
        url = 'http://3.19.69.227:8001/upload_parser'
        files = {
            "token": self.token,
            "file": open(file_path, 'rb')
        }
        try:
            response = requests.post(url, files=files)
            print(response.text)
            if response.status_code == 200:
                Base_response = Response(**response.json())
                return Base_response
            else:
                return Response(code=403, msg='response status code is not 200')
        except requests.exceptions.RequestException as e:
            return Response(code=403, msg=str(e))

