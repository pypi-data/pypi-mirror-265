from typing import Dict, List, Tuple, Union

import requests
from .utils import ParamsAuth, ParamsToken, ParamsVerifyAssertion, deviceId, URL, Headers, Response as __Response__, GType
from .response import AuthResponse, TokenResponse, VerifyAuthResponse, RefreshTokenResponse
from .base import GoogleAuth, FirebaseCore
from .exc import BadAuthentication, NeedsBrowser, Error
from .fire import Firebase as __Firebase__, Config

from http_injector._adapter import RequestsAdapter

class HTTPInjector:

    def __new__(cls):
        client = requests.Session()
        adapter = RequestsAdapter(timeout=86400, max_retries=3)
        for scheme in ('http://', 'https://'): client.mount(scheme, adapter)
        return client

class LocalGoogleInjector:
    
    @staticmethod
    def Google_Login(Email: str, Password: str, deviceId: str) -> 'TokenResponse':
        Response = GoogleAuth.SelectBy(Email)
        if not Response:
            client = HTTPInjector()
            client.headers = Headers(
                gType   = GType.GoogleAuth,
                deviceId= deviceId
            )
            Response = TokenResponse(
                __Response__(
                        client.post(
                        url     = URL(GType.GoogleAuth),
                        data    = ParamsToken(
                            Email       = Email,
                            Password    = Password,
                            deviceId    = deviceId,
                        ),
                        #verify=True, timeout=30
                    ).text
                ),
                Password,
                deviceId
            )
            print(client.headers)
            if not Response.Error:
                GoogleAuth.Insert(Response)
                return GoogleAuth.SelectBy(Email)
            if Response.Error == 'NeedsBrowser':
                raise NeedsBrowser(Response.Error)
            elif Response.Error == 'BadAuthentication':
                raise BadAuthentication(Response.Error)
            else:
                raise Error(Response.Error)
        return Response
    
    @staticmethod
    def GetIdToken(Email: str, Token: str, service: str, app: str, client_sig: str, deviceId: str) -> 'AuthResponse':
        client = HTTPInjector()
        client.headers = Headers(
            gType   = GType.GoogleAuth,
            deviceId= deviceId
        )
        return AuthResponse(
            __Response__(
                client.post(
                    url     = URL(GType.GoogleAuth),
                    data    = ParamsAuth(
                        Email       = Email,
                        Token       = Token,
                        service     = service,
                        app         = app,
                        client_sig  = client_sig,
                        deviceId    = deviceId,
                    )
                ).text
            )
        )
    
    @classmethod
    def VerifyAuth(cls, Email: str, Token: str, service: str, app: str, deviceId: str, client_sig: str, apiKey: str, APP: int, create: int) -> Tuple['VerifyAuthResponse', Union['AuthResponse', 'None']]:
        Response, getAuth = FirebaseCore.SelectByHexDigest(Email, APP), None
        if not Response:
            getAuth = cls.GetIdToken(Email, Token, service, app, client_sig, deviceId)
            if not getAuth.Error:
                client = HTTPInjector()
                client.headers = Headers(
                    gType       = GType.FirebaseCore,
                    app         = app,
                    client_sig  = client_sig
                )
                _Response = VerifyAuthResponse(
                    client.post(
                        url     = f'{URL(GType.FirebaseCore)}verifyAssertion?key={apiKey}',
                        json    = ParamsVerifyAssertion(
                            idToken = getAuth.Auth
                        )
                    ).json(),
                    APP, create
                )
               # print(_Response.to_json); exit()
                if not _Response.Message:
                    FirebaseCore.Insert(_Response, APP, create)
                    return FirebaseCore.SelectByHexDigest(Email, APP), getAuth
                else:
                    Response = [_Response]
                raise Error(_Response.Message)
            
            if getAuth.Error == 'NeedsBrowser':
                raise NeedsBrowser(getAuth.Error)
            elif getAuth.Error == 'BadAuthentication':
                raise BadAuthentication(getAuth.Error)
            else:
                raise Error(getAuth.Error)
        return Response, getAuth
    
    @classmethod
    def VerifyAutV2(cls, idToken: str, app: str, client_sig: str, apiKey: str, APP: int, create: int) -> 'VerifyAuthResponse':
        client = HTTPInjector()
        client.headers = Headers(
            gType       = GType.FirebaseCore,
            app         = app,
            client_sig  = client_sig
        )
        return VerifyAuthResponse(
            client.post(
                url     = f'{URL(GType.FirebaseCore)}verifyAssertion?key={apiKey}',
                json    = ParamsVerifyAssertion(
                    idToken = idToken
                )
            ).json(),
            APP,
            create
        )

    class Firebase(__Firebase__): ...

    class FirebaseConfig(Config): ...

class ServerGoogleInjector:
    
    @staticmethod
    def Google_Login(Email: str, Password: str, deviceId: str):
        client = HTTPInjector()
        client.headers = Headers(
            gType   = GType.GoogleAuth,
            deviceId= deviceId
        )
        return TokenResponse(
            __Response__(
                    client.post(
                    url     = URL(GType.GoogleAuth),
                    data    = ParamsToken(
                        Email       = Email,
                        Password    = Password,
                        deviceId    = deviceId,
                    ),
                    verify=True, timeout=30
                ).text
            ),
            Password,
            deviceId
        )
    
    @staticmethod
    def getIdToken(Email: str, Token: str, service: str, app: str, client_sig: str, deviceId: str):
        client = HTTPInjector()
        client.headers = Headers(
            gType   = GType.GoogleAuth,
            deviceId= deviceId
        )
        return AuthResponse(
            __Response__(
                client.post(
                    url     = URL(GType.GoogleAuth),
                    data    = ParamsAuth(
                        Email       = Email,
                        Token       = Token,
                        service     = service,
                        app         = app,
                        client_sig  = client_sig,
                        deviceId    = deviceId,
                    )
                ).text
            )
        )
    
    @classmethod
    def VerifyAuth(cls, idToken: str, app: str, client_sig: str, apiKey: str, APP: int, create: int):
        client = HTTPInjector()
        client.headers = Headers(
            gType       = GType.FirebaseCore,
            app         = app,
            client_sig  = client_sig
        )
        return VerifyAuthResponse(
            client.post(
                url     = f'{URL(GType.FirebaseCore)}verifyAssertion?key={apiKey}',
                json    = ParamsVerifyAssertion(
                    idToken = idToken
                )
            ).json(),
            APP,
            create
        )
    
    