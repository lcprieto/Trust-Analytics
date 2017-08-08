# -*- coding: utf-8 -*-
"""
Created on Wed May  3 12:01:58 2017

@author: Luis Carlos Prieto
luisc.prieto@gmail.com
"""

import log
import ta_MongoDB
import ta_SQLServer
import ta_DataCleaner


def main():
     
    # Variables Generales...
    Errores = 0   
    miLog = log.Log()
    GestorMongoDB = ta_MongoDB.MongoDB
    GestorSQLServer = ta_SQLServer.SQLServer
    miLog.Salidaln("Bienvenido al Manager MBIT, Iniciando servicios...")
   
        
    try:
        # Iniciamos el proceso...    
        # Creación del Gestor de MongoDB
        GestorMongoDB = ta_MongoDB.MongoDB()
        
    except Exception as e:
        Errores += 1
        miLog.Salidaln("ERROR generando Gestor de MongoDB")
        
    try:
        # Creación del -Gestor de SQL Server
        GestorSQLServer = ta_SQLServer.SQLServer()
         
    except Exception as e:
        Errores += 1
        miLog.Salidaln("ERROR generando Gestor de SQL Server..." + e.with_traceback)
        return -1
        
    try:
        #Una vez aseguradas las conexiones a BBDD, cargamos los Tweets en formato JSON
        GestorMongoDB.CargarJSON()
        
        # Creación del DataCleaner y Volcados a SQL Server
        DataCleaner = ta_DataCleaner.DataCleaner(GestorMongoDB.m_ListaJSON)
        
        DataCleaner.AnalisisTweets()
       
        GestorSQLServer.RegenerarTwiteros(DataCleaner.m_ListaTwiteros)
        GestorSQLServer.RegenerarTimeline(DataCleaner.m_ListaTimeline)
        
        GestorSQLServer.m_conSQL.close()
        
    except Exception as e:
        Errores += 1
        miLog.Salidaln("ERROR No se ha podido generar DataCleaner ")
        
    
    if (Errores > 0 ):
        miLog.Salidaln("ERRORES DETECTADOS")
    else:
        miLog.Salidaln("Proceso finalizado con exito...")
        
        
    
    
    
main()
