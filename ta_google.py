# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 10:36:16 2017

@author: Luis Carlos Prieto
"""


import log
import ta_SQLServer
from google.cloud import language


def main():
     
    # Variables Generales...
    Errores = 0   
    miLog = log.Log()
    GestorSQLServer = ta_SQLServer.SQLServer
        
    miLog.Salidaln("Bienvenido al Manager de  Sentinel Google, Iniciando servicios...")
    Lista =  []
    
    try:
        # Creación del -Gestor de SQL Server
        GestorSQLServer = ta_SQLServer.SQLServer()
         
    except Exception as e:
        Errores += 1
        miLog.Salidaln("ERROR generando Gestor de SQL Server..." )
        miLog.Salidaln(e.args)
        return -1
        
    try:
		 
        
        
        GestorSQLServer.ListaTweetsGoogle(Lista)
        
        
    except Exception as e:
        Errores += 1
        miLog.Salidaln("ERROR No se ha podido generar Sentinel de Google... ")
        miLog.Salidaln(e.args)
        
    miLog.Salidaln("OK.")
    
    
    # Instanciamos el Cliente Google
    miLog.Salida("Instanciando idioma Google... ")
            
    miLog.Salidaln("OK")
    miLog.Salidaln("Analizando Sentinel... " + str(len(Lista)) + " elementos..." )
    for Elemento in Lista:
        try:
            language_client = language.Client( )
            #miLog.Salida("C")
            CadenaLimpia = Elemento.m_Texto
            CadenaLimpia = CadenaLimpia.replace("'",'-')
            CadenaLimpia = CadenaLimpia.replace('"','-')
            
            #miLog.Salida("\bG")
            documentGoogle = language_client.document_from_text(CadenaLimpia)          
            #miLog.Salida("\bS")
            sentimentGoogle = documentGoogle.analyze_sentiment().sentiment
            
            #Elemento.m_SentinelGoogle = sentimentGoogle.score
            #Elemento.m_AccuracyGoogle = sentimentGoogle.magnitude
            GestorSQLServer.ActualizaSentinelGoogleTweet(Elemento.m_idTweet,sentimentGoogle.score,sentimentGoogle.magnitude)
            
            
            
        except :
            miLog.Salida("E")
            GestorSQLServer.ActualizaSentinelGoogleTweet(Elemento.m_idTweet,0,0)
    
    miLog.Salidaln("OK.")
    
        
    
    #GestorSQLServer.ActualizaSentinelGoogle(Lista)
    
    GestorSQLServer.m_conSQL.close()
    
    
    if (Errores > 0 ):
        miLog.Salidaln("ERRORES DETECTADOS")
    else:
        miLog.Salidaln("Proceso finalizado con exito...")
        
        
    
    
    
main()
    












