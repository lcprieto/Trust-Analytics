#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 12:40:03 2017

@author: lcprieto
"""

import log
import json
from bson import json_util
import ta_ConfigManager
from ta_emoticons import EmoticonDetector
import os

import pandas as pd
import re as regex
import nltk
import random

from sklearn import svm
from sklearn import linear_model

from sklearn.neural_network import MLPClassifier

from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import BernoulliNB

from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score

from sklearn.model_selection import train_test_split


import _pickle as cPickle
from collections import Counter

from time import time


class Tweetero(object):
     m_idUsuario    = ""
     m_Nombre       = ""
     m_Followers    = 0
     m_Follow       = 0
     m_Location     = ""
     m_NumTweets    = 0
     def __init__(self, idUsuario, Nombre, Followers, Follow, Location, NumTweets):
         self.m_idUsuario   = idUsuario
         self.m_Nombre      = str(Nombre).replace("'","-").encode('utf-8').decode('unicode_escape')
         self.m_Followers   = Followers
         self.m_Follow      = Follow
         self.m_Location    = str(Location).replace("'","-").encode('utf-8').decode('unicode_escape')
         self.m_NumTweets   = NumTweets
         
class TimeLine(object):
    m_idTweet = ""
    m_idUsuario = ""
    m_idUsuarioOriginal = ""
    m_Texto = ""
    m_Frases = ""
    m_reTweet = 0
    m_OrigenRetweet = ""
    m_SentinelMS = 0.0
    m_SentinelGoogle = 0.0
    m_SentinelIBM = 0.0
    m_SentinelBusiness = 0.0
    m_AccuracyMS = 0.0
    m_AccuracyGoogle = 0.0
    m_AccuracyIBM = 0.0
    m_AccuracyBusiness = 0.0
    m_Fecha = ""
    m_FechaOriginal = ""
    m_Hashtags = ""
    m_UsuariosMencionados = ""
    
    def __init__(self, idTweet, idUsuario, idUsuarioOriginal, Texto, reTweet, OrigenRetweet, Fecha, FechaOriginal, Hastags, UsuariosMencionados):
        miLog           = log.Log()
        try:
             self.m_idTweet                 = idTweet
             self.m_idUsuario               = idUsuario
             self.m_idUsuarioOriginal       = idUsuarioOriginal
             self.m_Texto                   = Texto
             self.m_reTweet                 = reTweet
             self.m_OrigenRetweet           = OrigenRetweet
             self.m_Fecha                   = Fecha
             self.m_FechaOriginal           = FechaOriginal
             self.m_Hastags                 = Hastags
             self.m_UsuariosMencionados     = UsuariosMencionados          
        except Exception as e:
            miLog.Salidaln ("ERROR Creando Twitero..." + e)
            return -1

#------------------------------------------------------------------------------------------------------------------------------

       
class JSONObject:
     def __init__(self, d):
             self.__dict__ = d

#------------------------------------------------------------------------------------------------------------------------------
         
class DataCleaner(object):
    miLog           = log.Log
    m_ListaTwiteros = []
    m_ListaTimeline = []
    m_ListaJSON     = []

#------------------------------------------------------------------------------------------------------------------------------    

    def __init__(self, JSONs):
        self.miLog = log.Log()
        self.miLog.Salida("Generando DataCleaner...")
        try:  
            self.m_ListaJSON = JSONs
            self.miLog.Salidaln("OK") 
        except ValueError:
            self.miLog.Salidaln( "ERROR - Generando DataCleaner")
            return -1

#------------------------------------------------------------------------------------------------------------------------------            
        
    def BuscarTwitero (self, Usuario):
        pos = -1
        for index in range(len(self.m_ListaTwiteros)):   
            if (self.m_ListaTwiteros[index].m_idUsuario == str(Usuario)):
                return index
                break           
        return pos

#------------------------------------------------------------------------------------------------------------------------------

    def ValidaTwitero (self, TLeido):

        return self.BuscarTwitero(TLeido.m_idUsuario)
    
#------------------------------------------------------------------------------------------------------------------------------
 
    def AnalisisTweets (self):
        try:       
            self.miLog.Salidaln ("Limpiando Twiteros de los Tweets...")
            numTweets = 0
            numTwiteros = 0
            for Dato in self.m_ListaJSON:
                try:                  
                    TweetString = json.dumps(Dato, sort_keys=True, indent=4, default=json_util.default)
                    Tweet = json.loads(TweetString)
                    numTweets += 1                  
        
                                                
                    #TWEETS
                    
                    idTweet                 = Tweet['id_str']
                    idUsuario               = Tweet['user']['id_str']
                    nickUsuario             = Tweet['user']['screen_name'].replace("'","-")
                    Texto                   = Tweet['text'].replace("'","-")
                    Fecha                   = Tweet['created_at']
                    Retweet                 = Tweet['retweet_count']
                    
                    nickUsuarioOriginal     = nickUsuario
                    OrigenRetweet           = idTweet
                    FechaOriginal           = Fecha
                    try:
                        nickUsuarioOriginal = Tweet['retweeted_status']['user']['screen_name'].replace("'","-")
                        OrigenRetweet       = Tweet['retweeted_status']['id_str']
                        FechaOriginal       = Tweet['retweeted_status']['created_at']
                        
                    except:
                        
                        self.miLog.Salida("")
                        
                    
                        
                    NumTweets               = Tweet['user']['statuses_count']
                    Hashtags                = ""
                    Followers               = Tweet['user']['followers_count']
                    Sigue                   = Tweet['user']['friends_count']
                    Ubicacion               = Tweet['user']['location'].replace("'","-") 
                    UsuariosMencionados     = ""
                    
                    
                    ElementoTL  = TimeLine(idTweet,nickUsuario,nickUsuarioOriginal, Texto, Retweet, OrigenRetweet, Fecha, FechaOriginal,Hashtags, UsuariosMencionados)
                    self.m_ListaTimeline.append(ElementoTL)  
                    
                    ElementoT = Tweetero(idUsuario,nickUsuario,Followers, Sigue, Ubicacion, NumTweets)
                    Encontrado = self.ValidaTwitero(ElementoT)  
                    
                    #TWITEROS
                    if (Encontrado < 0):
                        self.miLog.Salida(".")
                        self.m_ListaTwiteros.append(ElementoT)
                        numTwiteros += 1
                    else:
                        try:
                            self.miLog.Salida("D")
                            self.m_ListaTwiteros[Encontrado].m_Followers    = Followers
                            self.m_ListaTwiteros[Encontrado].m_Follow       = Sigue
                            self.m_ListaTwiteros[Encontrado].m_idUsuario    = idUsuario
                            self.m_ListaTwiteros[Encontrado].m_Location     = Ubicacion
                            self.m_ListaTwiteros[Encontrado].m_Nombre       = nickUsuario
                            self.m_ListaTwiteros[Encontrado].m_NumTweets    = NumTweets
                        except Exception as e:
                            self.miLog.Salida("X")
                    
                except Exception as e:
                    self.miLog.Salidaln ("ERROR Analizando twitero desdes los tweets #" + str(numTweets) + "   ...   " )
                    self.miLog.Salidaln(e.args)
                    pass
            del self.m_ListaJSON
            self.miLog.Salidaln(" OK")
            self.miLog.Salida("Identificados " + str(numTwiteros) + " Twiteros en ..." + str(numTweets) + " tweets ... ")
            self.miLog.Salidaln("OK") 
        except Exception as e :
            self.miLog.Salidaln( "ERROR - Limpiando Tweets en DataCleaner")
            self.miLog.Salidaln(e.args)
            return -1

    def AnalisisTweetsRetweet (self):
        try:       
            self.miLog.Salidaln ("Limpiando Tweets...")
            
            
            for Dato in self.m_ListaJSON:
                try:                  
                    TweetString = json.dumps(Dato, sort_keys=True, indent=4, default=json_util.default)
                    Tweet = json.loads(TweetString)
                    
        
                                                
                    #TWEETS
                    
                    idTweet                 = Tweet['id_str']
                    Retweet                 = Tweet['retweet_count']
                    nickUsuario             = Tweet['user']['screen_name'].replace("'","-")
                    Texto                   = Tweet['text'].replace("'","-")
                    Fecha                   = Tweet['created_at']
                    Retweet                 = 0
                    nickUsuarioOriginal     = nickUsuario
                    OrigenRetweet           = idTweet
                    FechaOriginal           = Fecha
                    try:
                        Retweet             = 1
                        nickUsuarioOriginal = Tweet['retweeted_status']['user']['screen_name'].replace("'","-")
                        OrigenRetweet       = Tweet['retweeted_status']['id_str']
                        FechaOriginal       = Tweet['retweeted_status']['created_at']
                        self.miLog.Salida("R")
                    except:
                        
                        self.miLog.Salida(".")
                        
                        
                    
                    Hashtags                = ""
                    
                    UsuariosMencionados     = ""
                    
                    ElementoTL  = TimeLine(idTweet,nickUsuario,nickUsuarioOriginal, Texto, Retweet, OrigenRetweet, Fecha, FechaOriginal,Hashtags, UsuariosMencionados)
                    self.m_ListaTimeline.append(ElementoTL)  
                    
                    
                except Exception as e:
                    self.miLog.Salidaln(e.args)
                    pass
            del self.m_ListaJSON
            self.miLog.Salidaln(" OK")
            
        except Exception as e :
            self.miLog.Salidaln( "ERROR - Limpiando Tweets en DataCleaner")
            self.miLog.Salidaln(e.args)
            return -1


        
    def CargaTimeline (self):
        try:       
            self.miLog.Salidaln ("Cargando los Tweets...")
            numTweets = 0
 
            for Dato in self.m_ListaJSON:
                try:                  
                    TweetString = json.dumps(Dato, sort_keys=True, indent=4, default=json_util.default)
                    Tweet = json.loads(TweetString)
                    numTweets += 1                  
    
                    #TWEETS
                    
                    idTweet                 = Tweet['id_str']
                    Retweet                 = Tweet['retweet_count']
                    nickUsuario             = Tweet['user']['screen_name'].replace("'","-")
                    Texto                   = Tweet['text'].replace("'","-")
                    Fecha                   = Tweet['created_at']
                    Retweet                 = 0
                    nickUsuarioOriginal     = nickUsuario
                    OrigenRetweet           = idTweet
                    FechaOriginal           = Fecha
                    try:
                        Retweet             = 1
                        nickUsuarioOriginal = Tweet['retweeted_status']['user']['screen_name'].replace("'","-")
                        OrigenRetweet       = Tweet['retweeted_status']['id_str']
                        FechaOriginal       = Tweet['retweeted_status']['created_at']
                        self.miLog.Salida("R")
                    except:
                        
                        self.miLog.Salida(".")
                        
                        
                    
                    Hashtags                = ""
                    
                    UsuariosMencionados     = ""
                    
                    ElementoTL = TimeLine(idTweet,nickUsuario,nickUsuarioOriginal, Texto, Retweet, OrigenRetweet, Fecha, FechaOriginal,Hashtags, UsuariosMencionados)
                    self.m_ListaTimeline.append(ElementoTL)  
                    self.miLog.Salida (".")
                    
                except Exception as e:
                    self.miLog.Salidaln ("ERROR Analizando twitero desdes los tweets #" + str(numTweets) + "   ...   " )
                    self.miLog.Salidaln(e.args)
                    pass
            del self.m_ListaJSON
            self.miLog.Salidaln(" OK")
            self.miLog.Salida("Identificados " + str(numTweets) + " tweets ... ")
            self.miLog.Salidaln("OK") 
        except Exception as e :
            self.miLog.Salidaln( "ERROR - Limpiando Tweets en DataCleaner")
            self.miLog.Salidaln(e.args)
            return -1   
        
    def AnalisisTweetsParcial (self):
            try:       
                self.miLog.Salidaln ("Limpiando Parcial de Twiteros de los Tweets...")
                self.AnalisisTweets()
                self.miLog.Salidaln("OK") 
            except Exception as e :
                self.miLog.Salidaln( "ERROR - Limpiando Parcial Tweets en DataCleaner" )
                self.miLog.Salidaln(e.args)
                return -1        
 

#-------------------------------------------------------------------------------------------------------



class DatosTwitter:
    Datos = pd.DataFrame
    Datos_Procesados = pd.DataFrame
    Palabras = pd.DataFrame
    miLog = log.Log()
    
    
    seed = 666
    random.seed(seed)
    
    miConf = ta_ConfigManager.Configuracion()
    
    ListaBlanca = None
    Datos_Modelo = None
    Etiquetas = None
    Testing = False
    
    def CargarDatos(self, Conexion):
        try:
            self.miLog.Salida("Cargando datos a predecir...")
            Consulta = u"SELECT  idTweet AS idtweet, Texto as texto, 'error' as sentinel FROM timeline WHERE esBusiness = 1 AND SentinelBusiness IS NULL"
            self.Datos = pd.read_sql_query(Consulta,Conexion)
            self.Datos_Procesados = self.Datos    
            self.miLog.Salidaln("OK...")
            
        except Exception as e:
            self.miLog.Salidaln("ERROR ..." + e.args())
        
        
    
    def Iniciar (self, csv_file, EsTesting=False, Cacheado=None):
        self.miLog.Salidaln("Inicializando DatosTwitter")
        if Cacheado is not None:
            self.Datos_Modelo = pd.read_csv(Cacheado,sep='|')
            return
        
        self.miLog.Salida("** 1 **")
        
        self.Testing = EsTesting
        
        self.miLog.Salida("\b\b\b\b\b\b\b")

        self.miLog.Salida("** 2 **")
        if not EsTesting:
            self.miLog.Salida("\b\b\b\b\b\b\b")
            self.miLog.Salida("** 3 **")
            self.Datos = pd.read_csv(csv_file, sep='|',header=0, names=["idtweet", "texto", "sentinel"])
            
            self.Datos = self.Datos[self.Datos["sentinel"].isin(["positivo", "negativo", "neutro"])]
            
            
            
        else:
            self.miLog.Salida("\b\b\b\b\b\b\b")
            self.miLog.Salida("** 4 **")
            self.Datos = pd.read_csv(csv_file, sep='|',header=0, names=["idtweet", "texto"],dtype={"idtweet":"str","texto":"str"},nrows=4000)
            
            not_null_text = 1 ^ pd.isnull(self.Datos["texto"])
            not_null_id = 1 ^ pd.isnull(self.Datos["idtweet"])
            self.Datos = self.Datos.loc[not_null_id & not_null_text, :]
        
        self.miLog.Salida("\b\b\b\b\b\b\b")
        
       
        
        self.Datos_Procesados = self.Datos
        self.Palabras = []
        self.Datos_Modelo = None
        self.Etiquetas = None
        self.miLog.Salidaln("OK...")   
        
    
    def Eliminar_URL (self):
        try:
            Expresion = "http.?://[^\s]+[\s]?" # regex.compile(r'http.?://[^\s]+[\s]?')
            self.Datos_Procesados['texto'].replace(to_replace = Expresion,  value = "", regex=True, inplace=True)
        except Exception as a:
            self.miLog.Salida("!")
        
        
    def Eliminar_na (self):
        try:
            self.Datos_Procesados[self.Datos_Procesados["texto"] != "Not Available"]
        except Exception as a:
            self.miLog.Salida("!")
        
    
    def Eliminar_Especiales (self):
        
        for remove in map(lambda r: regex.compile(regex.escape(r)), [",", ":", "\"", "=", "&", ";", "%", "$",
                                                                     "@", "%", "^", "*", "(", ")", "{", "}",
                                                                     "[", "]", "|", "/", "\\", ">", "<", "-",
                                                                     "!", "?", ".", "'",
                                                                     "--", "---", "#"]):
            try:
                self.Datos_Procesados.loc[:, "texto"].replace(remove, "", inplace=True)
            except Exception as a:
                self.miLog.Salida("!")
        
    def Eliminar_Usernames (self):
        try:
            Expresion = "@[^\s]+[\s]?"
            self.Datos_Procesados['texto'].replace(to_replace = Expresion,  value = "", regex=True, inplace=True)
        except Exception as a:
            self.miLog.Salida("!")
        
    def Eliminar_Numeros (self):
        try:
            Expresion = "\s?[0-9]+\.?[0-9]*" 
            self.Datos_Procesados['texto'].replace(to_replace = Expresion,  value = "", regex=True, inplace=True)
        except Exception as a:
            self.miLog.Salida("!")

        
    
    def Limpieza (self):
        self.miLog.Salida("Limpiando...") 
        self.miLog.Salida("H") 
        self.Eliminar_URL()
        self.miLog.Salida("U") 
        self.Eliminar_Usernames()
        self.miLog.Salida("E") 
        self.Eliminar_Especiales()
        self.miLog.Salida("V") 
        self.Eliminar_na()
        self.miLog.Salida("N") 
        self.Eliminar_Numeros()
        self.miLog.Salidaln("\b\b\b\b\bOK...") 
        
        
        
    def Separar(self, stemmer=nltk.PorterStemmer()):
        def stem_and_join(row):
            row["texto"] = list(map(lambda str: stemmer.stem(str.lower()), row["texto"]))
            return row

        self.Datos_Procesados = self.Datos_Procesados.apply(stem_and_join, axis=1)
        
    def Tokenizar(self, tokenizer=nltk.word_tokenize):
        def tokenize_row(row):
            row["texto_original"] = row["texto"]
            row["texto"] = tokenizer(row["texto"])
            row["texto_token"] = [] + row["texto"]
            return row

        self.Datos_Procesados = self.Datos_Procesados.apply(tokenize_row, axis=1)        
        
    def ContarPalabras (self):
        
        
        mPalabras = Counter(self.Palabras)
        
        for idx in self.Datos_Procesados.index:
            #print (self.Datos_Procesados.loc[idx, "texto"])
            ListaPalabras = []
            
            for Palabra in self.Datos_Procesados.loc[idx, "texto"]:
                if Palabra in self.Palabras:
                    ListaPalabras.append(Palabra)
                    
                
            #mPalabras.update(self.Datos_Procesados.loc[idx, "texto"])
            mPalabras.update(ListaPalabras)
        self.Palabras = mPalabras    
        self.miLog.Salida("Top 5 de palabras más usadas: ")
        self.miLog.Salidaln(self.Palabras.most_common(5))

        
    def RecuperarNegaciones (self):
        stopwords=nltk.corpus.stopwords.words("spanish")
        self.ListaBlanca = ["no", "ni"]
        
        for idx, stop_word in enumerate(stopwords):
            if stop_word not in self.ListaBlanca:
                del self.Palabras[stop_word]
        self.miLog.Salida("Top 5 de palabras más usadas (Recuperando negaciones: ")
        self.miLog.Salidaln(self.Palabras.most_common(5))
        
        
    def ConstruirPalabras(self, min_occurrences=1, max_occurences=1000, stopwords=nltk.corpus.stopwords.words("spanish")):
        self.Palabras = []
        whitelist = self.ListaBlanca
        
        if os.path.isfile(self.miConf.m_Palabras):
            self.miLog.Salidaln("Leyendo Palabras...")
            word_df = pd.read_csv(self.miConf.m_Palabras)
            word_df = word_df[word_df["ocurrencias"] > min_occurrences]
            self.Palabras = list(word_df.loc[:, "palabra"])
            return
        
        words = Counter()
        for idx in self.Datos_Procesados.index:
            words.update(self.Datos_Procesados.loc[idx, "texto"])

        for idx, stop_word in enumerate(stopwords):
            try:
                
                if stop_word not in whitelist:
                    del words[stop_word]
            except:
                continue

        word_df = pd.DataFrame(data={"palabra": [k for k, v in words.most_common() if min_occurrences < v < max_occurences],
                                     "ocurrencias": [v for k, v in words.most_common() if min_occurrences < v < max_occurences]},
                               columns=["palabra", "ocurrencias"])
        
        word_df.to_csv(self.miConf.m_Palabras, index_label="idx")
        
        self.Palabras = [k for k, v in words.most_common() if min_occurrences < v < max_occurences]
        
        
    def ConstruirMatrizEntrenamiento (self):
        try:
            print(self.Palabras)
        except Exception as e:
            self.miLog.Salidaln(e.args)

    def build_data_model(self):
        extra_columns = [col for col in self.Datos_Procesados.columns if col.startswith("number_of")]
        label_column = []
        if not self.Testing:
            label_column = ["label"]

        columns = label_column + extra_columns + list(
            map(lambda w: w + "_bow",self.Palabras))
        
        labels = []
        rows = []
        for idx in self.Datos_Procesados.index:
            current_row = []

            if not self.Testing:
                # add label
                current_label = self.Datos_Procesados.loc[idx, "sentinel"]
                labels.append(current_label)
                current_row.append(current_label)

            for _, col in enumerate(extra_columns):
                current_row.append(self.Datos_Procesados.loc[idx, col])

            # add bag-of-words
            tokens = set(self.Datos_Procesados.loc[idx, "texto"])
            for _, word in enumerate(self.Palabras):
                current_row.append(1 if word in tokens else 0)

            rows.append(current_row)

        self.Datos_Modelo = pd.DataFrame(rows, columns=columns)
        self.Etiquetas = pd.Series(labels)
        return self.Datos_Modelo, self.Etiquetas
    
    def build_features(self):
        def count_by_lambda(expression, word_array):
            return len(list(filter(expression, word_array)))

        def count_occurences(character, word_array):
            counter = 0
            for j, word in enumerate(word_array):
                for char in word:
                    if char == character:
                        counter += 1

            return counter

        def count_by_regex(regex, plain_text):
            return len(regex.findall(plain_text))

        self.add_column("splitted_text", map(lambda txt: txt.split(" "), self.Datos_Procesados["texto"]))

        # number of uppercase words
        uppercase = list(map(lambda txt: count_by_lambda(lambda word: word == word.upper(), txt),
                             self.Datos_Procesados["splitted_text"]))
        self.add_column("number_of_uppercase", uppercase)

        # number of !
        exclamations = list(map(lambda txt: count_occurences("!", txt),
                                self.Datos_Procesados["splitted_text"]))

        self.add_column("number_of_exclamation", exclamations)

        # number of ?
        questions = list(map(lambda txt: count_occurences("?", txt),
                             self.Datos_Procesados["splitted_text"]))

        self.add_column("number_of_question", questions)

        # number of ...
        ellipsis = list(map(lambda txt: count_by_regex(regex.compile(r"\.\s?\.\s?\."), txt),
                            self.Datos_Procesados["texto"]))

        self.add_column("number_of_ellipsis", ellipsis)

        # number of hashtags
        hashtags = list(map(lambda txt: count_occurences("#", txt),
                            self.Datos_Procesados["splitted_text"]))

        self.add_column("number_of_hashtags", hashtags)

        # number of mentions
        mentions = list(map(lambda txt: count_occurences("@", txt),
                            self.Datos_Procesados["splitted_text"]))

        self.add_column("number_of_mentions", mentions)

        # number of quotes
        quotes = list(map(lambda plain_text: int(count_occurences("'", [plain_text.strip("'").strip('"')]) / 2 +
                                                 count_occurences('"', [plain_text.strip("'").strip('"')]) / 2),
                          self.Datos_Procesados["texto"]))

        self.add_column("number_of_quotes", quotes)

        # number of urls
        urls = list(map(lambda txt: count_by_regex(regex.compile(r"http.?://[^\s]+[\s]?"), txt),
                        self.Datos_Procesados["texto"]))

        self.add_column("number_of_urls", urls)

        # number of positive emoticons
        ed = EmoticonDetector()
        positive_emo = list(
            map(lambda txt: count_by_lambda(lambda word: ed.is_emoticon(word) and ed.is_positive(word), txt),
                self.Datos_Procesados["splitted_text"]))

        self.add_column("number_of_positive_emo", positive_emo)

        # number of negative emoticons
        negative_emo = list(map(
            lambda txt: count_by_lambda(lambda word: ed.is_emoticon(word) and not ed.is_positive(word), txt),
            self.Datos_Procesados["splitted_text"]))

        self.add_column("number_of_negative_emo", negative_emo)
        
    def add_column(self, column_name, column_content):
        self.Datos_Procesados.loc[:, column_name] = pd.Series(column_content, index=self.Datos_Procesados.index)
    
    
   
    
    def Clasificador(self,X_train, y_train, X_test, y_test, classifier):
        self.miLog.Salidaln("")
        self.miLog.Salidaln("===============================================")
        classifier_name = str(type(classifier).__name__)
        self.miLog.Salidaln("Testing " + classifier_name)
        now = time()
        list_of_labels = sorted(list(set(y_train)))
        model = classifier.fit(X_train, y_train)
        self.miLog.Salidaln("Learing time {0}s".format(time() - now))
        now = time()
        predictions = model.predict(X_test)
        self.miLog.Salidaln("Predicting time {0}s".format(time() - now))
    
        precision = precision_score(y_test, predictions, average=None, pos_label=None, labels=list_of_labels)
        recall = recall_score(y_test, predictions, average=None, pos_label=None, labels=list_of_labels)
        accuracy = accuracy_score(y_test, predictions)
        f1 = f1_score(y_test, predictions, average=None, pos_label=None, labels=list_of_labels)
        self.miLog.Salidaln("=================== Results ===================")
        self.miLog.Salidaln("            Negative     Neutral     Positive")
        self.miLog.Salidaln("F1       " + str(f1))
        self.miLog.Salidaln("Precision" + str(precision))
        self.miLog.Salidaln("Recall   " + str(recall))
        self.miLog.Salidaln("Accuracy " + str(accuracy))
        self.miLog.Salidaln("===============================================")
    
        return precision, recall, accuracy, f1
    

    def RandomForest (self):
        
        X_train, X_test, y_train, y_test = train_test_split(self.Datos_Modelo.iloc[:, 1:], self.Datos_Modelo.iloc[:, 0],
                                                            train_size=0.7, stratify=self.Datos_Modelo.iloc[:, 0],
                                                            random_state=self.seed)
        ModeloClasificador = RandomForestClassifier(random_state=self.seed,n_estimators=500,n_jobs=-1, max_features=120)
       
            
        Modelo = ModeloClasificador.fit(X_train,y_train)
        
        precision, recall, accuracy, f1 = self.Clasificador(X_train, y_train, X_test, y_test, Modelo)

        
        with open(self.miConf.m_UbicacionModelos +'RandomForest.pkl', 'wb') as fid:
            cPickle.dump(Modelo, fid)
        
        
        
        
    def NaiveBayes(self):
        X_train, X_test, y_train, y_test = train_test_split(self.Datos_Modelo.iloc[:, 1:], self.Datos_Modelo.iloc[:, 0],
                                                            train_size=0.7, stratify=self.Datos_Modelo.iloc[:, 0],
                                                            random_state=self.seed)
        
        ModeloClasificador = BernoulliNB()
        
        Modelo = ModeloClasificador.fit(X_train,y_train)
                
        #Prediccion = Modelo.predict(X_test)
        #print (Prediccion)
        
        precision, recall, accuracy, f1 = self.Clasificador(X_train, y_train, X_test, y_test, Modelo)
        with open(self.miConf.m_UbicacionModelos +'NaiveBayes.pkl', 'wb') as fid:
            cPickle.dump(Modelo, fid)
        
    def SVM (self):
        X_train, X_test, y_train, y_test = train_test_split(self.Datos_Modelo.iloc[:, 1:], self.Datos_Modelo.iloc[:, 0],
                                                            train_size=0.7, stratify=self.Datos_Modelo.iloc[:, 0],
                                                            random_state=self.seed)
        
        ModeloClasificador = svm.SVC(probability=False, kernel="rbf", C=2.8, gamma=.0073)
        
        Modelo = ModeloClasificador.fit(X_train,y_train)
                
        #Prediccion = Modelo.predict(X_test)
        #print (Prediccion)
        
        precision, recall, accuracy, f1 = self.Clasificador(X_train, y_train, X_test, y_test, Modelo)
        with open(self.miConf.m_UbicacionModelos +'SVM.pkl', 'wb') as fid:
            cPickle.dump(Modelo, fid)
        
        
    def DescensoGradiente (self):
        X_train, X_test, y_train, y_test = train_test_split(self.Datos_Modelo.iloc[:, 1:], self.Datos_Modelo.iloc[:, 0],
                                                            train_size=0.7, stratify=self.Datos_Modelo.iloc[:, 0],
                                                            random_state=self.seed)
        
        ModeloClasificador = linear_model.SGDClassifier()
        
        Modelo = ModeloClasificador.fit(X_train,y_train)
                
        #Prediccion = Modelo.predict(X_test)
        #print (Prediccion)
        
        precision, recall, accuracy, f1 = self.Clasificador(X_train, y_train, X_test, y_test, Modelo)
        with open(self.miConf.m_UbicacionModelos +'SGD.pkl', 'wb') as fid:
            cPickle.dump(Modelo, fid)
    
    
    def Perceptron (self):
        X_train, X_test, y_train, y_test = train_test_split(self.Datos_Modelo.iloc[:, 1:], self.Datos_Modelo.iloc[:, 0],
                                                            train_size=0.7, stratify=self.Datos_Modelo.iloc[:, 0],
                                                            random_state=self.seed)
        
        ModeloClasificador = MLPClassifier(alpha=1e-5,hidden_layer_sizes=(1000, 500,50,5), random_state=1, max_iter=10000, warm_start=True)
        
        Modelo = ModeloClasificador.fit(X_train,y_train)
                
        #Prediccion = Modelo.predict(X_test)
        #print (Prediccion)
        
        precision, recall, accuracy, f1 = self.Clasificador(X_train, y_train, X_test, y_test, Modelo)
        with open(self.miConf.m_UbicacionModelos +'Perceptron.pkl', 'wb') as fid:
            cPickle.dump(Modelo, fid)
        
            
        
    def BusinessRandomForest(self):
        self.miLog.Salidaln("Revisión Business RandomForest...")
        with open(self.miConf.m_UbicacionModelos +'RandomForest.pkl', 'rb') as fid:
            ModeloClasificador = cPickle.load(fid)    
        Prediccion = ModeloClasificador.predict(self.Datos_Modelo.ix[:,1:])
        return Prediccion
            
        
    
    def BusinessNaiveBayes(self):   
         self.miLog.Salidaln("Revisión Business NaiveBayes...")
         with open(self.miConf.m_UbicacionModelos +'NaiveBayes.pkl', 'rb') as fid:
            ModeloClasificador = cPickle.load(fid)
         Prediccion = ModeloClasificador.predict(self.Datos_Modelo.iloc[:,1:])
         return Prediccion
     
        
    def BusinessSVM(self):
        self.miLog.Salidaln("Revisión Business SVM...")
        with open(self.miConf.m_UbicacionModelos +'SVM.pkl', 'rb') as fid:
            ModeloClasificador = cPickle.load(fid)    
        Prediccion = ModeloClasificador.predict(self.Datos_Modelo.ix[:,1:])
        return Prediccion
        
        
    def BusinesDescensoGradiente(self):
        self.miLog.Salidaln("Revisión Business Descenso Gradiente...")
        
        with open(self.miConf.m_UbicacionModelos +'SGD.pkl', 'rb') as fid:
            ModeloClasificador = cPickle.load(fid)    
        Prediccion = ModeloClasificador.predict(self.Datos_Modelo.ix[:,1:])
        return Prediccion
        
    def BusinesPerceptron(self):
        self.miLog.Salidaln("Revisión Business Perceptron...")
        
        with open(self.miConf.m_UbicacionModelos +'Perceptron.pkl', 'rb') as fid:
            ModeloClasificador = cPickle.load(fid)    
        Prediccion = ModeloClasificador.predict(self.Datos_Modelo.ix[:,1:])
        return Prediccion
        
        
        
#--------------------------------------------------------------------------------------------------------------
      
        
        
     
        
        
         

    
               
    
    
    