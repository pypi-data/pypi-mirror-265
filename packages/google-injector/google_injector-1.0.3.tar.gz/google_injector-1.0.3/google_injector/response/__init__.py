import hashlib
import json
from typing import Dict, Union

class TokenResponse:
    
    SID: Union[str, None] = None
    LSID: Union[str, None] = None
    Auth: Union[str, None] = None
    Token: Union[str, None] = None
    services: Union[str, None] = None
    firstName: Union[str, None] = None
    lastName: Union[str, None] = None
    GooglePlusUpdate: Union[str, None] = None
    Email: Union[str, None] = None
    accountId: Union[str, None] = None
    Password: Union[str, None] = None
    deviceId: Union[str, None] = None
    Error: Union[str, None] = None
    
    def __init__(self, result: Dict[str, str], password: str, deviceId: str) -> None:
        if 'Error' not in result:
            self.SID: str = result['SID']
            self.LSID: str = result['LSID']
            self.Auth: str = result['Auth']
            self.Token: str = result['Token']
            self.services: str = result['services']
            self.firstName: str = result['firstName']
            self.lastName: str = result['lastName']
            self.GooglePlusUpdate: str = result['GooglePlusUpdate']
            self.Email: str = result['Email']
            self.accountId: str = result['accountId']
            self.Password: str = password
            self.deviceId: str = deviceId
        else:
            try:
                self.Error = result['ErrorDetail']
            except KeyError:
                self.Error = result['Error']
    
    def __repr__(self) -> str:
        if not self.Error:
            return f'{self.__class__.__name__}(SID={self.SID}, LSID={self.LSID}, Auth={self.Auth}, Token={self.Token}, services={self.services}, firstName={self.firstName}, lastName={self.lastName}, GooglePlusUpdate={self.GooglePlusUpdate}, Email={self.Email}, Password={self.Password}, deviceId={self.deviceId}, accountId={self.accountId})'
        else:
            return f'{self.__class__.__name__}(Error={self.Error})'

    @property
    def to_json(self): return self.__dict__

class AuthResponse:
    
    issueAdvice: Union[str, None] = None
    Expiry: Union[str, None] = None
    ExpiresInDurationSec: Union[str, None] = None
    storeConsentRemotely: Union[str, None] = None
    isTokenSnowballed: Union[str, None] = None
    Auth: Union[str, None] = None
    Error: Union[str, None] = None
    
    def __init__(self, result: Dict[str, str]) -> None:
        if 'Error' not in result:
            self.issueAdvice: str = result['issueAdvice']
            self.Expiry: str = result['Expiry']
            self.ExpiresInDurationSec: str = result['ExpiresInDurationSec']
            self.storeConsentRemotely: str = result['storeConsentRemotely']
            self.isTokenSnowballed: str = result['isTokenSnowballed']
            self.Auth: str = result['Auth']
        else:
            self.Error: str = result['Error']
    
    def __repr__(self) -> str:
        if not self.Error:
            return f'{self.__class__.__name__}(issueAdvice={self.issueAdvice}, Expiry={self.Expiry}, ExpiresInDurationSec={self.ExpiresInDurationSec}, storeConsentRemotely={self.storeConsentRemotely}, isTokenSnowballed={self.isTokenSnowballed}, Auth={self.Auth})'
        else:
            return f'{self.__class__.__name__}(Error={self.Error})'

    @property
    def to_json(self): return self.__dict__

class RawUserInfo:
    
    def __init__(self, result: Dict[str, Union[str, bool, int]]) -> None:
        self.iss: str = result['iss']
        self.azp: str = result['azp']
        self.aud: str = result['aud']
        self.sub: str = result['sub']
        self.email: str = result['email']
        self.email_verified: bool = result['email_verified']
        self.iat: int = result['iat']
        self.exp: int = result['exp']
        
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(iss={self.iss}, azp={self.azp}, aud={self.aud}, sub={self.sub}, email={self.email}, email_verified={self.email_verified}, iat={self.iat}, exp={self.exp})'

    @property
    def to_json(self): return self.__dict__

class VerifyAuthResponse:
    
    hexdigest: Union[str, None] = None
    federatedId: Union[str, None] = None
    providerId: Union[str, None] = None
    email: Union[str, None] = None
    app: Union[int, None] = None
    create: Union[int, None] = None
    emailVerified: Union[bool, None] = None
    localId: Union[str, None] = None
    idToken: Union[str, None] = None
    refreshToken: Union[str, None] = None
    expiresIn: Union[str, None] = None
    oauthIdToken: Union[str, None] = None
    rawUserInfo: Union[RawUserInfo, None] = None
    kind: Union[str, None] = None
    Message: Union[str, None] = None
    
    def __init__(self, result: Dict[str, Union[str, bool]], app: int, create: int) -> None:
        if 'error' not in result:
            self.federatedId: str = result['federatedId']
            self.providerId: str = result['providerId']
            self.email: str = result['email']
            self.app: int = app
            self.create: int = create
            self.emailVerified: bool = result['emailVerified']
            self.localId: str = result['localId']
            self.idToken: str = result['idToken']
            self.refreshToken: str = result['refreshToken']
            self.expiresIn: str = result['expiresIn']
            self.oauthIdToken: str = result['oauthIdToken']
            self.rawUserInfo: RawUserInfo = RawUserInfo(json.loads(result['rawUserInfo']))
            self.kind: str = result['kind']
            self.hexdigest: str = hashlib.md5(f'{self.email}|{self.app}'.encode()).hexdigest()
        else:
            error = dict(result.get('error'))
            self.Message = error.get('message')
    
    def __repr__(self) -> str:
        if not self.Message:
            return f'{self.__class__.__name__}(hexdigest={self.hexdigest}, federatedId={self.federatedId}, providerId={self.providerId}, email={self.email}, emailVerified={self.emailVerified}, localId={self.localId}, idToken={self.idToken}, refreshToken={self.refreshToken}, expiresIn={self.expiresIn}, oauthIdToken={self.oauthIdToken}, rawUserInfo={self.rawUserInfo}, kind={self.kind}, app={self.app}, create={self.create})'
        else:
            return f'{self.__class__.__name__}(Message={self.Message})'

    @property
    def to_json(self): 
        result = self.__dict__
        rw: RawUserInfo = result.get('rawUserInfo')
        result.update(rawUserInfo = rw.to_json)
        return result

class RefreshTokenResponse:
    
    userId: Union[str, None] = None
    idToken: Union[str, None] = None
    refreshToken: Union[str, None] = None
    
    def __init__(self, result: Dict[str, str]) -> None:
        self.userId = result['userId']
        self.idToken = result['idToken']
        self.refreshToken = result['refreshToken']
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(userId={self.userId}, idToken={self.idToken}, refreshToken={self.refreshToken})'
    
    @property
    def to_json(self):
        return self.__dict__