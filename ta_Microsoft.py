# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 13:49:12 2017

@author: Luis Carlos Prieto
"""

import log
import ta_SQLServer
import urllib
from urllib.request import urlopen
from urllib.request import Request

import sys
import base64
import json
import pymongo



def main():
     
    # Variables Generales...
    Errores = 0   
    miLog = log.Log()
    GestorSQLServer = ta_SQLServer.SQLServer
        
    miLog.Salidaln("Bienvenido al Manager de  Sentinel Microisoft, Iniciando servicios...")
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
		 
        
        
        GestorSQLServer.ListaTweetsMicrosoft(Lista)
        
        
    except Exception as e:
        Errores += 1
        miLog.Salidaln("ERROR No se ha podido generar Sentinel de Microsoft... ")
        miLog.Salidaln(e.args)
        
    miLog.Salidaln("OK.")

  
    
      # Azure portal URL.
    base_url = 'https://westus.api.cognitive.microsoft.com/'
    # Your account key goes here.
    
    account_key = '<YOUR KEY>'
    
    headers = {'Content-Type':'application/json', 'Ocp-Apim-Subscription-Key':account_key}    
    
    
    
    
    
    # Instanciamos el Cliente Google
              
    
    miLog.Salidaln("Analizando Sentinel... " + str(len(Lista)) + " elementos..." )
    for Elemento in Lista:
        try:
            
            miLog.Salida("C")           
            CadenaLimpia = Elemento.m_Texto
            CadenaLimpia = CadenaLimpia.replace("'",'-')
            CadenaLimpia = CadenaLimpia.replace('"','-')
            
            miLog.Salida("\bA")
            TextoPorAnalizar = '{"documents":[{"id":"' + Elemento.m_idTweet + '","text":"' + CadenaLimpia + '"},]}'
            
            # Calculamos el Sentinel de Microsoft.
            miLog.Salida("\bS")
            Sentimiento_url = base_url + 'text/analytics/v2.0/sentiment'
            reqSentinel = Request(Sentimiento_url, TextoPorAnalizar.encode("utf-8"), headers) 
            RespuestaSentinel = urlopen(reqSentinel)
            ResultadoSentinel = RespuestaSentinel.read()
            objSentinel = json.loads(ResultadoSentinel)
            AnalisisSentinel = objSentinel['documents'][0]
            Elemento.SentinelMicrosoft = AnalisisSentinel['score']
            
            # Detectamos las palabras clave.
            miLog.Salida("\bF")
            Frases_url = base_url + 'text/analytics/v2.0/keyPhrases'
            reqFrases = Request(Frases_url, TextoPorAnalizar.encode("utf-8"), headers) 
            RespuestaFrases = urlopen(reqFrases)
            ResultadoFrases = RespuestaFrases.read()
            objFrases = json.loads(ResultadoFrases)
            AnalisisFrases=objFrases['documents'][0]
            
            Elemento.m_Frases = str(AnalisisFrases['keyPhrases'])
            
            
           
            miLog.Salida("\b.")
        except :
            miLog.Salida("\bE")
    
    miLog.Salidaln("OK.")
    
        
    
    if (Errores == 0):
        GestorSQLServer.ActualizaSentinelMicrosoft(Lista)
    
    GestorSQLServer.m_conSQL.close()
    
    
    if (Errores > 0 ):
        miLog.Salidaln("ERRORES DETECTADOS")
    else:
        miLog.Salidaln("Proceso finalizado con exito...")
        
  
    
    
    
main()

















