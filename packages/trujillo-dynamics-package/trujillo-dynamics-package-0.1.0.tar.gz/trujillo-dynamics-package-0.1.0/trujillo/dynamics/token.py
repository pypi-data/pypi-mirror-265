import requests

class Token():
    def __init__(self, args: dict):
        self.__tenant_id = args["tenant_id"]
        self.__client_id = args["client_id"]
        self.__client_secret = args["client_secret"]
        self.__grant_type = 'client_credentials'
        self.__environment = args["environment"]

    @property
    def environment(self):
        return self.__environment

    @environment.setter
    def environment(self, value: str):
        self.__environment = value

    # Public methods
    def generate_token(self):
        try:
            # Endpoint
            endpoint = 'https://login.microsoftonline.com/ceb88b8e-4e6a-4561-a112-5cf771712517/oauth2/token'
            payload = {
                'tenant_id': self.__tenant_id,
                'client_id': self.__client_id,
                'client_secret': self.__client_secret,
                'grant_type': self.__grant_type,
                'resource': self.__environment}
            
            req = requests.post(endpoint, payload, timeout=3)
            req.raise_for_status()

            # Create token
            token = ""
            if req.status_code == 200:
                access_token = req.json()['access_token']
                token = f'Bearer {access_token}'
                
            return token
        
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)     