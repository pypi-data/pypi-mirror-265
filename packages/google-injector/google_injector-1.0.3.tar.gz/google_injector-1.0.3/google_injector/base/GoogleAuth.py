import json, os
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

from ..response import TokenResponse

__Base_Sessions__ = declarative_base()

class Sessions(__Base_Sessions__):
    
    __tablename__   = f'Session'
    id              = Column(INTEGER(), primary_key=True)
    Email           = Column(VARCHAR(255), unique=True, nullable=False)
    SID             = Column(TEXT(), nullable=False)
    LSID            = Column(TEXT(), nullable=False)
    Auth            = Column(TEXT(), nullable=False)
    Token           = Column(TEXT(), nullable=False)
    services        = Column(TEXT(), nullable=False)
    firstName       = Column(TEXT(), nullable=False)
    lastName        = Column(TEXT(), nullable=False)
    GooglePlusUpdate= Column(TEXT(), nullable=False)
    accountId       = Column(TEXT(), nullable=False)
    Password        = Column(TEXT(), nullable=False)
    deviceId        = Column(TEXT(), nullable=False)

def BaseMetaData() -> MetaData:
    return __Base_Sessions__.metadata

class Engine:
    def __init__(self) -> None:
        #dbschema = 'evm,solana,public'
        if os.path.exists('Session') is False: os.mkdir('Session')
        self.Engine = create_engine(f'sqlite:///Session/GoogleAuth.sqlite', echo=False, pool_pre_ping=True)
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

class GoogleAuth:
    
    @staticmethod
    def InsertMassal(response: List[TokenResponse]):
        
        try:
            DB      = Engine()
            Session = DB.Session()
            Session.add_all(
                [
                    Sessions(
                        Email           = Response.Email,
                        SID             = Response.SID,
                        LSID            = Response.LSID,
                        Auth            = Response.Auth,
                        Token           = Response.Token,
                        services        = Response.services,
                        firstName       = Response.firstName,
                        lastName        = Response.lastName,
                        GooglePlusUpdate= Response.GooglePlusUpdate,
                        accountId       = Response.accountId,
                        Password        = Response.Password,
                        deviceId        = Response.deviceId,
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
    def Insert(Response: TokenResponse):
        try:
            DB      = Engine()
            Session = DB.Session()
            Session.add(Sessions(
                Email           = Response.Email,
                SID             = Response.SID,
                LSID            = Response.LSID,
                Auth            = Response.Auth,
                Token           = Response.Token,
                services        = Response.services,
                firstName       = Response.firstName,
                lastName        = Response.lastName,
                GooglePlusUpdate= Response.GooglePlusUpdate,
                accountId       = Response.accountId,
                Password        = Response.Password,
                deviceId        = Response.deviceId,
            ))
            Session.commit()
            Session.invalidate()
            Session.close()
            DB.Engine.dispose()
            return True
        except IntegrityError: return False
    
    @staticmethod
    def Update(Response: TokenResponse):
        DB      = Engine()
        Session = DB.Session()
        Data    = Response.to_json; Data.pop('Email')
        Result  = Session.query(Sessions).filter_by(Email = Response.Email).update(Data)
        Session.commit()
        Session.invalidate()
        Session.close()
        DB.Engine.dispose()
        return Result
    
    @staticmethod
    def Select(offset: int = 0, limit: int = 100):
        DB      = Engine()
        Session = DB.Session()
        Result = Session.query(Sessions).filter().offset(offset).limit(limit).all()
        Session.invalidate()
        Session.close()
        DB.Engine.dispose()
        if len(Result) != 0: return [
            TokenResponse(
                dict(
                    Email           = Response.Email,
                    SID             = Response.SID,
                    LSID            = Response.LSID,
                    Auth            = Response.Auth,
                    Token           = Response.Token,
                    services        = Response.services,
                    firstName       = Response.firstName,
                    lastName        = Response.lastName,
                    GooglePlusUpdate= Response.GooglePlusUpdate,
                    accountId       = Response.accountId,
                ),
                password        = Response.Password,
                deviceId        = Response.deviceId,
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
        Response = Session.query(Sessions).filter_by(Email = Email).first()
        Session.invalidate()
        Session.close()
        DB.Engine.dispose()
        if Response is not None: 
            return TokenResponse(
                dict(
                    Email           = Response.Email,
                    SID             = Response.SID,
                    LSID            = Response.LSID,
                    Auth            = Response.Auth,
                    Token           = Response.Token,
                    services        = Response.services,
                    firstName       = Response.firstName,
                    lastName        = Response.lastName,
                    GooglePlusUpdate= Response.GooglePlusUpdate,
                    accountId       = Response.accountId,
                ),
                password        = Response.Password,
                deviceId        = Response.deviceId,
            )
        return None
    
    @staticmethod
    def DeleteBy(Email: str):
        DB      = Engine()
        Session = DB.Session()
        Result = Session.query(Sessions).filter_by(Email = Email).delete()
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
    def SelectById(id: int):
        DB      = Engine()
        Session = DB.Session()
        Response = Session.query(Sessions).filter_by(id = id).first()
        Session.invalidate()
        Session.close()
        DB.Engine.dispose()
        if Response is not None: 
            return TokenResponse(
                dict(
                    Email           = Response.Email,
                    SID             = Response.SID,
                    LSID            = Response.LSID,
                    Auth            = Response.Auth,
                    Token           = Response.Token,
                    services        = Response.services,
                    firstName       = Response.firstName,
                    lastName        = Response.lastName,
                    GooglePlusUpdate= Response.GooglePlusUpdate,
                    accountId       = Response.accountId,
                ),
                password        = Response.Password,
                deviceId        = Response.deviceId,
            )
        return None