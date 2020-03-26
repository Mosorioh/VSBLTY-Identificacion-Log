import os
import os, sys
import time
import datetime
from shutil import rmtree 
from os import makedirs
from os import remove
import shutil

# comentario
import json
from io import open

# Date Time
from datetime import date
from datetime import datetime, timedelta
import datetime 
# DB
import pymysql


#/////////////////////////////////////////////////////
#--------- Proceso 1 -------------
#/////////////////////////////////////////////////////
print ("")
print ("///////////////////////////////////////////////////////////////////")
print ("PROCESS (1)")
print ("///////////////////////////////////////////////////////////////////")
print ("- Remove Folder From Log and Savephotos")
print ("- Obtain test sequence (Test number)")
print ("- Verify and Create Test Backup folder (C:/ProgramData/Vsblty-Test/)")
print ("///////////////////////////////////////////////////////////////////")

#crear carpeta
try:
    # change the destination path
    print (" - Removiendo Carpetas logs")
    PathLog = "C:/ProgramData/Vsblty/KingSalmon/"
    rmtree(PathLog)
    time.sleep(.200)
    
except FileNotFoundError:
    print (" - Folder KingSalmon No Exists")

#crear carpeta
try:
    # change the destination path
    print (" - Removiendo Carpetas savephotos")
    PathsavePhotos = "C:/ProgramData/VsbltyTmp/"
    rmtree(PathsavePhotos)
    
except FileNotFoundError:
    print (" - Folder VsbltyTmp No Exists")


#input ()

#///////////////////////////////////////////
# GET-Endpoint-Test
# Funcion para obtener de la DB, la ultima prueba que se ejecuto para el Endpoint
# Si la respuesta es Null, se TestNumero = 1
#//////////////////////////////////////////
# Connect to the database
def TestNumero():
    #print (EndpointId)
    connection = pymysql.connect(host='181.199.66.129',
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

#/////////////////////////////////////////////////
#
#--------- Setting -------------
#
#/////////////////////////////////////////////////////
NumerodeCiclos = 8
DuracionTest = 60
CountTest = 1
DateTest = str(datetime.datetime.now())
Fecha = DateTest[0:10]
TestNumero = TestNumero()
today = date.today()

#crear carpeta
try:
    # change the destination path
    FolderTest = "C:/ProgramData/Vsblty-Test/Identification-Results/"  + Fecha + " TEST - " + str(TestNumero)
    makedirs(FolderTest)
    print (" - Creating Folder of Test-", TestNumero)
except FileExistsError:
    print (" - Folder Exists")




#/////////////////////////////////////////////////////
#--------- Proceso 2 -------------
#/////////////////////////////////////////////////////
print ("")
print ("*****************************************************************")
print ("///////////////////////////////////////////////////////////////////")
print ("PROCESS (2)")
print ("///////////////////////////////////////////////////////////////////")
print (" - Inicio de Test y Ciclos")
print ("  --- Setting Test")
print ("       - Date: ", Fecha)
print ("       - Test Numero: ", TestNumero)
print ("       - Ciclos Definidos: ", NumerodeCiclos)
print ("       - Duracion por Ciclo: ", DuracionTest, "Segundos")
print ("")


#////////////////////////////////////////
# Iniciar el Cliente
#///////////////////////////////////////
while CountTest <= NumerodeCiclos:
    print ("///////////////////////////////////////////////////////////////////")
    print ("                       New Test Cycle")
    print ("///////////////////////////////////////////////////////////////////")
    StartTestCliente = str(datetime.datetime.now())
    #
    #crear carpeta
    try:
        # change the destination path
        NewFolderTest = FolderTest + "/"  + Fecha  + " " + "CICLO -" + str(CountTest)
        makedirs(NewFolderTest)
        print (" - Creating Folder of Result Ciclo-", CountTest)
    except FileExistsError:
        print (" - Folder Exists")

    print (" - Test Cycle", CountTest)

    #print ("Start Cliente", StartTestCliente) 
    print (" - Fecha", Fecha)

    #input ()
    # Iniciar Client
    print (" - Start Cliente", StartTestCliente)   
    os.startfile('C:\\Users/Mijail/Documents/VSBLTY-Identificacion-Log/Scripts-Extras/Start-Client.bat')
    print ("***********")
    print ("  -- Client is Running, Analizando Frame and Person...")
    print ("***********")

    
    # Tiempo de espera para cerrar el cliente
    time.sleep(DuracionTest)

    # close Client
    os.system('taskkill -f -im vsb*')
    StopTestCliente =  datetime.datetime.now()
    print ("  -- Stop Client", StopTestCliente)
    print ("***********")
    print ("")
    time.sleep(1)

    #//////////////////////////////////
	# Verificar la cantidad de archivos que existen dentro del directorio
	# Indicamos la ruta de donde se quieren leer los archivos
    path= "C:/ProgramData/Vsblty/KingSalmon/"
    dirs = os.listdir(path)
    i = 0

    print ("********************************************")
    print ("******************************************************")
    print ("          Inicio de Analisis del Log")
    print ("******************************************************")
    print ("********************************************")

    #//////////////////////////////////
	# Verificar la cantidad de archivos que existen dentro del directorio
	# Indicamos la ruta de donde se quieren leer los archivos
    #//////////////////////////////////
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
                print ("Ciclo Test:        ", CountTest)
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
                connection = pymysql.connect(host='181.199.66.129',
                                            user='Qatest',
                                            password='Quito.2019',
                                            db='Log-identificacion',
                                            charset='utf8mb4',
                                            cursorclass=pymysql.cursors.DictCursor)
                try:
                    with connection.cursor() as cursor:
                # Create a new record
                                        
                        sql = "INSERT INTO `Identificacion` (`Item`, `File`, `Timeline`, `Name`, `PersonId`, `MatchProbability`, `GroupId`, `LocalPersistedId`, `TestNumero`, `FechaTest`, `CicloTest`, `StartCiclo`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        cursor.execute(sql, (i, archivo, Timeline, NamePerson, PersonId, MatchProbability, GroupId, LocalPersistedFaceId, TestNumero, today, CountTest, StartTestCliente))
                         


                # connection is not autocommit by default. So you must commit to save
                # your changes.
                        connection.commit()

                finally:
                    connection.close()
        # Close opend file
        archivo_texto.close()

    CountTest +=1 

    # ////////////////////////////////////////////////////////////
    # Por cada Archivo dentro del directorio, se realiza un ciclo for para recorrer cada linea y verificar hits  
    # ////////////////////////////////////////////////////////////
    time.sleep(1)

    #/////////////////////////////////////////////////////
    #--------- Proceso 3 -------------
    #/////////////////////////////////////////////////////

    print ("")
    print ("*****************************************************************")
    print ("/////////////////////////////////////////////////////////////////////////////////")
    print (" - Respaldar Archivos generados en el ciclo de prueba-", CountTest)
    print ("/////////////////////////////////////////////////////////////////////////////////")
    print ("*****************************************************************")
    print ("------ Mover Process LOG -----")    
    print ("/////////////////////////////////////////////////////////////////////////////////")
    for file in dirs:
        Archivo = path + file
        print (" - Moviendo Archivo Log: ", Archivo)
        shutil.move(Archivo, NewFolderTest)
    print ("/////////////////////////////////////////////////////////////////////////////////")
    time.sleep(1)
    print ("------ Mover Process Photos-----")
    print ("///////////////////////////////////////////////////////////////////////////////")

    print ("*****************************************************************")
    try:
        FolderSavephotos = "C:/ProgramData/VsbltyTmp/KingSalmon/"
        print (" - Moviendo Folder SavePhotos: ", Archivo)
        shutil.move(FolderSavephotos, NewFolderTest)
        time.sleep(1)
        #crear carpeta
        #print ("Creando carpetas del savephotos")
        time.sleep(.200)
        makedirs("C:/ProgramData/VsbltyTmp/KingSalmon/StreamSnapshot")
        time.sleep(.200)
        makedirs("C:/ProgramData/VsbltyTmp/KingSalmon/TempPhotos")
        time.sleep(.200)
        makedirs("C:/ProgramData/VsbltyTmp/KingSalmon/TempPhotos/Face API Results")
        time.sleep(.200)
        makedirs("C:/ProgramData/VsbltyTmp/KingSalmon/TempPhotos/LocalDetectedBodies")
        time.sleep(.200)
        makedirs("C:/ProgramData/VsbltyTmp/KingSalmon/TempPhotos/LocalDetectedFaces")
        time.sleep(.200)
        makedirs("C:/ProgramData/VsbltyTmp/KingSalmon/TempPhotos/LocalPhotos")
        time.sleep(.200)
        makedirs("C:/ProgramData/VsbltyTmp/KingSalmon/TempPhotos/NoIdentifiedFaces")
        time.sleep(.200)
        makedirs("C:/ProgramData/VsbltyTmp/KingSalmon/TempPhotos/NoIdentifiedPhotos")
        
    except FileExistsError:
        print (" - folder SavePhotos No Exists")    


    print ("")
    print ("///////////////////////////////////////////////////////////////////////////////")
    print (" - Sleep de 5 Segundo")
    print ("///////////////////////////////////////////////////////////////////////////////")
    time.sleep(5)
    #input() 
print ("*****************************************************************")
print ("*****************************************************************")
print ("End Task Ciclos") 
print ("*****************************************************************")
print ("*****************************************************************")