# -*- coding: utf-8 -*-
"""
Created on Wed May  3 17:25:53 2017

@author: Luis Carlos Prieto
luisc.prieto@gmail.com
"""

import configparser
import log


class Configuracion(object):
    #Clase con la que gestionaremos los scripts
    miLog = ""
    config = ""
    
    # Variables de Tweeter
    m_tweeter_consumer_key = ""
    m_tweeter_consumer_secret = ""
    m_tweeter_access_key = ""
    m_tweeter_access_secret = ""
    m_tweeter_query = ""
    m_tweeter_lang = ""
    
    # Variables de MongoDB
    m_uri_Mongodb = ""
    
    # Variables SQL Server
    m_serverSQL = ""
    m_userSQL = ""
    m_siteSQL = ""
    m_passwordSQL = ""
    m_databaseSQL = ""
    
    # Variables ML1
    m_ML1_APIKey = ""
    
    # Variables ML2
    m_FicheroML2Training = ""
    m_FicheroML2Test = ""
    m_Palabras = ""
    m_PalabrasML2 = ""
    m_Emoticonos = ""
    m_UbicacionModelos = ""
    m_UbicacionWord2Vec = ""

    
            
    def __init__(self):
        
        self.miLog = log.Log()
        self.miLog.Salida("Cargando INI...")      
        
        try:
            self.config = configparser.ConfigParser()

            self.config.read('sys/config.ini')
            self.miLog.Salida("Leyendo Parámetros INI...") 

            # Leyendo Parametros Tweeter
            self.m_tweeter_consumer_key = self.config.get("TwitterAPIcredentials", "consumer_key")
            self. m_tweeter_consumer_secret = self.config.get("TwitterAPIcredentials", "consumer_secret")
            self.m_tweeter_access_key = self.config.get("TwitterAPIcredentials", "access_key")
            self.m_tweeter_access_secret = self.config.get("TwitterAPIcredentials", "access_secret")
            
            self.m_tweeter_query = self.config.get("TwitterSearchItems", "query")
            self.m_tweeter_lang = self.config.get("TwitterSearchItems", "lang")
    
            # Leyendo Parámetros SQL
            self.m_serverSQL = self.config.get("SQLServer", "server")
            self.m_userSQL = self.config.get("SQLServer", "user")
            self.m_siteSQL = self.config.get("SQLServer", "site")
            self.m_passwordSQL = self.config.get("SQLServer", "password")
            self.m_databaseSQL = self.config.get("SQLServer", "database")
            
            # Leyendo Parámetros MongoDB
            self.m_uri_Mongodb = self.config.get("MongoDB", "uri")
            
            # Leyendo Parámetros ML1
            self.m_ML1_APIKey = self.config.get("ML1", "ML1_APIKey")
            
            # Leyendo Parámetros ML2
            self.m_FicheroML2Training = self.config.get("ML2", "FicheroTraining")
            self.m_FicheroML2Test     = self.config.get("ML2", "FicheroTest")
            self.m_Palabras           = self.config.get("ML2", "Palabras")
            self.m_PalabrasML2        = self.config.get("ML2", "PalabrasML2")
            self.m_Emoticonos         = self.config.get("ML2", "Emoticonos")
            self.m_UbicacionModelos   = self.config.get("ML2", "UbicacionModelos")
            self.m_UbicacionWord2Vec   = self.config.get("ML2", "UbicacionWord2Vec")
            
            self.miLog.Salidaln("OK") 
        except ValueError:
            self.miLog.Salidaln( "ERROR - Leyendo Config.ini")
            return -1

  