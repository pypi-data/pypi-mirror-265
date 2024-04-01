import pandas as pd
import os
from datetime import datetime, timedelta
from io import StringIO
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from azure.storage.blob import BlobServiceClient, ContainerClient


class Tables():
    def __init__(self, cn: str, container: str = None, environment: str = None, url: str = None):
        self.__connections_string = cn
        self.__container: str = container
        self.__environment: str = environment
        self.__url: str = url

    @property
    def container(self):
        return self.__container

    @container.setter
    def container(self, value: str):
        self.__container = value

    @property
    def environment(self):
        return self.__environment

    @environment.setter
    def environment(self, value: str):
        self.__environment = value

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value: str):
        self.__url = value

    # Métodos privados
    # Private methods
    def __file_name(self, url: str):
        return url.split("/")[-1]

    def __url_full(self):
        return self.__environment + self.__url

    def __url_blobs(self):
        connect = self.__connections_string
        container_client = ContainerClient.from_connection_string(
            connect, self.__container)

        url = self.__url_full()
        blobs_list = []
        for blob in container_client.list_blobs(url):
            # Para obtener más propiedades aparte del nombre:
            # To get more properties than the name:
            # https://learn.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob.blobproperties?view=azure-python
            attributes = {"name": blob.name,
                          "last_modified": blob.last_modified, "size": blob.size}
            blobs_list.append(attributes)

        # Excluimos el archivo index.json
        # We exclude the index.json file
        exclude = self.__url_full() + "index.json"
        blobs_list = [blob for blob in blobs_list if blob["name"] != exclude]
        # blobs_list.remove(exclude)

        return blobs_list

    def __get_blob(self, url: str):
        connect = self.__connections_string
        blob_service_client = BlobServiceClient.from_connection_string(
            connect)

        blob_client = blob_service_client.get_blob_client(
            container=self.__container, blob=url)
        blob_stream = blob_client.download_blob().readall()

        return blob_stream

    def table_columns(self):
        return self.__get_table_columns()

    def path_files(self):
        attributes = self.__url_blobs()
        urls = [url["name"] for url in attributes]
        return urls

    def name_files(self):
        urls = self.__url_blobs()
        url_names = list(map(self.__file_name, [url["name"] for url in urls]))
        return url_names

    def attribute_files(self):
        return self.__url_blobs()

    def __get_table_columns(self):
        # Obtenemos la url con los nombres de las tablas
        url = self.__url_full()
        path = Path(url).parent
        file_table_columns = url.split("/")[-2]+".cdm.json"
        url_table_columns = str(path / file_table_columns).replace("\\", "/")

        # Retornamos los nombres de las tablas
        file_stream = self.__get_blob(url=url_table_columns)
        file_str = str(object=file_stream, encoding='utf-8')
        dataset = pd.read_json(StringIO(file_str))
        columns = pd.DataFrame(dataset["definitions"][0]["hasAttributes"])[
            "name"].to_list()

        return columns

    def __download_parallel(self, workers: int, metadata: bool, save_disk: str, url_blobs: list):
        # File name
        names_blobs = list(map(self.__file_name, url_blobs))
        names_columns = self.__get_table_columns()

        # Descargamos los archivos
        dataset = []
        with ThreadPoolExecutor(max_workers=workers) as executor:
            index = 0
            for blob in executor.map(self.__get_blob, url_blobs):
                # Convertimos el stream en csv
                blob_str = str(blob, 'utf-8')
                blob_content = pd.read_csv(
                    StringIO(blob_str), sep=",", header=None, low_memory=False, dtype="str", names=names_columns)
                dataset.append(blob_content)

                # Guardamos en local el archivo
                if save_disk != None:
                    path = os.path.join(save_disk, names_blobs[index])
                    with open(path, "wb") as file:
                        file.write(blob)
                index += 1

        if (len(dataset) > 0):  # Solo ejecutar cuando hay registros
            dataset = pd.concat(dataset)
            dataset.columns = names_columns

            if metadata == False:
                del dataset['_SysRowId']
                del dataset['LSN']
                del dataset['LastProcessedChange_DateTime']
                del dataset['DataLakeModified_DateTime']
        else:
            dataset = pd.DataFrame()

        return dataset

    def all_download(self, workers: int = 1, metadata: bool = False, save_disk: str = None):
        attributes = self.__url_blobs()
        url_blobs = [attr["name"] for attr in attributes]
        names_blobs = list(map(self.__file_name, url_blobs))

        # Descargamos los archivos
        return self.__download_parallel(workers, metadata, save_disk, url_blobs)

    def part_download(self, workers: int = 1, metadata: bool = False, start: int = 1, end: int = 1, descending: bool = True, save_disk: str = None):
        # Configuramos de extracción de las urls de los blobs
        attributes = self.__url_blobs()
        url_blobs = [attr["name"] for attr in attributes]
        url_blobs.sort(reverse=descending)

        # Configuramos desde donde y hasta donde va extraer las urls de los blobs
        __start = start - 1 if start > 0 else start
        __end = end

        if __start == 0 and __end == 0:
            url_blobs = url_blobs[:1]
        else:
            url_blobs = url_blobs[__start:__end]
        names_blobs = list(map(self.__file_name, url_blobs))

        # Descargamos los archivos
        return self.__download_parallel(workers, metadata, save_disk, url_blobs)

    def date_download(self, workers: int = 1, metadata: bool = False, save_disk: str = None, days: int = 0):
        # Obtenemos la fecha de descarga
        date = datetime.now()
        date_day = datetime.strftime(date - timedelta(days=days), '%Y-%m-%d')

        # Configuramos de extracción de las urls de los blobs
        attributes = self.__url_blobs()
        blobs = pd.DataFrame(attributes)
        blobs["last_modified"] = blobs["last_modified"] - timedelta(hours=5)
        content = blobs[blobs["last_modified"] >= date_day]
        url_blobs = list(content["name"])

        # Descargamos los archivos
        return self.__download_parallel(workers, metadata, save_disk, url_blobs)

    def file_download(self, blobs: list, workers: int = 1, metadata: bool = False, save_disk: str = None):
        # Configuramos de extracción de las urls de los blobs
        url_blobs = blobs
        return self.__download_parallel(workers, metadata, save_disk, url_blobs)