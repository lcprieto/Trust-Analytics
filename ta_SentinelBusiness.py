# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 09:23:49 2017

@author: Luis Carlos Prieto
"""





import log
import ta_ConfigManager
import ta_DataCleaner


def main():
     # Variables Generales...
    Errores = 0   
    miLog = log.Log()
    m_DatosTwitter = ta_DataCleaner.DatosTwitter()
    miConf = ta_ConfigManager.Configuracion()
    
    miLog.Salida("Lanzando proceso ML2 ...")
    m_DatosTwitter.Iniciar(miConf.m_FicheroML2Training)
    miLog.Salidaln("OK ...")

    miLog.Salida("construyendo Features ML2 ...")
    m_DatosTwitter.build_features()
    miLog.Salidaln("OK...")

    miLog.Salida("Limpiando ML2 ...")
    m_DatosTwitter.Limpieza()
    miLog.Salida("OK ...")
    
    miLog.Salida("Tokenizando ...")
    m_DatosTwitter.Tokenizar()
    m_DatosTwitter.Separar()
    miLog.Salidaln("OK ...")   
        
    miLog.Salida("Construyendo lista de palagras ...")
    m_DatosTwitter.ConstruirPalabras()
    miLog.Salidaln("OK ...")
    
    miLog.Salida("Contando Palabras ...")
    m_DatosTwitter.ContarPalabras()
    miLog.Salidaln("OK ...")
    
    miLog.Salida("Recuperando Negaciones ...")
    m_DatosTwitter.RecuperarNegaciones()
    miLog.Salidaln("OK ...")
    
    
    miLog.Salida("Construyendo modelo ...")
    ModeloDatos, Etiquetas = m_DatosTwitter.build_data_model()
    miLog.Salidaln("OK ...")
     
    miLog.Salidaln("Random Forest ...")
    m_DatosTwitter.RandomForest()
    miLog.Salidaln("OK ...")
     
    miLog.Salidaln("Naive Bayes ...")
    m_DatosTwitter.NaiveBayes()
    miLog.Salidaln("OK ...")
    
    miLog.Salidaln("SVM ...")
    m_DatosTwitter.SVM()
    miLog.Salidaln("OK ...")
 
    miLog.Salidaln("Descenso de Gradiente ...")
    m_DatosTwitter.DescensoGradiente()
    miLog.Salidaln("OK ...")
 
    miLog.Salidaln("Perceptron ...")
    m_DatosTwitter.Perceptron()
    miLog.Salidaln("OK ...")
    

    
    
    if (Errores > 0 ):
        miLog.Salidaln("ERRORES DETECTADOS")
    else:
        miLog.Salidaln("Proceso finalizado con exito...")

main()
