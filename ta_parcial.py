# -*- coding: utf-8 -*-
"""
Created on Fri May 19 11:30:30 2017

@author: Luis Carlos Prieto
luisc.prieto@gmail.com
"""


import log

import ta_MongoDB
import ta_SQLServer

import ta_DataCleaner
#import ta_twitter


def main():
     
    # Variables Generales...
    Errores = 0   
    miLog = log.Log()
    GestorMongoDB = ta_MongoDB.MongoDB
    GestorSQLServer = ta_SQLServer.SQLServer
    #GestorTwitter = ta_twitter.Twitter
    
    miLog.Salidaln("Bienvenido al Manager de  carga PARCIAL de MBIT, Iniciando servicios...")
    
    GestorMongoDB = ta_MongoDB.MongoDB()
    
    #GestorTwitter = ta_twitter.Twitter(GestorMongoDB.m_db)
    #GestorTwitter.BuscarNuevos()
    
    
    try:
        # Creación del -Gestor de SQL Server
        GestorSQLServer = ta_SQLServer.SQLServer()
         
    except Exception as e:
        Errores += 1
        miLog.Salidaln("ERROR generando Gestor de SQL Server..." )
        miLog.Salidaln(e.args)
        return -1
        
    try:
		  #Una vez aseguradas las conexiones a BBDD, cargamos los Tweets en formato JSON
        GestorMongoDB.CargarJSONParcial()
                
        # Creación del DataCleaner y Volcados a SQL Server
        DataCleaner = ta_DataCleaner.DataCleaner(GestorMongoDB.m_ListaJSON)
        
        DataCleaner.AnalisisTweetsParcial()
       
        GestorSQLServer.ParcialTwiteros(DataCleaner.m_ListaTwiteros)
        GestorSQLServer.ParcialTimeline(DataCleaner.m_ListaTimeline)
		
        # Marcamos los tweets ya cargados para reducir la carga de parciales desde Mongo Azure

        GestorMongoDB.CerrarJSONParcial(DataCleaner.m_ListaTimeline)         
        GestorSQLServer.m_conSQL.close()
        
    except Exception as e:
        Errores += 1
        miLog.Salidaln("ERROR No se ha podido generar DataCleaner ")
        miLog.Salidaln(e.args)
        
    
    if (Errores > 0 ):
        miLog.Salidaln("ERRORES DETECTADOS")
    else:
        miLog.Salidaln("Proceso finalizado con exito...")
        
        
    
    
    
main()
    
    