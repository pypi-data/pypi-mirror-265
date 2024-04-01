import requests
from oauth2client.service_account import ServiceAccountCredentials

from http_injector import HTTPInjector, TypeInjector

from .Authentication import Authentication as __Auth__
from .Database import Database as __Database__
from .Storage import Storage as __Storage__
from .Config import Config
from ..exc import RequiredError

class Setup(object):
    
    def __init__(self, config: Config):
        self.__api_key__ = config.apiKey
        if not self.__api_key__:
            raise  RequiredError('apiKey is Required')
        self.__auth_domain__    = config.authDomain
        self.__database_url__   = config.databaseURL
        self.__storage_bucket__ = config.storageBucket
        self.__credentials__    = None
        self.__client__         = HTTPInjector(
            typeInjector    = TypeInjector.requests,
            timeout         = 15
        )
                
        self.__serviceAccount = config.serviceAccount
        if self.__serviceAccount:
            scopes = [
                'https://www.googleapis.com/auth/firebase.database',
                'https://www.googleapis.com/auth/userinfo.email',
                "https://www.googleapis.com/auth/cloud-platform"
            ]
            if isinstance(self.__serviceAccount, str):
                self.__credentials__ = ServiceAccountCredentials.from_json_keyfile_name(self.__serviceAccount, scopes)
            elif isinstance(self.__serviceAccount, dict):
                self.__credentials__ = ServiceAccountCredentials.from_json_keyfile_dict(self.__serviceAccount, scopes)
        

class Firebase:
    
    class Authentication(Setup, __Auth__):
        
        def __init__(self, config: Config, isHttpx: bool = True):
            Setup.__init__(self, config)
            __Auth__.__init__(self, self.__api_key__, self.__client__, self.__credentials__)
    
    class Database(Setup, __Database__):
        
        def __init__(self, config: Config, isHttpx: bool = True):
            Setup.__init__(self, config)
            if not self.__database_url__:
                raise  RequiredError('databaseURL is Required')
            __Database__.__init__(self, self.__credentials__, self.__api_key__, self.__database_url__, self.__client__)
    
    class Storage(Setup, __Storage__):
        
        def __init__(self, config: Config, isHttpx: bool = True):
            Setup.__init__(self, config)
            if not self.__storage_bucket__:
                raise  RequiredError('storageBucket is Required')
            __Storage__.__init__(self, self.__credentials__, self.__storage_bucket__, self.__client__)
