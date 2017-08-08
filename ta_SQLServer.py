#!/usr/bin/env python3

# coding: latin1
"""
Created on Thu May  4 12:13:44 2017

@author: Luis Carlos Prieto
luisc.prieto@gmail.com
"""


import log
import pymssql
import ta_DataCleaner
import ta_ConfigManager
import time


      

class SQLServer(object):
    #Clase con la que gestionaremos las consultas a SQL Server
    
    miLog       = log.Log
    m_conSQL    = pymssql.Connection
    
    m_ListaJSON = []
    miConf = ta_ConfigManager.Configuracion

#------------------------------------------------------------------------------------------------------------------------------
            
    def __init__(self):      
        self.miLog = log.Log()
        self.miLog.Salida("Cargando Gestor de SQL Server...")          
        try:
            self.miConf = ta_ConfigManager.Configuracion()
            self.Conectar()
            self.miLog.Salidaln("OK") 
        except ValueError:
            self.miLog.Salidaln( "ERROR - Cargano Gestor de SQLServer")
            return -1

#------------------------------------------------------------------------------------------------------------------------------
            
    def Conectar(self):
        # Conectamos con SQL Server Express en Local...
        self.miLog.Salida("Conectando con SQL Server en Azure......")
        try:      
            self.m_conSQL = pymssql.connect(server=self.miConf.m_serverSQL, user=self.miConf.m_userSQL, password=self.miConf.m_passwordSQL, database=self.miConf.m_databaseSQL) 
            
            self.miLog.Salidaln("SQL Server OK...")
    
        except Exception as e:
            self.miLog.Salidaln (" ERROR Conectando SQL Server en Azure ......"  )
            self.miLog.Salidaln(e.args)
            return -1


            
#------------------------------------------------------------------------------------------------------------------------------
                        
    def ListaTweetsGoogle(self, Lista):
        try:
            self.miLog.Salidaln("")
            self.miLog.Salidaln("Recuperando timeline en SQL Server...")  
            cursor = self.m_conSQL.cursor()
            cursor.execute(u"SELECT  idTweet,idUsuario, idUsuarioOriginal, Texto, ReTweet, OrigenRetweet, Fecha, FechaOriginal, Hashtags, usuariosMencionados FROM timeline WHERE esBusiness = 1 AND SentinelGoogle IS NULL")
            self.miLog.Salidaln("Analizando...") 
            for Fila in cursor:
                 idTweet                 = str(Fila[0])
                 nickUsuario             = str(Fila[1])
                 nickUsuarioOriginal     = str(Fila[2])
                 Texto                   = str(Fila[3])
                 Retweet                 = Fila[4]
                 OrigenRetweet           = Fila[5]
                 Fecha                   = Fila[6]
                 FechaOriginal           = Fila[7]
                 Hashtags                = str(Fila[8])
                 UsuariosMencionados     = str(Fila[9])
                    
                 self.miLog.Salida(".")     
                 ElementoTL  = ta_DataCleaner.TimeLine(idTweet,nickUsuario, nickUsuarioOriginal, Texto, Retweet, OrigenRetweet, Fecha, FechaOriginal, Hashtags, UsuariosMencionados)
                 Lista.append(ElementoTL)  
            self.miLog.Salidaln("OK")     
                
        except Exception as e:
            self.miLog.Salidaln (" ERROR Recuperando timeline de SQL Server en Azure"  )
            self.miLog.Salidaln(e.args)
            return -1
        
            
#------------------------------------------------------------------------------------------------------------------------------
            
    def ListaTweetsMicrosoft(self, Lista):
        try:
            self.miLog.Salidaln("")
            self.miLog.Salidaln("Recuperando timeline en SQL Server...")  
            cursor = self.m_conSQL.cursor()
            cursor.execute(u"SELECT idTweet,idUsuario, idUsuarioOriginal, Texto, ReTweet, OrigenRetweet, Fecha, FechaOriginal, Hashtags, usuariosMencionados FROM timeline WHERE esBusiness = 1 AND SentinelMs IS NULL")
            self.miLog.Salidaln("Analizando...") 
            for Fila in cursor:
                 idTweet                 = str(Fila[0])
                 nickUsuario             = str(Fila[1])
                 nickUsuarioOriginal     = str(Fila[2])
                 Texto                   = str(Fila[3])
                 Retweet                 = Fila[4]
                 OrigenRetweet           = Fila[5]
                 Fecha                   = Fila[6]
                 FechaOriginal           = Fila[7]
                 Hashtags                = str(Fila[8])
                 UsuariosMencionados     = str(Fila[9])
                    
                 self.miLog.Salida(".")     
                 ElementoTL  = ta_DataCleaner.TimeLine(idTweet,nickUsuario, nickUsuarioOriginal, Texto, Retweet, OrigenRetweet, Fecha, FechaOriginal, Hashtags, UsuariosMencionados)
                 Lista.append(ElementoTL)  
            self.miLog.Salidaln("OK")     
                
        except Exception as e:
            self.miLog.Salidaln (" ERROR Recuperando timeline de SQL Server en Azure"  )
            self.miLog.Salidaln(e.args)
            return -1            
        
#------------------------------------------------------------------------------------------------------------------------------
            
    def ListaTweetsBusiness(self, Lista):
        try:
            self.miLog.Salidaln("")
            self.miLog.Salidaln("Recuperando timeline ESBUSINESS en SQL Server...")  
            cursor = self.m_conSQL.cursor()
            cursor.execute(u"SELECT idTweet,idUsuario, idUsuarioOriginal, Texto, ReTweet, OrigenRetweet, Fecha, FechaOriginal, Hashtags, usuariosMencionados FROM timeline WHERE esBusiness IS NULL")
            self.miLog.Salidaln("Analizando...") 
            for Fila in cursor:
                 idTweet                 = str(Fila[0])
                 nickUsuario             = str(Fila[1])
                 nickUsuarioOriginal     = str(Fila[2])
                 Texto                   = str(Fila[3])
                 Retweet                 = Fila[4]
                 OrigenRetweet           = Fila[5]
                 Fecha                   = Fila[6]
                 FechaOriginal           = Fila[7]
                 Hashtags                = str(Fila[8])
                 UsuariosMencionados     = str(Fila[9])
                    
                 self.miLog.Salida(".")     
                 ElementoTL  = ta_DataCleaner.TimeLine(idTweet,nickUsuario, nickUsuarioOriginal, Texto, Retweet, OrigenRetweet, Fecha, FechaOriginal, Hashtags, UsuariosMencionados)
                 Lista.append(ElementoTL)  
            self.miLog.Salidaln("OK")     
                
        except Exception as e:
            self.miLog.Salidaln (" ERROR Recuperando timeline ESBUSINESS de SQL Server en Azure"  )
            self.miLog.Salidaln(e.args)
            return -1            

#------------------------------------------------------------------------------------------------------------------------------
        
    def ListaTweetsSentinelBusiness(self, Lista):
        try:
            self.miLog.Salidaln("")
            self.miLog.Salidaln("Recuperando timeline SENTINEL ESBUSINESS en SQL Server...")  
            cursor = self.m_conSQL.cursor()
            cursor.execute(u"SELECT idTweet,idUsuario, idUsuarioOriginal, Texto, ReTweet, OrigenRetweet, Fecha, FechaOriginal,  Hashtags, usuariosMencionados FROM timeline WHERE esBusiness = 1 AND SentinelBusiness IS NULL")
            self.miLog.Salidaln("Analizando...") 
            for Fila in cursor:
                 idTweet                 = str(Fila[0])
                 nickUsuario             = str(Fila[1])
                 nickUsuarioOriginal     = str(Fila[2])
                 Texto                   = str(Fila[3])
                 Retweet                 = Fila[4]
                 OrigenRetweet           = Fila[5]
                 Fecha                   = Fila[6]
                 FechaOriginal           = Fila[7]
                 Hashtags                = str(Fila[8])
                 UsuariosMencionados     = str(Fila[9])
                    
                 self.miLog.Salida(".")     
                 ElementoTL  = ta_DataCleaner.TimeLine(idTweet,nickUsuario, nickUsuarioOriginal, Texto, Retweet, OrigenRetweet, Fecha, FechaOriginal, Hashtags, UsuariosMencionados)
                 Lista.append(ElementoTL)  
            self.miLog.Salidaln("OK")     
                
        except Exception as e:
            self.miLog.Salidaln (" ERROR Recuperando timeline ESBUSINESS de SQL Server en Azure"  )
            self.miLog.Salidaln(e.args)
            return -1            

#------------------------------------------------------------------------------------------------------------------------------
            
    def RegenerarTwiteros(self, Lista):
        try:
            self.miLog.Salidaln("")
            self.miLog.Salidaln("Regenerando Twiteros en SQL Server...")  
            Usuario = ta_DataCleaner.Tweetero
            cursor = self.m_conSQL.cursor()
            self.miLog.Salida("Limpiando Tabla de Usuarios...")  
            strSQL = "TRUNCATE TABLE [dbo].[Usuarios]"
            cursor.execute(strSQL) 
            self.miLog.Salidaln("OK")  
            ConsultaSQL = b''
            
            for Usuario in Lista:
                try:
                    strSQL = u"INSERT INTO [dbo].[Usuarios] ([idUsuario], [Nombre], [Followers], [Follow], [Localizacion], [numTweets]) VALUES ("
                    strSQL = strSQL + "'" + Usuario.m_idUsuario + "',"
                    strSQL = strSQL + "'" + Usuario.m_Nombre + "',"
                    strSQL = strSQL + str(Usuario.m_Followers)  + ","
                    strSQL = strSQL + str(Usuario.m_Follow)   + ","
                    strSQL = strSQL + "'" + Usuario.m_Location  + "',"
                    strSQL = strSQL + str(Usuario.m_NumTweets)   + ")"
                    ConsultaSQL = strSQL.encode('iso-8859-1','ignore').decode('utf-8','ignore')
                    cursor.execute(ConsultaSQL)              
                    self.miLog.Salida(".")  
                    self.m_conSQL.commit()
                except pymssql.Error as e:
                    ConsultaSQL = strSQL.encode('unicode-escape')
                    cursor.execute(ConsultaSQL)   
                    self.m_conSQL.commit()
                    self.miLog.Salida("E") 
                    continue    

        except Exception as e:
            self.miLog.Salidaln("ERROR Volvando a SQL los tuiteros")
            self.miLog.Salidaln(e.args)
            return -1

#------------------------------------------------------------------------------------------------------------------------------
        
    def RegenerarTimeline(self, ListaTL):
        try:
            self.miLog.Salidaln("")
            self.miLog.Salidaln("Regenerando Timeline en SQL Server...")  
            Elemento = ta_DataCleaner.TimeLine
            cursor = self.m_conSQL.cursor()
            self.miLog.Salida("Limpiando Tabla de Timeline...")  
            strSQL = "TRUNCATE TABLE [dbo].[timeline]"
            cursor.execute(strSQL) 
            self.miLog.Salidaln("OK")  
            ConsultaSQL = b''
            for Elemento in ListaTL:
                try: # Si fallan las dos encodings
                    try:
                        ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(Elemento.m_Fecha,'%a %b %d %H:%M:%S +0000 %Y'))
                        tso = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(Elemento.m_FechaOriginal,'%a %b %d %H:%M:%S +0000 %Y'))
                        strSQL = u"INSERT INTO [dbo].[timeline] ([idTweet],[idUsuario], [idUsuarioOriginal], [Fecha], [FechaOriginal], [Texto], [Retweet], [OrigenRetweet]) VALUES ("
                        strSQL = strSQL + "'" + str(Elemento.m_idTweet) + "',"
                        strSQL = strSQL + "'" + str(Elemento.m_idUsuario) + "',"
                        strSQL = strSQL + "'" + str(Elemento.m_idUsuarioOriginal) + "',"
                        strSQL = strSQL + "'" + str(ts) + "',"
                        strSQL = strSQL + "'" + str(tso) + "',"
                        strSQL = strSQL + "'" + Elemento.m_Texto + "',"
                        strSQL = strSQL + Elemento.m_reTweet  + ","
                        strSQL = strSQL + "'" + Elemento.m_OrigenRetweet + "')"
                        ConsultaSQL = strSQL#.encode('latin-1').decode('utf-8')
                        cursor.execute(ConsultaSQL)              
                        self.miLog.Salida(".")  
                        self.m_conSQL.commit() 
                    except pymssql.Error as e:
                        ConsultaSQL = strSQL.encode('unicode-escape')
                        cursor.execute(ConsultaSQL)   
                        self.m_conSQL.commit()
                        self.miLog.Salida("E")                      
                        continue
                except: # Si fallan los dos encoding damos error X pero seguimos, así solo perdemos un tweet...
                    self.miLog.Salida("X")                      
                    continue

        except Exception as e: 
            self.miLog.Salidaln("ERROR Volcando a SQL los tweets ")
            self.miLog.Salidaln(strSQL)
            self.miLog.Salidaln(e.args)
            return -1

			
#------------------------------------------------------------------------------------------------------------------------------
            
    def ParcialTwiteros(self, Lista):
        try:
            self.miLog.Salidaln("")
            self.miLog.Salida("Regenerando Twiteros en SQL Server")  
            Elemento = ta_DataCleaner.Tweetero
            ConsultaSQL = b''
            self.miLog.Salidaln("...")  
           
            for Elemento in Lista:
                try:
                    try:
                        strSQL = u"INSERT INTO [dbo].[Usuarios] ([idUsuario],[Nombre], [Followers], [Follow], [Localizacion], [numTweets]) VALUES ("
                        strSQL = strSQL + "'" + str(Elemento.m_idUsuario) + "',"
                        strSQL = strSQL + "'" + Elemento.m_Nombre + "',"
                        strSQL = strSQL + str(Elemento.m_Followers)  + ","
                        strSQL = strSQL + str(Elemento.m_Follow)   + ","
                        strSQL = strSQL + "'" + Elemento.m_Location  + "',"
                        strSQL = strSQL + str(Elemento.m_NumTweets)   + ")"
                        ConsultaSQL = strSQL.encode('iso-8859-1','ignore').decode('utf-8','ignore')
                        self.m_conSQL.cursor().execute(ConsultaSQL)              
                        self.m_conSQL.commit()
                        self.miLog.Salida(".")
                    except: 
                        strSQL = u"UPDATE [dbo].[Usuarios] SET "
                        strSQL = strSQL + "[Nombre] = '" + Elemento.m_Nombre + "',"
                        strSQL = strSQL + "[Followers] = " + str(Elemento.m_Followers) + ","
                        strSQL = strSQL + "[Follow] = " + str(Elemento.m_Follow) + ","
                        strSQL = strSQL + "[Localizacion] = '" + Elemento.m_Location + "',"
                        strSQL = strSQL + "[numTweets] = " + str(Elemento.m_NumTweets) + " WHERE [idUsuario] = '" + str(Elemento.m_idUsuario) + "'"
                        ConsultaSQL = strSQL.encode('iso-8859-1','ignore').decode('utf-8','ignore')
                        self.m_conSQL.cursor().execute(ConsultaSQL)              
                        self.m_conSQL.commit()
                        self.miLog.Salida("U")
                except: # Si fallan los dos encoding damos error X pero seguimos, así solo perdemos un tweet...
                    self.miLog.Salida("X")                      
                    continue

        except Exception as e:
            self.miLog.Salidaln("ERROR Volcando PARCIALES a SQL los tuiteros")
            self.miLog.Salidaln(e.args)
            return -1

#------------------------------------------------------------------------------------------------------------------------------

    def VecesReteet (self, idTweet):
        
        try:
            ConsultaSQL = u"SELECT idTweet FROM timeline WHERE OrigenRetweet = '" + idTweet + "'"
            cursor = self.m_conSQL.cursor()
            cursor.execute(ConsultaSQL)      
            cursor.fetchall()
            Veces = cursor.rowcount
            
            Consulta = u"UPDATE [dbo].[timeline] SET [VecesRetweeteado] = " + str(Veces) + " WHERE [idTweet] = '" + idTweet + "'"
            
            ConsultaSQL = Consulta
            cursor.execute(ConsultaSQL)              
            
        except  Exception as e:
            self.miLog.Salidaln("ERROR Actualizando Retweets")
            self.miLog.Salidaln(Consulta)
            self.miLog.Salidaln(e.args)
        
         
        


#------------------------------------------------------------------------------------------------------------------------------
        
    def ParcialTimeline(self, ListaTL):
        try:
            self.miLog.Salidaln("")
            self.miLog.Salidaln("Regenerando Parcial Timeline en SQL Server...")  
            Elemento = ta_DataCleaner.TimeLine
            ConsultaSQL = b''
            
            for Elemento in ListaTL:
                ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(Elemento.m_Fecha,'%a %b %d %H:%M:%S +0000 %Y'))
                tso = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(Elemento.m_FechaOriginal,'%a %b %d %H:%M:%S +0000 %Y'))
               
               
                try:
                    strSQL = u"INSERT INTO [dbo].[timeline] ([idTweet],[idUsuario], [idUsuarioOriginal], [Fecha], [FechaOriginal], [Texto], [Retweet], [OrigenRetweet], [VecesRetweeteado]) VALUES ("
                    strSQL = strSQL + "'" + str(Elemento.m_idTweet) + "',"
                    strSQL = strSQL + "'" + str(Elemento.m_idUsuario) + "',"
                    strSQL = strSQL + "'" + str(Elemento.m_idUsuarioOriginal) + "',"
                    strSQL = strSQL + "'" + str(ts) + "',"
                    strSQL = strSQL + "'" + str(tso) + "',"
                    strSQL = strSQL + "'" + Elemento.m_Texto + "',"
                    strSQL = strSQL + str(Elemento.m_reTweet)  + ","
                    strSQL = strSQL + "'" + Elemento.m_OrigenRetweet + "',"
                    strSQL = strSQL + "0)"
                    ConsultaSQL = strSQL.encode('iso-8859-1','ignore').decode('utf-8','ignore')
                    self.m_conSQL.cursor().execute(ConsultaSQL)              
                    #self.m_conSQL.commit()
                    self.miLog.Salida(".")
                except : 
                      
                    strSQL = u"UPDATE [dbo].[timeline] SET "
                    strSQL = strSQL + "[Fecha] = '" + str(ts) + "', "
                    strSQL = strSQL + "[Retweet] = " + str(Elemento.m_reTweet) + ", "
                    strSQL = strSQL + "[OrigenRetweet] = '" + str(Elemento.m_OrigenRetweet) + "', "
                    strSQL = strSQL + "[idUsuarioOriginal] = '" + str(Elemento.m_idUsuarioOriginal) + "', "
                    strSQL = strSQL + "[FechaOriginal] = '" + str(tso) + "', "
                    strSQL = strSQL + "[VecesRetweeteado] = 0 " 
                    strSQL = strSQL + " WHERE [idTweet] = '" + str(Elemento.m_idTweet) + "'"
                    ConsultaSQL = strSQL.encode('iso-8859-1','ignore').decode('utf-8','ignore')
                    
                    self.m_conSQL.cursor().execute(ConsultaSQL)              
                    
                    self.miLog.Salida("U")
                self.m_conSQL.commit()   
                if (Elemento.m_reTweet == 1):
                        
                        self.VecesReteet(str(Elemento.m_OrigenRetweet))


        except Exception as e: 
            self.miLog.Salidaln("ERROR Volcando a SQL los tweets ")
            self.miLog.Salidaln(strSQL)
            self.miLog.Salidaln(e.args)
            return -1			
     


#------------------------------------------------------------------------------------------------------------------------------
        
    def ActualizaSentinelGoogle (self,ListaTL):
        try:
            self.miLog.Salidaln("")
            self.miLog.Salidaln("Regenerando Sentinel Google en SQL Server...")  
            Elemento = ta_DataCleaner.TimeLine
            ConsultaSQL = b''
            for Elemento in ListaTL:
               strSQL = u"UPDATE [dbo].[timeline] SET "
               strSQL = strSQL + "[SentinelGoogle] = " + str(Elemento.m_SentinelGoogle) + ","
               strSQL = strSQL + "[AccuracyGoogle] = " + str(Elemento.m_AccuracyGoogle) + " WHERE [idTweet] = '" + str(Elemento.m_idTweet) + "'"
               ConsultaSQL = strSQL.encode('iso-8859-1','ignore').decode('utf-8','ignore')
               self.m_conSQL.cursor().execute(ConsultaSQL)              
                    
               self.miLog.Salida(".")
               self.m_conSQL.commit()   

            self.miLog.Salidaln("OK...") 
        except Exception as e: 
            self.miLog.Salidaln("ERROR Volcando a SQL los tweets ")
            self.miLog.Salidaln(strSQL)
            self.miLog.Salidaln(e.args)
            return -1	
        
#------------------------------------------------------------------------------------------------------------------------------

    def ActualizaSentinelGoogleTweet (self, idTweet, Sentinel, Accuracy):
        try:
            
            ConsultaSQL = b''
            strSQL = u"UPDATE [dbo].[timeline] SET "
            strSQL = strSQL + "[SentinelGoogle] = " + str(Sentinel) + ","
            strSQL = strSQL + "[AccuracyGoogle] = " + str(Accuracy) + " WHERE [idTweet] = '" + str(idTweet) + "'"
            ConsultaSQL = strSQL.encode('iso-8859-1','ignore').decode('utf-8','ignore')
            self.m_conSQL.cursor().execute(ConsultaSQL)              
                    
            self.m_conSQL.commit()   
            self.miLog.Salida(".")

        except Exception as e: 
            self.miLog.Salida("E")
            self.miLog.Salidaln(strSQL)
            self.miLog.Salidaln(e.args)
            return -1	
        
#------------------------------------------------------------------------------------------------------------------------------


    def ActualizaEsBusiness (self, idTweet, esBusiness):
        try:
            strSQL = u"UPDATE [dbo].[timeline] SET "
            strSQL = strSQL + "[esBusiness] = " + str(esBusiness) 
            strSQL = strSQL + " WHERE [idTweet] = '" + idTweet + "'"
            ConsultaSQL = strSQL.encode('iso-8859-1','ignore').decode('utf-8','ignore')
            self.m_conSQL.cursor().execute(ConsultaSQL)              
                    
            self.miLog.Salida(".")
            self.m_conSQL.commit()   

            
        except Exception as e: 
            self.miLog.Salida("E")
            self.miLog.Salidaln(strSQL)
            self.miLog.Salidaln(e.args)
            return -1	
        
#------------------------------------------------------------------------------------------------------------------------------        
    def ActualizaSentinelMicrosoft (self,ListaTL):
        try:
            self.miLog.Salidaln("")
            self.miLog.Salidaln("Regenerando Sentinel Microsoft en SQL Server...")  
            Elemento = ta_DataCleaner.TimeLine
            ConsultaSQL = b''
            for Elemento in ListaTL:
               ListaFrases = str(Elemento.m_Frases).replace(",","|")
               ListaFrases = ListaFrases.replace("'","")
               ListaFrases = ListaFrases.replace("[","")
               ListaFrases = ListaFrases.replace("]","")
               strSQL = u"UPDATE [dbo].[timeline] SET "
               strSQL = strSQL + "[SentinelMs] = " + str(Elemento.m_SentinelMS) + ","
               strSQL = strSQL + "[Frases] = '" + ListaFrases + "' WHERE [idTweet] = '" + str(Elemento.m_idTweet) + "'"
               ConsultaSQL = strSQL.encode('iso-8859-1','ignore').decode('utf-8','ignore')
               self.m_conSQL.cursor().execute(ConsultaSQL)              
                    
               self.miLog.Salida(".")
               self.m_conSQL.commit()   

            self.miLog.Salidaln("OK...") 
        except Exception as e: 
            self.miLog.Salidaln("ERROR Volcando a SQL los tweets ")
            self.miLog.Salidaln(strSQL)
            self.miLog.Salidaln(e.args)
            return -1	        
        		
                
        
        
    def UpdateSentibelBusiness(self, idTweet,Sentinel):
        try:
            ConsultaSQL = b''
            strSQL = u"UPDATE [dbo].[timeline] SET "
            if (Sentinel == "negativo"): strSQL = strSQL + "[SentinelBusiness] = 0 "
            if (Sentinel == "neutro"): strSQL = strSQL + "[SentinelBusiness] = 0.5 "
            if (Sentinel == "positivo"): strSQL = strSQL + "[SentinelBusiness] = 1 "
            strSQL = strSQL + " WHERE [idTweet] = '" + str(idTweet) + "'"
            ConsultaSQL = strSQL.encode('iso-8859-1','ignore').decode('utf-8','ignore')
            self.m_conSQL.cursor().execute(ConsultaSQL)              
                    
            self.miLog.Salida(".")
            self.m_conSQL.commit()   

            
        except Exception as e: 
            self.miLog.Salidaln("ERROR Volcando a SENTINEL SQL los tweets ")
            self.miLog.Salidaln(strSQL)
            self.miLog.Salidaln(e.args)
            return -1	        
        