from typing import Dict, Union


class Config:
    
    def __init__(self, data: Dict[str, str]) -> None:
        self.apiKey: Union[str, None] = data["apiKey"]
        self.authDomain: Union[str, None] = data["authDomain"]
        self.databaseURL: Union[str, None] = data["databaseURL"]
        self.storageBucket: Union[str, None] = data["storageBucket"]
        try:
            self.serviceAccount: Union[str, Dict[str, any], None] = data['serviceAccount']
        except:
            self.serviceAccount: Union[str, Dict[str, any], None] = None
            
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(apiKey={self.apiKey}, authDomain={self.authDomain}, databaseURL={self.databaseURL}, storageBucket={self.storageBucket}, serviceAccount={self.serviceAccount})'
    
    @property
    def toJson(self):
        return self.__dict__