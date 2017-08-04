# -*- coding: utf-8 -*-
"""
Created on Fri May 19 12:08:55 2017

@author: lcprieto
"""
import tweepy
import ta_ConfigManager
import log
import ta_MongoDB


from tweepy import OAuthHandler


class Twitter(object):
    miLog       = log.Log
    miConf = ta_ConfigManager.Configuracion
    miAuth = ""
    miApi = ""
    m_ListaJSON = []
    m_InicializacionCamposSentinel = {'SentinelMicrosoft': "NA",'FrasesMicrosoft':" ",'SentinelGoogle': "NA",'FrasesGoogle':" ",'MagnitudeGoogle':" ",'SentinelBusiness': "NA",'FrasesBusiness':" "}
    m_MongoDB = ta_MongoDB.MongoDB

#------------------------------------------------------------------------------------------------------------------------------
            
    def __init__(self, db):      
        self.miLog = log.Log()
        self.m_MongoDB = db
        self.miLog.Salida("Cargando Gestor de Twitter...")          
        try:
            self.miConf = ta_ConfigManager.Configuracion()
            self.Conectar()
            self.miLog.Salidaln("OK") 
        except ValueError:
            self.miLog.Salidaln( "ERROR - Cargando Gestor de Twitter...")
            return -1
        
    def Conectar(self):
        try:         
            self.miLog.Salida("Conectando con Twitter...")
            self.miAuth = OAuthHandler(self.miConf.m_tweeter_consumer_key, self.miConf.m_tweeter_consumer_secret)
            self.miAuth.set_access_token(self.miConf.m_tweeter_access_key, self.miConf.m_tweeter_access_secret)
            self.miApi = tweepy.API(self.miAuth)
            self.miLog.Salidaln("OK")
        except :
            self.miLog.Salidaln( "ERROR - Conectado con Twitter...")
            return -1
        
    def BuscarNuevos (self):
        for datajson in tweepy.Cursor(self.miApi.search, q=self.miConf.m_tweeter_query, lang=self.miConf.m_tweeter_lang).items():   
            try:
                datajson._json.update(self.m_InicializacionCamposSentinel)
                
                if (self.m_MongoDB.timeline.find({"id_str":datajson.id_str}).count() > 0):
                    self.miLog.Salidaln("REPETIDO "+ datajson.id_str)
                else:
                    self.m_ListaJSON.append(datajson)
                    self.m_MongoDB.timeline.insert(datajson._json) 
                    
                    self.miLog.Salidaln("FECHA TWEET   " + str(datajson.created_at)) 
                    self.miLog.Salidaln("IDIOMA        " + datajson.lang)
                    self.miLog.Salidaln("LUGAR         " + datajson.user.location)
                    
                    self.miLog.Salidaln("MENSAJE       " + datajson.text)
                    self.miLog.Salidaln("HASHTAGS      ")
                      
                    i=0
                    for Hashtag in datajson.entities["hashtags"]:
                        i = i + 1
                        self.miLog.Salidaln("       HT " + str(i) + " : " + Hashtag["text"])
                          
                    self.miLog.Salidaln("MENCIONES     ")
                    i=0
                    for Menciones in datajson.entities["user_mentions"]:
                        i = i + 1
                        self.miLog.Salidaln("      USR " + str(i) + " : " + Menciones['screen_name'])
                    self.miLog.Salidaln("FUENTE        "+datajson.source)
                    self.miLog.Salidaln("AUTOR         ")
                    self.miLog.Salidaln("     USUARIO        " + datajson.user.screen_name)
                    self.miLog.Salidaln("     NOMBRE COMPLETO" + datajson.user.name)
                    self.miLog.Salidaln("     ZONA           " + datajson.user.time_zone)
                    try:
                        s_descripcion = datajson.user.description
                        self.miLog.Salidaln("     DESCIPCION     " + s_descripcion)
                    except Exception as e:
                        self.miLog.Salidaln("     DESCIPCION     " )
                        self.miLog.Salidaln(e.args)
                        pass
                    self.miLog.Salidaln("     TWEETS PUBLICOS" + str(datajson.user.statuses_count))
                    self.miLog.Salidaln("     SEGUIDORES     " + str(datajson.user.followers_count))
                    self.miLog.Salidaln("     AMIGOS         " + str(datajson.user.friends_count))
                    self.miLog.Salidaln("     SIGUE A        " + str(datajson.user.following))
                    self.miLog.Salidaln
                self.miLog.Salidaln ("---------------------------------------------------------------------")
            except Exception as e:
                self.miLog.Salidaln("          FIN STREAM TWITER")
                self.miLog.Salidaln(e.args)
                  