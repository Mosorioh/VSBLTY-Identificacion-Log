import os
import os, sys
import time
import datetime
from shutil import rmtree 
from os import makedirs
from os import remove
import shutil

import json
from io import open

# Date Time
from datetime import date
from datetime import datetime, timedelta
import datetime 
# DB
import pymysql


try:
    NewFolderTest = "C:/Users/Mijail/Documents/VSBLTY-Identificacion-Log/Log-Result/"
    FolderSavephotos = "C:/ProgramData/VsbltyTmp/KingSalmon/"
    print ("Moviendo Folder SavePhotos: ")
    shutil.move(FolderSavephotos, NewFolderTest)
except FileExistsError:
    print ("folder SavePhotos No Exists") 