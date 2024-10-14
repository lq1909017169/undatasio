import os
from typing import Dict, List
from langchain_core.documents import Document as lcDocument
import requests
from llama_index.core.schema import Document
from requests_toolbelt.multipart.encoder import MultipartEncoder


class UnDatasIO:
    def __init__(self, token: str, task_name: str = ""):
        self.token = token
        self.task_name = task_name
        self.base_url = 'https://backend.undatas.io/api/api'

    def upload(self, file_dir_path: str) -> Dict:
        """
        :param file_dir_path: Upload specified folder
        :return:
        """
        for file_path in os.listdir(file_dir_path):
            file_read_path = os.path.join(file_dir_path, file_path)
            with open(file_read_path, "rb") as file:
                fields = {
                    "user_id": self.token,
                    "task_name": self.task_name,
                    "file": (file_path, file, "application/octet-stream"),
                }
                m = MultipartEncoder(fields=fields)

                # 发送 POST 请求
                headers = {"Content-Type": m.content_type}
                response = requests.post(
                    f"{self.base_url}/upload", data=m, headers=headers
                )
                if response.json()['code'] != 200:
                    return {"code": 403, "msg": response.json()['msg']}
        return {"code": 200, "msg": "upload success"}

    def parser(self, file_name_list: List) -> Dict:
        """
        :param file_name_list: List of parsed file names
        :return:
        """
        API_ENDPOINT = f"{self.base_url}/task_return_list"
        data = {
            "user_id": self.token,
            "task_name": self.task_name,
            "fileName": file_name_list,  # 根据你的接口定义，文件名参数应该是 fileName
        }

        try:
            response = requests.post(API_ENDPOINT, data=data)
            if response.json()['code'] != 200:
                return {"code": 403, "msg": response.json()['msg']}
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"code": 403, "msg": f"{e}"}

    def download(self, version: str) -> Dict:
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
            if response.json()['code'] != 200:
                return {"code": 403, "msg": response.json()['msg']}
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"code": 403, "msg": f"{e}"}

    def show_version(self) -> Dict:
        """
        :return:
        """
        API_ENDPOINT = f"{self.base_url}/version_info"
        data = {"user_id": self.token, "task_name": self.task_name}

        try:
            response = requests.post(API_ENDPOINT, data=data)
            if response.json()['code'] != 200:
                return {"code": 403, "msg": response.json()['msg']}
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"code": 403, "msg": f"{e}"}

    def show_upload(self) -> Dict:
        """
        :return:
        """
        API_ENDPOINT = f"{self.base_url}/view_upload_file"
        data = {"user_id": self.token, "task_name": self.task_name}

        try:
            response = requests.post(API_ENDPOINT, data=data)
            if response.json()['code'] != 200:
                return {"code": 403, "msg": response.json()['msg']}
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"code": 403, "msg": f"{e}"}

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
            if response.json()['code'] != 200:
                return {"code": 403, "msg": response.json()['msg']}
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"code": 403, "msg": f"{e}"}

    def get_result_to_langchain_document(
            self, type_info: List, file_name: str, version: str
    ) -> lcDocument:
        """
        :param type_info: Please select from title, table, text, image, interline_equation
        :param file_name: file name
        :param version: version
        :return: langchain_core.Document
        """
        result = self.get_result_type(type_info, file_name, version)['data']
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

        result = self.get_result_type(type_info, file_name, version)['data']
        return Document(
            text=result,
            metadata={
                "source": f"{self.task_name}_{version}_{file_name}_[{','.join(type_info)}]"
            },
        )
