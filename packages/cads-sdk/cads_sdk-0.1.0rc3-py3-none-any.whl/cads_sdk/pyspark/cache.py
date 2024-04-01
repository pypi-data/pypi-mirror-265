import time
from cads_sdk.utils import log
import logging


class MemoryCacheToken:
    def __init__(self, all_config):
        if "spark.hadoop.parquet.encryption.kms.instance.id" in all_config:
            self.VAULT_ROLE_ID = all_config["spark.hadoop.parquet.encryption.kms.instance.id"]
            if "spark.hadoop.parquet.encryption.kms.instance.password" in all_config:
                self.VAULT_SECRET_ID = all_config["spark.hadoop.parquet.encryption.kms.instance.password"]
            else:
                raise Exception("You have to add vault password client \n")
        self.urn = all_config["spark.hadoop.parquet.encryption.kms.instance.url"]

    def cache_token(self, refresh_time=600):
        if hasattr(self, 'cached_token'):
            if 'timestamp' in self.cached_token:
                if time.time() - self.cached_token["timestamp"] < refresh_time:
                    return self.cached_token["token"]

        if hasattr(self, "VAULT_ROLE_ID"):
            new_token = self.get_token(self.urn, self.VAULT_ROLE_ID, self.VAULT_SECRET_ID)
            self.cached_token = {"token": new_token, "timestamp": time.time()}
            return new_token
        else:
            log("Parquet Encryption", "You are not login, you cannot encrypt or decrypt columns")
            return None

    def get_token(self, urn, VAULT_ROLE_ID, VAULT_SECRET_ID):
        import requests
        logging.debug("Refresh vault token")
        auth_header = {
            'role_id': VAULT_ROLE_ID,
            'secret_id': VAULT_SECRET_ID
        }
        try:
            r = requests.post(urn+'/v1/auth/approle/login', data=auth_header)
            if 'auth' in r.json().keys():
                token = r.json()['auth']['client_token']
                return token
            else:
                log("Parquet Encryption", "You are not login, you cannot encrypt or decrypt columns")
                return None
        except Exception as e:
            log("Requests get_token", e)
            return None