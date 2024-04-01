import pandas as pd
import requests
import math
import json
from concurrent.futures import ThreadPoolExecutor


class Entity():
    def __init__(self, token: str, environment: str, enterprise: str, name: str = None, queries: str = None):
        self.__token = token
        self.__environment = environment
        self.__enterprise = enterprise
        self.__name = name
        self.__queries = queries

    @property
    def environment(self):
        return self.__environment

    @environment.setter
    def environment(self, value: str):
        self.__environment = value

    @property
    def enterprise(self):
        return self.__enterprise

    @enterprise.setter
    def enterprise(self, value: str):
        self.__enterprise = value

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

    # Private methods
    def __parts(self):
        # Obtenemos la cantidad de registros para realizar el particionado de datos
        # We obtain the number of records to perform data partitioning
        if self.__name != None:
            url = "{0}/data/{1}/$count".format(self.__environment, self.__name)
            url += f"?$filter=dataAreaId eq '{self.__enterprise}'&cross-company=true"

            if self.__queries != None:
                url = f"{self.__environment}/data/{self.__name}/$count"
                url += f"?{self.__queries} and dataAreaId eq '{self.__enterprise}'&cross-company=true"

        payload = {}
        headers = {'Authorization': self.__token,
                   'Content-Type': 'application/json'}
        response = requests.request("GET", url, headers=headers, data=payload)
        count = int(response.text.replace("ï»¿", ""))

        # Creamos las particiones de datos
        # We create the data partitions
        urls = []
        if count > 0:
            if self.__name != None:
                url = f"{self.__environment}/data/{self.__name}"
                if self.__queries != None:
                    url += f"?$skip=rvar_s&$top=rvar_t&{self.__queries} and dataAreaId eq '{self.__enterprise}'&cross-company=true"
                else:
                    url += f"?$skip=rvar_s&$top=rvar_t&$filter=dataAreaId eq '{self.__enterprise}'&cross-company=true"

            acumulado = 0
            lote = 10000
            frac = math.ceil(count / lote)
            iteration = list(range(frac))
            mult = count % lote

            for i in iteration:
                u = url.replace('rvar_s', str(acumulado))

                if i != iteration[-1]:
                    l = u.replace('rvar_t', str(lote))
                else:
                    l = u.replace('rvar_t', str(mult))

                urls.append(l)
                acumulado += lote

        return urls

    def __get_record(self, url: str):
        payload = {}
        headers = {'Authorization': self.__token,
                   'Content-Type': 'application/json'}

        # Verificamos que el token aún este vigente, cason contrario lo renovamos
        # We verify that the token is still valid, otherwise we renew it
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 401:
            self.generate_token()
            headers['Authorization'] = self.__token
            response = requests.request(
                "GET", url, headers=headers, data=payload)

        response.encoding = 'utf-8'
        json_text = response.json()['value']
        content = pd.DataFrame.from_dict(json_text, orient='columns')
        if "@odata.etag" in content.columns.values:
            del content["@odata.etag"]

        return content

    def get_records(self, workers: int = 1):
        content = pd.DataFrame()
        urls = self.__parts()
        with ThreadPoolExecutor(max_workers=workers) as executor:
            results = executor.map(self.__get_record, urls)

        dataset = []
        for result in results:
            dataset.append(result)

        if len(dataset) > 0:
            content = pd.concat(dataset)

        return content

    def insert(self, object: dict):
        url = "{0}/data/{1}".format(self.__environment, self.__name)

        payload = json.dumps(object)
        headers = {'Authorization': self.__token,
                   'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload)

        status = False
        if response.status_code == 201:
            status = True

        return status

    def update(self, object: dict):
        url = "{0}/data/{1}{2}".format(self.__environment,
                                       self.__name, self.__queries)

        payload = json.dumps(object)
        headers = {'Authorization': self.__token,
                   'Content-Type': 'application/json', 'Accept': 'application/json'}
        response = requests.request(
            "PATCH", url, headers=headers, data=payload)

        status = False
        if response.status_code == 204:
            status = True

        return status
