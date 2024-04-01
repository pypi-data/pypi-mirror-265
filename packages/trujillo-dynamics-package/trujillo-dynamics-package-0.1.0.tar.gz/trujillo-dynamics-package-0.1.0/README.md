# Introducción 
Este paquete está diseñado específicamente para proporcionar clases que permiten a los usuarios establecer una conexión eficiente con las entidades de datos de Dynamics 365 Finance and Operations.

# Empezando
Este proyecto cuenta con las siguientes clases:
1.	Generador de token (Clase Token)
2.	CRUD Data entities (Clase Entity)
3.	Conexión con tablas del Add-in Export To Data Lake (Clase Tables)

# 1. Generador de token (Clase Token)
```
import os
from dotenv import load_dotenv as env
from trujillo.dynamics.token import Token

env("environments\.env.token")
args = {
    "tenant_id": os.environ["TENANT_ID"],
    "client_id": os.environ["CLIENT_ID"],
    "client_secret": os.environ["CLIENT_SECRET"],
    "environment": os.environ["ENVIRONMENT"]
}

token = Token(args=args)
access_token = token.generate_token()
print(access_token)
```

# 2. CRUD Data entities (Clase Entity)
```
import os
from dotenv import load_dotenv as env
from trujillo.dynamics.token import Token
from trujillo.dynamics.entity import Entity

# Create access token
env("environments\.env.token")
args = {
    "tenant_id": os.environ["TENANT_ID"],
    "client_id": os.environ["CLIENT_ID"],
    "client_secret": os.environ["CLIENT_SECRET"],
    "environment": os.environ["ENVIRONMENT"]
}

token = Token(args=args)
access_token = token.generate_token()

# Create connection with data entity
entity = Entity(
    token=access_token,
    environment=os.environ["ENVIRONMENT"],
    enterprise="msa",
)

entity.name="WarehousesOnHandV2"
content = entity.get_records(workers=8)
print(content)
```
# 3. Conexión con tablas del Add-in Export To Data Lake (Clase Tables)
```
import os
from dotenv import load_dotenv as env
from trujillo.dynamics.table import Tables

env("environments\.env.table")

table = Tables(
    cn=os.environ["CONNECTION_STRING"],
    container=os.environ["CONTAINER"],
    environment=os.environ["ENVIRONMENT"],
)
table.url="SupplyChain/ProcurementAndSourcing/WorksheetLine/PurchLine/"

# Mostramos los nombres de las columnas
# Show the column names
table.table_columns()

# Mostramos la ruta de todos los archivos
# We show the path of all files
table.path_files()

# Mostramos la lista de nombres de archivo
# Show the list of file names
table.name_files()

# Mostramos la lista de atributos de todos los archivos de la tabla
# We show the list of attributes of all the files in the table
table.attribute_files()

# Descarga todos los archivos csv de la tabla, opcional workers, metadata y save_disk=F:\Documentos\python\library-dynamics
# Download all csv files from the table, optional workers, metadata and save_disk=F:\Documents\python\library-dynamics
content = table.all_download(workers=8)
print(content)

# Descarga todos los archivos csv indicados por su número
# Download all csv files indicated by their number
content = table.part_download(start=1, end=2)
print(content)

# Descarga todos los archivos indicas por días hacia atras
# Download all files indicated by days backwards
content = table.date_download(days=2)
print(content)

# Descarga todos los archivos indicados en la lista
# Download all files indicated in the list
blobs_download = ["mistr.operations.dynamics.com/Tables/SupplyChain/ProcurementAndSourcing/WorksheetLine/PurchLine/PURCHLINE_00004.csv"]
content = table.file_download(blobs=blobs_download)
print(content)
```