import random
import secrets
from typing import Dict, Optional
from Cryptodome.PublicKey.RSA import RsaKey

from .Key_Base64 import ANDROID_KEY_7_3_29, construct_signature
from .types import GType
from ..exc import RequiredError

def Response(text: str) -> Dict[str, str]:  # Parse auth response
   response_data = { # Initialize response data as empty dict
   }
   for line in text.split("\n"):  # Loop through each line in text
       if not line:             # Skip empty lines
           continue
       key, _, val = line.partition("=")  # Partition line into key, separator, value
       response_data[key] = val  # Add key-value pair to response data
   return response_data  # Return response data
    
def Signature(email: str, password: str, key: RsaKey):
    # Construct signature using email, password, and key
    return construct_signature(email, password, key)
    
def AndroidKey():
    return ANDROID_KEY_7_3_29

def deviceId():
    return secrets.token_hex(8)

def Headers(gType: GType, deviceId: Optional[str] = None, app: Optional[str] = None, client_sig: Optional[str] = None):
    if gType == GType.GoogleAuth:
        if deviceId is None: 
            raise RequiredError('deviceId required')
        return {
            "User-Agent"    : "GoogleAuth/1.4 (land MMB29M); gzip",
            "Content-type"  : "application/x-www-form-urlencoded",
            "device"        : deviceId,
            "gmsversion"    : "232414019",
            "gmscoreFlow"   : "16"
        }
    else:
        if app is None: 
            raise RequiredError('app required')
        if client_sig is None: 
            raise RequiredError('client_sig required')
        return {
            'Content-Type': 'application/json',
            'X-Android-Package': app,
            'X-Android-Cert': client_sig.upper(),
            'Accept-Language': 'in-ID, en-US',
            'X-Client-Version': 'Android/Fallback/X22001000/FirebaseCore-Android'
        }
    
def URL(gType: GType):
    if gType == GType.GoogleAuth:
        #return 'https://android.clients.google.com/auth'
        return random.choice(['https://android.googleapis.com/auth', 'https://android.clients.google.com/auth'])
    else:
        return 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/'

def ParamsToken(Email: str, Password: str, deviceId: str, service: str = 'ac2dm', device_country: str = 'id', operator_country: str = 'id', lang: str = 'in-ID', client_sig: str = '38918a453d07199354f8b19af05ec6562ced5788', jwt: bool = True):
    return dict(
        androidId                       = deviceId,
        lang                            = lang,
        google_play_services_version    = 232414019,
        sdk_version                     = 20,            
        device_country                  = device_country,
        build_device                    = 'land',
        build_brand                     = 'Xiaomi',
        build_fingerprint               = 'Xiaomi/land/land:6.0.1/MMB29M/V10.2.2.0.MALMIXM:user/release-keys',
        service                         = service,
        build_product                   = 'land',
        callerPkg                       = 'com.google.android.gms',
        get_accountid                   = 1,
        callerSig                       = client_sig,
        Email                           = Email,
        ACCESS_TOKEN                    = 1,
        droidguard_results              = 'DESKAONE',
        add_account                     = 1,
        accountType                     = 'HOSTED_OR_GOOGLE',
        has_permission                  = 1,
        EncryptedPasswd                 = Signature(Email, Password, AndroidKey()).decode(),
        source                          = 'android',
        operatorCountry                 = operator_country,
        client_sig                      = client_sig,
        check_email                     = 1,
        oauth2_include_email            = 1,
        token_request_options           = 'CAA4AVAB'
    )

def ParamsAuth(Email: str, Token: str, service: str, app: str, client_sig: str, deviceId: str, device_country: str = 'id', operator_country: str = 'id', lang: str = 'in-ID'):
    return dict(
        accountType                     = 'HOSTED_OR_GOOGLE',
        Email                           = Email,
        has_permission                  = 1,
        EncryptedPasswd                 = Token,
        service                         = service,
        source                          = 'android',
        androidId                       = deviceId,
        app                             = app,
        device_country                  = device_country,
        operatorCountry                 = operator_country,
        lang                            = lang,
        sdk_version                     = 20,
        client_sig                      = client_sig,
        google_play_services_version    = 232414019,
        check_email                     = 1,
        oauth2_include_email            = 1,
        callerPkg                       = 'com.google.android.gms',
    )

def ParamsVerifyAssertion(idToken: str):
    return dict(
        autoCreate          = True,
        returnSecureToken   = True,
        postBody            = f'id_token={idToken}&providerId=google.com',
        requestUri          = 'http://localhost',
        returnIdpCredential = True
    )