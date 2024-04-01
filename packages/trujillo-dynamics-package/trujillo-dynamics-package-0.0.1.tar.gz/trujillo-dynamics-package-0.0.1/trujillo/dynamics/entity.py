import pandas as pd
from datetime import datetime, timedelta
from io import StringIO
from pathlib import Path
import requests, math, json, os
from azure.storage.blob import BlobServiceClient, ContainerClient
from concurrent.futures import ThreadPoolExecutor


class Token():
    def __init__(self, environment: str = "prod", enterprise: str = "trv"):
        self.__tenant_id = 'ceb88b8e-4e6a-4561-a112-5cf771712517'
        self.__grant_type = 'client_credentials'
        self.__enterprise = enterprise
        self.__client_id = os.environ["CLIENT_ID"]
        self.__client_secret = os.environ["CLIENT_SECRET"]

        if environment == "prod":
            self.__resource = 'https://mistr.operations.dynamics.com'
        elif environment == "uat":
            self.__resource = 'https://terranova-uat.sandbox.operations.dynamics.com'
        elif environment == "master":
            self.__resource = 'https://mistr-master.sandbox.operations.dynamics.com'
        
        # if self.__enterprise == "trv":
        #     self.__client_id = '53f3c906-9bfc-4a5d-89d8-30ce9a672481'
        #     self.__client_secret = 'zNA3~9-5wuywwiflFbAP52cgJ_5wQ__Y48'
        # elif self.__enterprise == "msa":
        #     self.__client_id = '62e5f1a9-64a9-42f1-9440-ec08e4e39772'
        #     self.__client_secret = 'cVV8Q~xQG8rGIWdvfk.YDOEf8~B3LnFJ6WB_4ape'
            
    @property
    def resource(self):
        return self.__resource
    
    @resource.setter
    def resource(self, value: str):
        self.__resource = value
    
    @property
    def enterprise(self):
        return self.__enterprise
    
    @enterprise.setter
    def enterprise(self, value: str):
        self.__enterprise = value
            
    def generate_token(self):
        # endpoint
        endpoint = 'https://login.microsoftonline.com/ceb88b8e-4e6a-4561-a112-5cf771712517/oauth2/token'
        payload = {
            'tenant_id': self.__tenant_id,
            'client_id': self.__client_id,
            'client_secret': self.__client_secret,
            'grant_type': self.__grant_type,
            'resource': self.__resource}
        req = requests.post(endpoint,payload)

        if req.status_code == 200:
            # create token
            token = req.json()['access_token']
            return 'Bearer {0}'.format(token)
        else:
            return None
        
        
class Entity(Token):
    def __init__(self, environment: str = "prod", enterprise: str = "trv", name: str = None, queries: str = None):
        super().__init__(environment, enterprise)
        self.__token : str = None
        self.__name = name
        self.__queries = queries
        self.__content = pd.DataFrame()
    
    @property
    def token(self):
        if self.__token is None:
            self.__token = super().generate_token()
        return self.__token

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def queries(self):
        return self.__queries

    @queries.setter
    def queries(self, value: str):
        self.__queries = value
        
    @property
    def content(self):
        return self.__content

    def generate_token(self):
        self.__token = super().generate_token()

    def __parts(self):
        # Obtenemos la cantidad de registros para realizar el particionado de datos
        if self.__name != None:
            url =  "{0}/data/{1}/$count".format(self.resource, self.__name)
            url += f"?$filter=dataAreaId eq '{self.enterprise}'&cross-company=true"
            
            if self.__queries != None:
                url =  f"{self.resource}/data/{self.__name}/$count"        
                url += f"?{self.__queries} and dataAreaId eq '{self.enterprise}'&cross-company=true"                
            
        payload={}
        headers = {'Authorization': self.__token, 'Content-Type': 'application/json'}
        response = requests.request("GET", url, headers=headers, data=payload)
        count = int(response.text.replace("ï»¿", ""))
        
        # Creamos las particiones de datos
        urls = []
        if count > 0:
            if self.__name != None:
                url = f"{self.resource}/data/{self.__name}"
                if self.__queries != None:
                    url += f"?$skip=rvar_s&$top=rvar_t&{self.__queries} and dataAreaId eq '{self.enterprise}'&cross-company=true"
                else:
                    url += f"?$skip=rvar_s&$top=rvar_t&$filter=dataAreaId eq '{self.enterprise}'&cross-company=true"

            acumulado = 0
            lote = 10000
            frac = math.ceil(count / lote)
            iteration = list(range(frac))
            mult = count % lote

            for i in iteration:
                u = url.replace('rvar_s',str(acumulado))
                
                if i != iteration[-1]:
                    l = u.replace('rvar_t',str(lote))
                else:
                    l = u.replace('rvar_t',str(mult))
                
                urls.append(l)
                acumulado += lote

        return urls
    
    def __get_record(self, url: str):
        payload={}
        headers = {'Authorization': self.__token,'Content-Type': 'application/json'}
        
        # Verificamos que el token aún este vigente, cason contrario lo renovamos
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 401:
            self.generate_token()
            headers['Authorization'] = self.__token
            response = requests.request("GET", url, headers=headers, data=payload)
        
        response.encoding = 'utf-8'
        json_text = response.json()['value']
        content = pd.DataFrame.from_dict(json_text, orient='columns')
        if "@odata.etag" in content.columns.values:
            del content["@odata.etag"]
        
        return content

    def get_records(self, workers: int = 1):
        urls = self.__parts()
        with ThreadPoolExecutor(max_workers=workers) as executor:
            results = executor.map(self.__get_record, urls)

        dataset=[]
        for result in results:
            dataset.append(result)

        if len(dataset) > 0:
            self.__content = dataset = pd.concat(dataset)          
            
    def insert(self, object: dict):
        url = "{0}/data/{1}".format(self.resource, self.__name)

        payload = json.dumps(object)
        headers = {'Authorization': self.__token, 'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload)
        
        status = False
        if response.status_code == 201:
            status = True

        return status
    
    def update(self, object: dict):
        url = "{0}/data/{1}{2}".format(self.resource, self.__name, self.__queries)

        payload = json.dumps(object)
        headers = {'Authorization': self.__token, 'Content-Type': 'application/json', 'Accept': 'application/json'}
        response = requests.request("PATCH", url, headers=headers, data=payload)
        
        status = False
        if response.status_code == 204:
            status = True

        return status


class Tables():
    def __init__(self, url: str = None):
        self.__connections_string: str = "DefaultEndpointsProtocol=https;" +\
            "AccountName=d365dataextract;" +\
            "AccountKey=+6HnYd0AouZvfFoYNiGC+i14+VGQ2kiMTUcsqTTSr6IFir9pahAgwuzMmpvdKgiBbHPNDHDiCWI14r23jA8aIQ==;" +\
            "EndpointSuffix=core.windows.net"
        
        self.__container: str = "dynamics365-financeandoperations"
        self.__environment: str = "mistr.operations.dynamics.com/Tables/"
        self.__url: str = url
        self.__content = pd.DataFrame()
    
    @property
    def url(self):
        return self.__url
    
    @url.setter
    def url(self, value: str):
        self.__url = value

    @property
    def content(self):
        return self.__content

    
    # Métodos
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
            # https://learn.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob.blobproperties?view=azure-python
            attributes = {"name": blob.name, "last_modified": blob.last_modified, "size": blob.size}
            blobs_list.append(attributes)
        
        # Excluimos el archivo index.json
        exclude = self.__url_full() + "index.json"
        blobs_list = [blob for blob in blobs_list if blob["name"] != exclude] 
        # blobs_list.remove(exclude)
        
        return blobs_list
    
    def __get_blob(self, url: str):
        connect = self.__connections_string
        blob_service_client = BlobServiceClient.from_connection_string(
            connect)

        blob_client = blob_service_client.get_blob_client(container=self.__container, blob=url)
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
        columns = pd.DataFrame(dataset["definitions"][0]["hasAttributes"])["name"].to_list()

        return columns
    
    def __download_parallel(self, workers: int, metadata: bool, save_disk : str, url_blobs: list):
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
                                    StringIO(blob_str)
                                    , sep=","
                                    , header=None
                                    , low_memory=False
                                    , dtype="str"
                                    , names=names_columns)
                dataset.append(blob_content)

                # Guardamos en local el archivo
                if save_disk != None:
                    path = os.path.join(save_disk, names_blobs[index])
                    with open(path, "wb") as file:
                        file.write(blob)
                index += 1

        if(len(dataset) > 0): # Solo ejecutar cuando hay registros
            dataset = pd.concat(dataset)
            dataset.columns = names_columns

            if metadata == False:
                del dataset['_SysRowId']
                del dataset['LSN']
                del dataset['LastProcessedChange_DateTime']
                del dataset['DataLakeModified_DateTime']
        else:
            dataset = pd.DataFrame()

        self.__content = dataset
        
    def all_download(self, workers: int = 1, metadata: bool = False, save_disk : str = None):
        attributes = self.__url_blobs() 
        url_blobs = [attr["name"] for attr in attributes]
        names_blobs = list(map(self.__file_name, url_blobs))

        # Descargamos los archivos
        self.__download_parallel(workers, metadata, save_disk, url_blobs)

    def part_download(self, workers: int = 1, metadata: bool = False, start: int = 1, end: int = 1, descending: bool = True, save_disk : str = None):
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
        self.__download_parallel(workers, metadata, save_disk, url_blobs)
        
    def date_download(self, workers: int = 1, metadata: bool = False, save_disk : str = None, days: int = 0):
        # Obtenemos la fecha de descarga
        date = datetime.now()
        date_day = datetime.strftime(date - timedelta(days=days), '%Y-%m-%d')
        
        # Configuramos de extracción de las urls de los blobs
        attributes = self.__url_blobs() 
        blobs = pd.DataFrame(attributes)
        blobs["last_modified"] = blobs["last_modified"] - timedelta(hours=5)
        content =  blobs[blobs["last_modified"] >= date_day]
        url_blobs = list(content["name"])
        
        # Descargamos los archivos
        self.__download_parallel(workers, metadata, save_disk, url_blobs)
    
    def file_download(self, blobs: list , workers: int = 1, metadata: bool = False, save_disk : str = None):
        # Configuramos de extracción de las urls de los blobs
        url_blobs = blobs
        self.__download_parallel(workers, metadata, save_disk, url_blobs)