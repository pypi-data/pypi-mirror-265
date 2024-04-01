import json, os
import random
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

from .response import ProxyResponse

__Base_Sessions__ = declarative_base()

class Sessions(__Base_Sessions__):
        
    __tablename__   = 'Sessions'
    ID                  = Column(INTEGER(), primary_key=True)
    IpPort              = Column(VARCHAR(255), unique=True, nullable=False)
    username            = Column(VARCHAR(255), nullable=False)
    password            = Column(VARCHAR(255), nullable=False)
    proxy_address       = Column(VARCHAR(255), nullable=False)
    port                = Column(INTEGER(), nullable=False)
                
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.__dict__})'
        
    @property
    def toJson(self):
        return self.__dict__

def BaseMetaData() -> MetaData:
    return __Base_Sessions__.metadata

class Engine:
    def __init__(self) -> None:
        #dbschema = 'evm,solana,public'
        if os.path.exists('Session') is False: os.mkdir('Session')
        self.Engine = create_engine(f'sqlite:///Session/Proxys.sqlite', echo=False, pool_pre_ping=True)
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

class Proxys:
    
    @staticmethod
    def InsertMassal(response: List[ProxyResponse]):
        
        try:
            DB      = Engine()
            Session = DB.Session()
            Session.add_all(
                [
                    Sessions(
                        IpPort              = Response.IpPort,
                        username            = Response.username,
                        password            = Response.password,
                        proxy_address       = Response.proxy_address,
                        port                = Response.port,
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
    def Insert(Response: ProxyResponse):
        try:
            DB      = Engine()
            Session = DB.Session()
            Session.add(Sessions(
                IpPort              = Response.IpPort,
                username            = Response.username,
                password            = Response.password,
                proxy_address       = Response.proxy_address,
                port                = Response.port,
            ))
            Session.commit()
            Session.invalidate()
            Session.close()
            DB.Engine.dispose()
            return True
        except IntegrityError: return False
    
    @staticmethod
    def Select():
        DB      = Engine()
        Session = DB.Session()
        Result = Session.query(Sessions).filter().all()
        Session.invalidate()
        Session.close()
        DB.Engine.dispose()
        if len(Result) != 0: return [ProxyResponse(R.toJson) for R in Result]
        return None
    
    @staticmethod
    def Random():
        DB      = Engine()
        Session = DB.Session()
        Result = Session.query(Sessions).filter().all()
        Session.invalidate()
        Session.close()
        DB.Engine.dispose()
        if len(Result) != 0: return random.choice([ProxyResponse(R.toJson) for R in Result])
        return None
    
    @staticmethod
    def SelectBy(IpPort: str):
        DB      = Engine()
        Session = DB.Session()
        Result = Session.query(Sessions).filter_by(IpPort = IpPort).first()
        Session.invalidate()
        Session.close()
        DB.Engine.dispose()
        if Result is not None: return ProxyResponse(Result.toJson)
        else: return None
        
    @staticmethod
    def Update(IpPort: str, Data: dict):
        DB      = Engine()
        Session = DB.Session()
        Result  = Session.query(Sessions).filter_by(IpPort = IpPort).update(Data)
        Session.commit()
        Session.invalidate()
        Session.close()
        DB.Engine.dispose()
        return Result

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
    def Delete(IpPort: str):
        DB      = Engine()
        Session = DB.Session()
        Result = Session.query(Sessions).filter_by(IpPort = IpPort).delete()
        Session.commit()
        Session.invalidate()
        Session.close()
        DB.Engine.dispose()
        return Result
    
    @staticmethod
    def DeleteAll():
        DB      = Engine()
        Session = DB.Session()
        Result = Session.query(Sessions).filter().delete()
        Session.commit()
        Session.invalidate()
        Session.close()
        DB.Engine.dispose()
        try:
            if os.path.exists('Session/Proxys.sqlite'):
                os.unlink('Session/Proxys.sqlite')
        except: pass
        return Result