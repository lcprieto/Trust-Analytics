# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 09:55:30 2017

@author: Luis Carlos Prieto
luisc.prieto@gmail.com
"""

import urllib.request
import json
import ta_SQLServer
import ta_ConfigManager
import log

           

def main():
    
   
    
    
    
     # Variables Generales...
    Errores = 0   
    miLog = log.Log()
    GestorSQLServer = ta_SQLServer.SQLServer
    miConf = ta_ConfigManager.Configuracion()
    m_esBusiness = 0
        
    miLog.Salidaln("Bienvenido al Manager de  esBusiness, Iniciando servicios...")
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
        GestorSQLServer.ListaTweetsBusiness(Lista)
    except Exception as e:
        Errores += 1
        miLog.Salidaln("ERROR No se ha podido generar EsBsuness... ")
        miLog.Salidaln(e.args)
        
    miLog.Salidaln("OK.")
        
    for Elemento in Lista:
        try:
            #miLog.Salida("B")
            Dato = {"Inputs": {"input1":[{'idTweet': "" + Elemento.m_idTweet + "",'idUsuario': "" + Elemento.m_idUsuario + "",'esBusiness': "",'Texto': "" + Elemento.m_Texto + "",}],},"GlobalParameters":  {}}
            
            #miLog.Salida("\bC")
            body = str.encode(json.dumps(Dato))      
            
            #miLog.Salida("\bW")
            url = 'https://europewest.services.azureml.net/subscriptions/561a3040473c45e9bec4ce3b0751236e/services/71a40c7296094c8a8014a6b39187a31e/execute?api-version=2.0&format=swagger'
            api_key = miConf.m_ML1_APIKey
            headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
            
            #miLog.Salida("\bR")
            req = urllib.request.Request(url, body, headers)
    
            try:
                
                #miLog.Salida("\bA")
                response = urllib.request.urlopen(req)
            
                #miLog.Salida("\bB")            
                result = response.read()
                Salida = json.loads(result)
                
                if (Salida["Results"]["output1"][0]["esBusiness"] == 'True'):
                    m_esBusiness = 1
                else:
                    m_esBusiness = 0
                
                GestorSQLServer.ActualizaEsBusiness(Salida["Results"]["output1"][0]["idTweet"],m_esBusiness)
                
            except urllib.error.HTTPError as error:
                Errores +=1
                miLog.Salidaln("ERROR Web Service ML1 con status code: " + str(error.code))
                miLog.Salidaln("Datos Request: " + str(Dato))
                miLog.Salidaln(error.info())
                miLog.Salidaln(json.loads(error.read().decode("utf8", 'ignore'))) 
            
        except :
            miLog.Salida("E")



main()