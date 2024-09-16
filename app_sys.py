from aws_cdk import App, Environment, DefaultStackSynthesizer
from cdk_python.cdk_python_stack import PilaEc2
import boto3

# Obtener automáticamente el Account ID y la región
session = boto3.session.Session()
account_id = boto3.client('sts').get_caller_identity()['Account']
region = session.region_name

# Definir un nuevo qualifier
qualifier = "ec2-dep"

# Crear una instancia de la aplicación CDK
app = App()

# Definir el entorno con el Account ID y la región obtenidos automáticamente
env = Environment(account=account_id, region=region)

# Configurar el sintetizador con el qualifier correcto
sintetizador = DefaultStackSynthesizer(
    qualifier=qualifier, # Qualifier verifica los componentes en base al prefijo.
    cloud_formation_execution_role=f"arn:aws:iam::{account_id}:role/LabRole",
    file_assets_bucket_name=f"cdk-{qualifier}-assets-{account_id}-{region}"
)

# Crear la instancia de la pila EC2
PilaEc2(app, "PilaEc2", env=env, synthesizer=sintetizador)

# Sintetizar y desplegar la aplicación
app.synth()
