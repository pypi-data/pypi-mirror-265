from typing import Any, List, Dict
from pydantic import BaseModel, EmailStr, HttpUrl, PrivateAttr
from enum import Enum


class ITipoEnum(str, Enum):
    FISICA = "F"
    GIURIDICA = "G"

class IPersona(BaseModel):
    tipo: str
    codice: str
    nome: str | None
    cognome: str | None
    denominazione: str | None = None
    indirizzo: str | None = None
    civico: str | None = None
    cap: str | None = None
    localita: str | None = None
    provincia: str | None = None
    nazione: str | None = None
    email: str | None
    
class IImporto(BaseModel):
    codice: str
    descrizione: str | None = None
    importo: float
    capitolo: str | None = None
    
class IDebito(BaseModel):
    idpos: str #max 256
    codice: str | None = None
    dettaglio: str #max 1000
    iddeb: str #univoco max 256
    gruppo: str | None = None
    ordinamento: int | None = None
    data_inizio: str
    data_fine: str | None = None
    data_limite: str | None = None
    importo: float
    causale: str # max 140 
    importi: list[IImporto]
    
class IPagoPa(BaseModel):
    soggetto: IPersona
    debito: IDebito
    debito_xml:str | None = None
    numero_avviso: str | None = None
    
class IEsito(BaseModel):
    esito: str
    errore: str | None = None
    descrizione: str | None = None

    

    
class IConfig(BaseModel):
    wsUrl: str
    wsUser: str
    wsPassword: str
    codiceIpa: str
    codiceServizio: str
    codiceTipoDebito: str
    FAKE: bool = False
    FAKE_ERROR: str = ""
    
class BaseRet(BaseModel):
    lngErrNumber: int = 0
    strErrString: str = ''

class ILoginRet(BaseRet):
    strDST: str | None
    
class IResult(BaseRet):
    lngNumPG: int = 0
    lngAnnoPG: int = 0
    strDataPG: str = ''
    lngDocID: int = 0

    


class IDocumento(BaseModel):
    id: int | None
    descrizione: str
    tipo: str
    nome: str
    content: Any
    size: int
    mimetype: str
    ext: str


class IUser(BaseModel):
    username: str
    password: str

class IAmministrazione(BaseModel):
    Denominazione: str
    CodiceAOO: str
    CodiceEnte: str
    IndirizzoTelematico: EmailStr

class IFascicolo(BaseModel):
    numero: str
    anno:str
    
class IParametro(BaseModel):
    nome: str
    valore: str

class IProtocolloBase(BaseModel):
    Soggetto: List[IPersona]
    Flusso: str = 'E'
    Oggetto: str | None
    Titolario: str | None
    UO: str   | None
    Fascicolo: IFascicolo | None
    NumeroRegistrazione: str = '0'
    DataRegistrazione: str = '0'
    Parametri: List[IParametro]

class IProtocollo(IProtocolloBase):
    Amministrazione: IAmministrazione
    Principale: IDocumento
    Allegati: List[IDocumento]
    Applicativo: str = 'AGSPR'


class IMessageData(BaseModel):
    pass


