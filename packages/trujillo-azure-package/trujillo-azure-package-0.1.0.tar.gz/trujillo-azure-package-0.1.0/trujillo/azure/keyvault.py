from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential


class KeyVault():
    def __init__(self, tenant_id: str, client_id: str, client_secret: str, vault_url: str):
        self.__tenant_id = tenant_id
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__vault_url = vault_url

    def __credential(self):
        credentials = ClientSecretCredential(
            client_id=self.__client_id,
            client_secret=self.__client_secret,
            tenant_id=self.__tenant_id,
        )

        return credentials

    def get_secret(self, secret_name: str):
        client_secret = SecretClient(
            vault_url=self.__vault_url,
            credential=self.__credential(),
        )

        secret = client_secret.get_secret(name=secret_name)
        return secret.value
