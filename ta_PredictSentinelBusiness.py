# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 09:23:49 2017

@author: Luis Carlos Prieto
"""




import gensim

import log
import ta_SQLServer
import ta_DataCleaner
import pandas as pd

def main():
     # Variables Generales...
    Errores = 0   
    miLog = log.Log()
    m_DatosTwitter = ta_DataCleaner.DatosTwitter()
    GestorSQLServer = ta_SQLServer.SQLServer
        
    miLog.Salidaln("Bienvenido al Manager de  Sentinel Business, Iniciando servicios ML2...")
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
	    
        GestorSQLServer.ListaTweetsSentinelBusiness(Lista)
        miLog.Salidaln("Cargendo Datos...")
        m_DatosTwitter.CargarDatos(GestorSQLServer.m_conSQL)
    
        
    except Exception as e:
        Errores += 1
        miLog.Salidaln("ERROR No se ha podido generar Sentinel de Business... ")
        miLog.Salidaln(e.args)
        
    miLog.Salidaln("OK.")
    

    
    miLog.Salida("construyendo Features ML2 ...")
    m_DatosTwitter.build_features()
    miLog.Salidaln("OK...")



    miLog.Salida("Limpiando ML2 ...")
    m_DatosTwitter.Limpieza()
    miLog.Salida("OK ...")
    
        
    miLog.Salida("Tokenizando ...")
    m_DatosTwitter.Tokenizar()
    m_DatosTwitter.ConstruirPalabras()
    m_DatosTwitter.ContarPalabras()
    m_DatosTwitter.Separar()
    miLog.Salidaln("OK ...")   
    
    #m_DatosTwitter.ConstruirMatrizEntrenamiento()
        
    miLog.Salida("Recuperando Negaciones ...")
    m_DatosTwitter.RecuperarNegaciones()
    miLog.Salidaln("OK ...")
    
    
    miLog.Salida("Construyendo modelo ...")
    ModeloDatos, Etiquetas = m_DatosTwitter.build_data_model()
    miLog.Salidaln("OK ...")
       
    
    miLog.Salidaln("Business ...")
    Prediccion_RF = pd.DataFrame
    Prediccion_NB = pd.DataFrame
    Prediccion_SV = pd.DataFrame
    Prediccion_SD = pd.DataFrame
    Prediccion_PE = pd.DataFrame
    
    
    
    Prediccion_RF = m_DatosTwitter.BusinessRandomForest()    
    Prediccion_NB = m_DatosTwitter.BusinessNaiveBayes()
    Prediccion_SV = m_DatosTwitter.BusinessSVM()
    Prediccion_SD = m_DatosTwitter.BusinesDescensoGradiente()
    Prediccion_PE = m_DatosTwitter.BusinesPerceptron()
        
    
    Tamano = Prediccion_RF.size
    for i in range(0, Tamano):
        #miLog.Salidaln("--------------------------------")
        #miLog.Salidaln("idTweet : " + m_DatosTwitter.Datos_Procesados.loc[i, "idtweet"])
        #miLog.Salidaln("Texto   : " + m_DatosTwitter.Datos_Procesados.loc[i, "texto_original"])
        #miLog.Salidaln("RF      :" + Prediccion_RF[i])
        #miLog.Salidaln("NB      :" + Prediccion_NB[i])
        Resultado = 'neutro'
        if (Prediccion_PE[i] == 'positivo'): Resultado = 'positivo' 
        if (Prediccion_PE[i] == 'negativo'): Resultado = 'negativo'
        if (Prediccion_PE[i] == 'neutro'):  
            if (Prediccion_RF[i] == 'negativo' ): Resultado = 'negativo' 
            if (Prediccion_RF[i] == 'positivo' ): Resultado = 'positivo'
            if (Prediccion_RF[i] == 'neutro' ): 
                if (Prediccion_NB[i] == 'positivo'): Resultado = 'positivo'
                if (Prediccion_NB[i] == 'negativo' ): Resultado = 'negativo'
                if (Prediccion_NB[i] == 'neutro' ): 
                    if (Prediccion_SD[i] == 'negativo'): Resultado = 'negativo'
                    if (Prediccion_SD[i] == 'positivo'): Resultado = 'positivo'
                    if (Prediccion_SD[i] == 'neutro'): 
                        if (Prediccion_SV[i] == 'negativo'): 
                            Resultado = 'negativo'
                        else:
                            if (Prediccion_SV[i] == 'positivo'): 
                                Resultado = 'positivo'
                            else:
                                Resultado = 'neutro'
                            
        
        #miLog.Salidaln("----->  :" + Resultado)
        
        
        GestorSQLServer.UpdateSentibelBusiness(m_DatosTwitter.Datos_Procesados.loc[i, "idtweet"],Resultado)

        

    miLog.Salidaln("OK ...")
    
    
    
    
    if (Errores > 0 ):
        miLog.Salidaln("ERRORES DETECTADOS")
    else:
        miLog.Salidaln("Proceso finalizado con exito...")

main()
