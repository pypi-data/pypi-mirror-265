import json, os, hashlib
from typing import Dict, List, Union
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, INTEGER, VARCHAR, TEXT, BOOLEAN
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
from sqlalchemy.schema import CreateSchema
from sqlalchemy.exc import IntegrityError
from sqlalchemy_utils import database_exists, create_database
from dotenv import load_dotenv
load_dotenv()

from ..response import VerifyAuthResponse

__Base_Sessions__ = declarative_base()

class Sessions(__Base_Sessions__):
    
    __tablename__   = f'Session'
    id              = Column(INTEGER(), primary_key=True)
    hexdigest       = Column(VARCHAR(255), unique=True, nullable=False)
    email           = Column(VARCHAR(255), nullable=False)
    app             = Column(INTEGER(), nullable=False)
    federatedId     = Column(TEXT(), nullable=False)
    providerId      = Column(TEXT(), nullable=False)
    emailVerified   = Column(BOOLEAN(), nullable=False)
    localId         = Column(TEXT(), nullable=False)
    idToken         = Column(TEXT(), nullable=False)
    refreshToken    = Column(TEXT(), nullable=False)
    expiresIn       = Column(TEXT(), nullable=False)
    oauthIdToken    = Column(TEXT(), nullable=False)
    rawUserInfo     = Column(TEXT(), nullable=False)
    kind            = Column(TEXT(), nullable=False)
    create          = Column(INTEGER(), nullable=False)

def BaseMetaData() -> MetaData:
    return __Base_Sessions__.metadata

class Engine:
    def __init__(self) -> None:
        #dbschema = 'evm,solana,public'
        if os.path.exists('Session') is False: os.mkdir('Session')
        self.Engine = create_engine(f'sqlite:///Session/FirebaseCore.sqlite', echo=False, pool_pre_ping=True)
        if not database_exists(self.Engine.url):
            create_database(self.Engine.url)
            BaseMetaData().create_all(self.Engine)

    def Connect(self):
        # Get SQLite engine connection
        return self.Engine.connect()

    def Session(self):
        # Create session factory
        Session = sessionmaker(bind=self.Engine)
        # Get session instance
        return Session()

class FirebaseCore:
    
    @staticmethod
    def InsertMassal(response: List[VerifyAuthResponse], app: int, create: int):
        
        try:
            DB      = Engine()
            Session = DB.Session()
            Session.add_all(
                [
                    Sessions(
                        hexdigest       = hashlib.md5(f'{Response.email}|{app}'.encode()).hexdigest(),
                        email           = Response.email,
                        app             = app,
                        create          = create,
                        federatedId     = Response.federatedId,
                        providerId      = Response.providerId,
                        emailVerified   = Response.emailVerified,
                        localId         = Response.localId,
                        idToken         = Response.idToken,
                        refreshToken    = Response.refreshToken,
                        expiresIn       = Response.expiresIn,
                        oauthIdToken    = Response.oauthIdToken,
                        rawUserInfo     = json.dumps(Response.rawUserInfo.to_json),
                        kind            = Response.kind,
                    )
                    for Response in response
                ]
            )
            Session.commit()
            Session.invalidate()
            Session.close()
            DB.Engine.dispose()
            return True
        except IntegrityError: return False
    
    @staticmethod
    def Insert(Response: VerifyAuthResponse, app: int, create: int):
        try:
            DB      = Engine()
            Session = DB.Session()
            Session.add(Sessions(
                hexdigest       = hashlib.md5(f'{Response.email}|{app}'.encode()).hexdigest(),
                email           = Response.email,
                app             = app,
                create          = create,
                federatedId     = Response.federatedId,
                providerId      = Response.providerId,
                emailVerified   = Response.emailVerified,
                localId         = Response.localId,
                idToken         = Response.idToken,
                refreshToken    = Response.refreshToken,
                expiresIn       = Response.expiresIn,
                oauthIdToken    = Response.oauthIdToken,
                rawUserInfo     = json.dumps(Response.rawUserInfo.to_json),
                kind            = Response.kind,
            ))
            Session.commit()
            Session.invalidate()
            Session.close()
            DB.Engine.dispose()
            return True
        except IntegrityError: return False
    
    @staticmethod
    def Update(Response: VerifyAuthResponse, app: int):
        DB      = Engine()
        Session = DB.Session()
        Data    = Response.to_json; Data.pop('email'); Data.update(rawUserInfo = json.dumps(Data.get('rawUserInfo')))
        hexdigest = Data.get('hexdigest'); Data.pop('hexdigest')
        Result  = Session.query(Sessions).filter_by(hexdigest = hexdigest).update(Data)
        Session.commit()
        Session.invalidate()
        Session.close()
        DB.Engine.dispose()
        return Result
    
    @staticmethod
    def Select(offset: int = 0, limit: int = 10):
        DB      = Engine()
        Session = DB.Session()
        Result = Session.query(Sessions).filter().offset(offset).limit(limit).all()
        Session.invalidate()
        Session.close()
        DB.Engine.dispose()
        if len(Result) != 0: return [
            VerifyAuthResponse(
                dict(
                    email           = Response.email,
                    federatedId     = Response.federatedId,
                    providerId      = Response.providerId,
                    emailVerified   = Response.emailVerified,
                    localId         = Response.localId,
                    idToken         = Response.idToken,
                    refreshToken    = Response.refreshToken,
                    expiresIn       = Response.expiresIn,
                    oauthIdToken    = Response.oauthIdToken,
                    rawUserInfo     = Response.rawUserInfo,
                    kind            = Response.kind,
                ),
                Response.app,
                Response.create
            )
            for Response in Result
        ]
        return None
    
    @staticmethod
    def Count():
        DB      = Engine()
        Session = DB.Session()
        Result = Session.query(Sessions).filter().count()
        Session.invalidate()
        Session.close()
        DB.Engine.dispose()        
        return Result
    
    @staticmethod
    def SelectBy(Email: str):
        DB      = Engine()
        Session = DB.Session()
        Result = Session.query(Sessions).filter_by(email = Email).all()
        Session.invalidate()
        Session.close()
        DB.Engine.dispose()
        if len(Result) != 0: return [
            VerifyAuthResponse(
                dict(
                    email           = Response.email,
                    federatedId     = Response.federatedId,
                    providerId      = Response.providerId,
                    emailVerified   = Response.emailVerified,
                    localId         = Response.localId,
                    idToken         = Response.idToken,
                    refreshToken    = Response.refreshToken,
                    expiresIn       = Response.expiresIn,
                    oauthIdToken    = Response.oauthIdToken,
                    rawUserInfo     = Response.rawUserInfo,
                    kind            = Response.kind,
                ),
                Response.app,
                Response.create
            )
            for Response in Result
        ]
        return None
    
    @staticmethod
    def SelectByHexDigest(Email: str, app: int):
        DB      = Engine()
        Session = DB.Session()
        Response = Session.query(Sessions).filter_by(hexdigest = hashlib.md5(f'{Email}|{app}'.encode()).hexdigest()).first()
        Session.invalidate()
        Session.close()
        DB.Engine.dispose()
        if Response is not None: 
            return VerifyAuthResponse(
                dict(
                    email           = Response.email,
                    federatedId     = Response.federatedId,
                    providerId      = Response.providerId,
                    emailVerified   = Response.emailVerified,
                    localId         = Response.localId,
                    idToken         = Response.idToken,
                    refreshToken    = Response.refreshToken,
                    expiresIn       = Response.expiresIn,
                    oauthIdToken    = Response.oauthIdToken,
                    rawUserInfo     = Response.rawUserInfo,
                    kind            = Response.kind,
                ),
                Response.app,
                Response.create
            )
        return None
    
    @staticmethod
    def DeleteBy(Email: str):
        DB      = Engine()
        Session = DB.Session()
        Result = Session.query(Sessions).filter_by(email = Email).delete()
        Session.commit()
        Session.invalidate()
        Session.close()
        DB.Engine.dispose()
        return Result
    
    @staticmethod
    def DeleteById(id: int):
        DB      = Engine()
        Session = DB.Session()
        Result = Session.query(Sessions).filter_by(id = id).delete()
        Session.commit()
        Session.invalidate()
        Session.close()
        DB.Engine.dispose()
        return Result
    
    @staticmethod
    def DeleteByEmailApp(email: str, app: int):
        DB      = Engine()
        Session = DB.Session()
        Result = Session.query(Sessions).filter_by(email = email, app = app).delete()
        Session.commit()
        Session.invalidate()
        Session.close()
        DB.Engine.dispose()
        return Result
    
    @staticmethod
    def SelectById(id: int):
        DB      = Engine()
        Session = DB.Session()
        Response = Session.query(Sessions).filter_by(id = id).first()
        Session.invalidate()
        Session.close()
        DB.Engine.dispose()
        if Response is not None: 
            return VerifyAuthResponse(
                dict(
                    email           = Response.email,
                    federatedId     = Response.federatedId,
                    providerId      = Response.providerId,
                    emailVerified   = Response.emailVerified,
                    localId         = Response.localId,
                    idToken         = Response.idToken,
                    refreshToken    = Response.refreshToken,
                    expiresIn       = Response.expiresIn,
                    oauthIdToken    = Response.oauthIdToken,
                    rawUserInfo     = Response.rawUserInfo,
                    kind            = Response.kind,
                ),
                Response.app,
                Response.create
            )
        return None