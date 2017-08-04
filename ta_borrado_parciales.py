# -*- coding: utf-8 -*-
"""
Created on Fri May 19 11:30:30 2017

@author: lcprieto
"""


import log

import ta_MongoDB

import ta_DataCleaner


def main():
     
    # Variables Generales...
    Errores = 0   
    miLog = log.Log()
    GestorMongoDB = ta_MongoDB.MongoDB
    
    
    miLog.Salidaln("Bienvenido al Manager de  borrado de PARCIALES de MBIT, Iniciando servicios...")
    
    GestorMongoDB = ta_MongoDB.MongoDB()
    
    
    
        
    try:
		  #Una vez aseguradas las conexiones a BBDD, cargamos los Tweets en formato JSON
        GestorMongoDB.CargarJSONOK()
                
        # Creación del DataCleaner y Volcados a SQL Server
        DataCleaner = ta_DataCleaner.DataCleaner(GestorMongoDB.m_ListaJSON)
        DataCleaner.CargaTimeline()
        
		
        # Marcamos los tweets ya cargados para reducir la carga de parciales desde Mongo Azure

        GestorMongoDB.BorrarParcial(DataCleaner.m_ListaTimeline)         

        
    except Exception as e:
        Errores += 1
        miLog.Salidaln("ERROR Borrando Parciales")
        miLog.Salidaln(e.args)
        
    
    if (Errores > 0 ):
        miLog.Salidaln("ERRORES DETECTADOS")
    else:
        miLog.Salidaln("Proceso finalizado con exito...")
        
        
    
    
    
main()
    
    