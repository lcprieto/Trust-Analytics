# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 12:16:34 2017

@author: Luis Carlos Prieto
luisc.prieto@gmail.com
"""


import sys
import pymongo
import json
import tweepy

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

#config = configparser.RawConfigParser()
#config.read('./sys/config.ini')
#consumer_key = config.get('TwitterAPIcredentials', 'consumer_key')
#consumer_secret = config.get('TwitterAPIcredentials', 'consumer_secret')
#access_key = config.get('TwitterAPIcredentials', 'access_key')
#access_secret = config.get('TwitterAPIcredentials', 'access_secret')
            
#SearchItems = config.get('TwitterSearchItems','SearchItems')

consumer_key = "1ek2VjUA81dn2a3Bl8wDolrs3"
consumer_secret = "J3YEWhzQw2p3JYXfYfrPHAHD9S0swyLh5dRa06TG8pofPqDj2w"
access_key = "847446734309474307-Sf1juR0NeCyNw10vbuM4a0ayTq45d7T"
access_secret = "YTZedW1oBZ777bD8zL2VghTVbSkmuBrClLmpw71ejSq5a"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth)
def Mostrar(Cabecera,Text):
    try:
        print(Cabecera + " : " + Text)  
    except Exception as e:
        print(Cabecera + " : -")
        pass
uri = "mongodb://ta-mrw-db:CncI8PbsXMJUaCUpkqNWmVygKS55ZsV3YJIjCszEwdwAE4D7UumFtobAOHeYM4rbqFEqrQc1e9ZI1Piz9D6sEA==@ta-mrw-db.documents.azure.com:10250/?ssl=true&ssl_cert_reqs=CERT_NONE"
client = pymongo.MongoClient(uri)

db = client.get_database("ta-mrw")
       
InicializacionCamposSentinel = {'SentinelMicrosoft': "NA",'FrasesMicrosoft':" ",'SentinelGoogle': "NA",'FrasesGoogle':" ",'MagnitudeGoogle':" ",'SentinelBusiness': "NA",'FrasesBusiness':" "}

for datajson in tweepy.Cursor(api.search, q="mrw", lang="es").items():   
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