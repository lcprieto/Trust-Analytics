#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 11:25:41 2017

@author: Luis Carlos Prieto
luisc.prieto@gmail.com
"""


import log
import pymongo
import ta_ConfigManager



class MongoDB(object):
    #Clase con la que gestionaremos las consultas a MongoDB
    
    miLog       = log.Log
    m_db        = pymongo.database
    m_ListaJSON = []
    miConf = ta_ConfigManager.Configuracion
 
#------------------------------------------------------------------------------------------------------------------------------
           
    def __init__(self):
        
        self.miLog = log.Log()
        self.miLog.Salida("Cargando Gestor de MongoDB...")  
        
        try:
            self.miConf = ta_ConfigManager.Configuracion()
            self.Conectar()
            self.miLog.Salidaln("OK") 
        except ValueError:
            self.miLog.Salidaln( "ERROR - Cargando Gestor de MongoDB")
            return -1
 
#------------------------------------------------------------------------------------------------------------------------------
           
    def Conectar(self):
        # Conectamos con MongoDB en Azure...
        self.miLog.Salida("Conectando con MongoDB en Azure......")
        try:       
            self.miLog.Salida("Conectando...")       
            self.m_db =  pymongo.MongoClient(self.miConf.m_uri_Mongodb).get_database("ta-mrw")
            self.miLog.Salidaln("MongoDB OK")
        except Exception as e:
            self.miLog.Salidaln (" ERROR Conectando a Mongo Azure- ..." )
            self.miLog.Salidaln(e.args)
            return -1
 
#------------------------------------------------------------------------------------------------------------------------------
           
    def CargarJSON (self):
        self.miLog.Salida ("Cargando JSON desde MongoDB de Azure...")
        try:       
            
            self.m_ListaJSON = self.m_db.timeline.find()
            self.miLog.Salida ("Obtenidos " + str(self.m_ListaJSON.count()) + " Tweets...")                
            self.miLog.Salidaln("OK") 
        except ValueError:
            self.miLog.Salidaln( "ERROR - Cargando JSON desde MongoDB")
            return -1
			
#------------------------------------------------------------------------------------------------------------------------------			

    def CargarJSONOK (self):
            self.miLog.Salida ("Cargando JSON OK desde MongoDB de Azure...")
            try:       
                
                self.m_ListaJSON = self.m_db.timeline.find({"place" : {'$eq': 'OK'}})
                self.miLog.Salida ("Obtenidos " + str(self.m_ListaJSON.count()) + " Tweets...")                
                self.miLog.Salidaln("OK") 
            except ValueError:
                self.miLog.Salidaln( "ERROR - Cargando JSON desde MongoDB")
            return -1
        
        
    def CargarJSONNULL (self):
            self.miLog.Salida ("Cargando JSON NULL desde MongoDB de Azure...")
            try:       
                
                self.m_ListaJSON = self.m_db.timeline.find({"place" : {'$eq': 'null'}})
                self.miLog.Salida ("Obtenidos " + str(self.m_ListaJSON.count()) + " Tweets...")                
                self.miLog.Salidaln("OK") 
            except ValueError:
                self.miLog.Salidaln( "ERROR - Cargando JSON desde MongoDB")
            return -1
			
#------------------------------------------------------------------------------------------------------------------------------			
			
    def CargarJSONParcial (self):
        self.miLog.Salida ("Cargando Parcial de JSON desde MongoDB de Azure...")
        try:       
          
                        
            self.miLog.Salida ("Buscando nuevas entradas...")
            self.m_ListaJSON = self.m_db.timeline.find({"place" : {'$ne': 'OK'}})
            self.miLog.Salidaln(" OK...") 
            #self.miLog.Salidaln ("Obtenidos " + str(len(self.m_ListaJSON)) + " Tweets no gestionados previamente...")                
            
			
        except Exception as e:
            self.miLog.Salidaln( "ERROR - Cargando JSON Parciales desde MongoDB ")
            self.miLog.Salidaln(e.args)
            return -1
			
#------------------------------------------------------------------------------------------------------------------------------			
			
    def CerrarJSONParcial (self, Lista):
        self.miLog.Salidaln("")
        self.miLog.Salidaln("Marcando Parcial de JSON a MongoDB de Azure...")
        try:                 
            i = 0
            for Dato in Lista:
                i = i + 1                         
                self.m_db.timeline.update({'id_str': Dato.m_idTweet},{'$set': {'place': 'OK'}}, multi=True, upsert=False)
                self.miLog.Salida(".")
            self.miLog.Salidaln("")
            self.miLog.Salida ("Marcados " + str(i) + " Tweets no gestionados previamente...")                
            self.miLog.Salidaln("OK") 
			
        except Exception as e :
              self.miLog.Salidaln( "ERROR - Marcando JSON Parciales a MongoDB")
              self.miLog.Salidaln(e.args)
              return -1
#------------------------------------------------------------------------------------------------------------------------------			
          
    def BorrarParcial (self, Lista):
        self.miLog.Salidaln("")
        self.miLog.Salidaln("Borrado de los parciales de JSON a MongoDB de Azure...")
        try:                 
            i = 0
            for Dato in Lista:
                i = i + 1                         
                self.m_db.timeline.update({'id_str': Dato.m_idTweet},{'$set': {'place': 'null'}},multi=True,  upsert=False)
                self.miLog.Salida(".")
            self.miLog.Salidaln("")
            self.miLog.Salida ("Marcados " + str(i) + " Tweets...")                
            self.miLog.Salidaln("OK") 
			
        except Exception as e :
              self.miLog.Salidaln( "ERROR - Borrando Parciales JSON Parciales a MongoDB")
              self.miLog.Salidaln(e.args)
              return -1
          
            
    def PonerParcial (self, Lista):
        self.miLog.Salidaln("")
        self.miLog.Salidaln("Set de los parciales de JSON a MongoDB de Azure...")
        try:                 
            i = 0
            for Dato in Lista:
                i = i + 1                         
                self.m_db.timeline.update({'id_str': Dato.m_idTweet},{'$set': {'place': 'OK'}}, multi=True, upsert=False)
                self.miLog.Salida(".")
            self.miLog.Salidaln("")
            self.miLog.Salida ("Marcados " + str(i) + " Tweets...")                
            self.miLog.Salidaln("OK") 
			
        except Exception as e :
              self.miLog.Salidaln( "ERROR - Poniendo Parciales JSON Parciales a MongoDB")
              self.miLog.Salidaln(e.args)
              return -1
            
