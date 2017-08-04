# TrustAnalytics

## Descripción
Se trata de un proyecto nacido en la Escuala de Negocio **MBIT School** como proyecto final de Master Executive Data Science.

Se ha desarrollado una serie de scripts basados en Python, que son capaces de leer los Tweets de un criterio de negocio específico y analuizar el sentimiento de dicho texto mejorando los resultados del API estandar de otros proveedores de servicios API de Análisis Sintáctico.

Como plataforma y tecnologías, se han usado:
   #### Microsoft Azure como base de plataforma
   #### MongoDB como Repositorio para ingesta de datos
   #### Microsoft Azure Machine Learniing como plataforma de uno de los módulos d emachine Laerning del proyecto (consta de dos)
   #### Azure SQL Server como respositorio de los datos debidamente tratados y como repsoitorio de visualización
   #### Power BI como solución de visualización.

## Requisitos

La plataforma está testada bajo SO Linux.
Se dispone de un fichero descriptivo de los requisitos previos del sistema "Requisitos2.txt"

## ¿Cómo funciona?
La forma de funcionamiento es en distintas fases y está pensado para que todas sean independientes entre si y destinadas a ser programadas en un CRON de Linux a distintas horas.

#### Fase 1: Es el script Python encargado de la ingesta de Twitter y volcado a MongoDB. No hace tratamiento alguno de los datos, dado que solo se encarga de la ingesta de los mismos.
             python managertimeline.py

#### Fase 2: Este script se encarga de discernir entre los tweets que son relevantes para el negocio de los que no. 
             python ta_ML1.py

#### Fase 3: Este es el script encargado de limpieza de datos y analizar el Sentimiento del Tweet (POSITIVO, NEUTRO o NEGATIVO)
             python ta_PredictSentinelBusiness.py

#### Fase 4: Con PowerBI de Microsoft se genera la capa de visualización.			 
              
   
## Equipo
Por orden alfabético...

* Pablo Blanco
* Horacio Fernández
* Cristina Florín 
* Luis Carlos Prieto
