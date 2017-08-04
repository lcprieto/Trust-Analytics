# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 12:16:34 2017

@author: lcpri
"""


import sys
import pymongo
import json
import tweepy

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener


consumer_key = "<YOUR KEY>"
consumer_secret = "<YOUR KEY>"
access_key = "<YOUR KEY>"
access_secret = "<YOUR KEY>"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth)
def Mostrar(Cabecera,Text):
    try:
        print(Cabecera + " : " + Text)  
    except Exception as e:
        print(Cabecera + " : -")
        pass
uri = "<MONGO DB AZURE URI ADDRESS>"
client = pymongo.MongoClient(uri)

db = client.get_database("<DATABASE NAME>")
       
InicializacionCamposSentinel = {'SentinelMicrosoft': "NA",'FrasesMicrosoft':" ",'SentinelGoogle': "NA",'FrasesGoogle':" ",'MagnitudeGoogle':" ",'SentinelBusiness': "NA",'FrasesBusiness':" "}

for datajson in tweepy.Cursor(api.search, q="<YOUR FILTER>", lang="<LANGUAJE es,en,...>").items():   
    try:
        

        datajson._json.update(InicializacionCamposSentinel)
        
        if (db.timeline.find({"id_str":datajson.id_str}).count() > 0):
            Mostrar("REPETIDO",datajson.id_str)
        else:
            db.timeline.insert(datajson._json) 
            Mostrar("FECHA TWEET   ",datajson.created_at) 
            Mostrar("IDIOMA        " , datajson.lang)
            Mostrar("LUGAR         " , datajson.user.location)
            
            Mostrar("MENSAJE       " , datajson.text)
            Mostrar("HASHTAGS      ","")
              
            i=0
            for Hashtag in datajson.entities["hashtags"]:
                i = i + 1
                Mostrar("       HT " + str(i) + " : ",Hashtag["text"])
                  
            Mostrar("MENCIONES     ","")
            i=0
            for Menciones in datajson.entities["user_mentions"]:
                i = i + 1
                Mostrar("      USR " + str(i) + " : ",Menciones['screen_name'])
            Mostrar("FUENTE        ",datajson.source)
            Mostrar("AUTOR         ","")
            Mostrar("     USUARIO        " , datajson.user.screen_name)
            Mostrar("     NOMBRE COMPLETO" , datajson.user.name)
            Mostrar("     ZONA           " , datajson.user.time_zone)
            try:
                s_descripcion = datajson.user.description
                Mostrar("     DESCIPCION     " , s_descripcion)
            except Exception as e:
                Mostrar("     DESCIPCION     " , "")
                pass
            Mostrar("     TWEETS PUBLICOS" , str(datajson.user.statuses_count))
            Mostrar("     SEGUIDORES     " , str(datajson.user.followers_count))
            Mostrar("     AMIGOS         " , str(datajson.user.friends_count))
            Mostrar("     SIGUE A        " , str(datajson.user.following))
            print ("\n")
        print ("---------------------------------------------------------------------")
    except Exception as e:
        Mostrar("          " , e.message())
        pass  