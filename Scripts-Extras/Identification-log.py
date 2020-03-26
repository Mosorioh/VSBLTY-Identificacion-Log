import json
import os, sys
from io import open
# import pymysql.cursors

# Date Time
import time
import datetime 
from datetime import date
from datetime import datetime
# DB
import pymysql


#///////////////////////////////////////////
# GET-Endpoint-Test
# Funcion para obtener de la DB, la ultima prueba que se ejecuto para el Endpoint
# Si la respuesta es Null, se TestNumero = 1
#//////////////////////////////////////////
# Connect to the database
def TestNumero():
    #print (EndpointId)
    connection = pymysql.connect(host='192.168.100.51',
                                    user='Qatest',
                                    password='Quito.2019',
                                    db='Log-identificacion',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `TestNumero` FROM `Identificacion` ORDER BY `TestNumero` DESC LIMIT 1"
            cursor.execute(sql) 
            result = cursor.fetchone()
            #print (result)
            if result == None:
                TestNumero = 1
                #print (TestNumero)
            else:
                TestNumero = int(result.get('TestNumero')) + 1
                #print (TestNumero)
            #input ()
    finally:
        connection.close()
    return TestNumero

TestNumero = TestNumero()
today = date.today()




#///////////////////////////////////////////
# Funcion para obtener todas las lineas de Identificacion, desde el archivo de Log
#//////////////////////////////////////////
def GetVersionClient():
    #//////////////////////////////////
	# Verificar la cantidad de archivos que existen dentro del directorio
	# Indicamos la ruta de donde se quieren leer los archivos
    path= "C:/ProgramData/Vsblty/KingSalmon/"
    dirs = os.listdir(path)
    i = 0
    # ////////////////////////////////////////////////////////////
    # Por cada Archivo dentro del directorio, se realiza un ciclo for para recorrer cada linea y verificar hits  
    # ////////////////////////////////////////////////////////////
    for file in dirs:
        ruta = "C:/ProgramData/Vsblty/KingSalmon/"
        archivo = file
        rutacompleta = ruta + archivo
        print ("/////////////////////////////////////////////////////////////////////////////////////////////////////////////")
        print ("/////////////////////////////////////////////////////////////////////////////////////////////////////////////")
        print ("File: ",rutacompleta)
        print ("/////////////////////////////////////////////////////////////////////////////////////////////////////////////")
        print ("/////////////////////////////////////////////////////////////////////////////////////////////////////////////")
        # La aplicaicon lee y guarada en la variable "archivo_texto" toda la informacion 
        archivo_texto=open (rutacompleta, "r")

        # Se lee Linea por linea
        lineas_texto=archivo_texto.readlines()

        # ////////////////////////////////////////////////////////////
        # Inicio de Busqueda
        # Por cada linea se valida si contiene el Texto que se desea encontrar 
        # Para este caso es: "[EDGE Detection] Identified Person >> Name:"
        # ////////////////////////////////////////////////////////////

        for ClientLine in lineas_texto:
            if "[EDGE Detection] Identified Person >> Name:" in ClientLine: #busqueda por el parametro 
                # ////////////////////////////////////////////////////////////
                # Obtener la posicion de cada Propiedad
                # ////////////////////////////////////////////////////////////
                Timeline = ClientLine[0:19]

                PosicionNamePerson = ClientLine.find("Name") + 6
                PosicionPersonId = ClientLine.find("PersonId")
                PosicionGroupId  = ClientLine.find("GroupId") 
                PosicionMatchProbability = ClientLine.find("MatchProbability") 
                PosicionLocalPersistedFaceId = ClientLine.find("LocalPersistedFaceId")

                CortePersonId = PosicionPersonId + 10
                CorteGroupId = PosicionGroupId + 9 
                CorteMatchProbability = PosicionMatchProbability + 18
                CorteLocalPersistedFaceId = ClientLine.find("LocalPersistedFaceId") + 22

                # ///////////////////////////////////////////////////////////
                # print ("PosicionNamePerson ", PosicionNamePerson)
                # print ("PosicionPersonId ", PosicionPersonId)
                # print ("PosicionGroupId ", PosicionGroupId)
                # print ("PosicionMatchProbability ", PosicionMatchProbability)
                # print ("PosicionLocalPersistedFaceId ", PosicionLocalPersistedFaceId)

                # ///////////////////////////////////////////////////////////
                #input ()
                # ///////////////////////////////////////////////////////////
                NamePerson = ClientLine[PosicionNamePerson:PosicionPersonId]
                PersonId = ClientLine[CortePersonId:PosicionGroupId]
                GroupId = ClientLine[CorteGroupId:PosicionMatchProbability]
                MatchProbability = ClientLine[CorteMatchProbability:PosicionLocalPersistedFaceId]
                LocalPersistedFaceId = ClientLine[CorteLocalPersistedFaceId:-40]

                """    
                print ("Name person:", NamePerson)
                print ("Id   person:", PersonId)
                print ("GroupId    :", GroupId)
                print ("MatchPro   :", MatchProbability)
                print ("LocalPer   :", LocalPersistedFaceId)
                input ()
                """

                # ////////////////////////////////////////////////////////////
                # Obtener el valor de cada propiedad segun la posicion
                # ///////////////////////////////////////////////////////////

                # ////////////////////////////////////////////////////////////
                # imprimir los valores encontrados en cada linea
                # ///////////////////////////////////////////////////////////
                i +=1
                print ("Date Test:         ", today)
                print ("Test Numero:       ", TestNumero)
                print ("Item:              ", i)
                print ("File:              ", archivo)
                print ("Time:              ", Timeline)
                print ("Name:              ", NamePerson)
                print ("PersonId:          ", PersonId)
                print ("Match Probability: ", MatchProbability)
                print ("GroupId:           ", GroupId)
                print ("LocalPersistedId:  ", LocalPersistedFaceId)
                print ("/////////////////////////////////////////////////////////////////////////////////////////////////////////////")
                #input ()
                
                # Connect to the database
                connection = pymysql.connect(host='192.168.100.51',
                                            user='Qatest',
                                            password='Quito.2019',
                                            db='Log-identificacion',
                                            charset='utf8mb4',
                                            cursorclass=pymysql.cursors.DictCursor)
                try:
                    with connection.cursor() as cursor:
                # Create a new record
                                        
                        sql = "INSERT INTO `Identificacion` (`Item`, `File`, `Timeline`, `Name`, `PersonId`, `MatchProbability`, `GroupId`, `LocalPersistedId`, `TestNumero`, `FechaTest`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        cursor.execute(sql, (i, archivo, Timeline, NamePerson, PersonId, MatchProbability, GroupId, LocalPersistedFaceId, TestNumero, today))
                         


                # connection is not autocommit by default. So you must commit to save
                # your changes.
                        connection.commit()

                finally:
                    connection.close()

    return 


input ()
