#!/usr/bin/python
import subprocess
import sys
import logging

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', filename="Plex-Automatic-Preroll.log", level=logging.INFO)

try:
    from plexapi.server import PlexServer

except:
    logging.error("PlexAPI Not Installed")
    print('\033[91mERROR:\033[0m PlexAPI is not installed.')
    x = input("Do you want to install it? y/n:")
    if x == 'y':
        logging.info("Installing PlexAPI")
        subprocess.check_call([sys.executable, "-m", "pip", "install", 'PlexAPI==4.13.4'])
        from plexapi.server import PlexServer
    elif x == 'n':
        logging.info("Exiting...")
        sys.exit()

import re
import requests
import yaml
from urllib.parse import quote_plus, urlencode
import datetime

from plexapi import media, utils, settings, library
from plexapi.base import Playable, PlexPartialObject
from plexapi.exceptions import BadRequest, NotFound

from argparse import ArgumentParser
import os
import random
import pathlib
from configparser import *

print('#############################')
print('#                           #')
print('#  Plex Automated Preroll!  #')
print('#                           #')
print('#############################' + '\n')


file = pathlib.Path("config.yml")
if file.exists():
    logging.info("config.yml found. Let's get to work.")
    print('Pre-roll updating...')
else:
    logging.warning("No config.yml found. Need to set one up. Prompting user.")
    Master = ','
    print('No config file found! Lets set one up!')
    file1 = open("config.yml", "w+")
    file1.write("Plex: " + "\n")
    x = input("Enter your (https) plex url:")
    file1.write("  url: " + x + "\n")
    x = input("Enter your plex token: (not sure what that is go here "
              "https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/): ")
    file1.write("  token: " + x + "\n")
    file1.write("Paths: " + "\n")
    x = input("Enter the root folder where your PreRolls are stored: (ending with a \)")
    file1.write("  host_dir: " + x + "\n")
    file1.write("MasterList: "  + "\n")
    x = input("Do you want to enable a Masterlist of Trailers? (Y/N)")
    if x.lower() == 'y':
        file1.write("  UseMaster: " + "Yes" + "\n")
        x = input("Do you want Plex to play the items in the Masterlist randomly? (Y/N)")
        if x.lower() == 'y':
            Master = ';'
            file1.write("  MasterRandom: " + "Yes" + "\n")
        else:
            Master = ','
            file1.write("  MasterRandom: " + "No" + "\n")
        file1.write("# If the path for the Master List is left blank the script will create the path " + "\n")
        file1.write("# based on if Monthly, Weekly, or Daily are set to be used in the Master List " + "\n")
        file1.write("# otherwise you can populate the path with your own set of trailers" + "\n")
        file1.write("  Path: ")
        x = input("Enter Masterlist path(s) or folder name:")
        file1.write(x + "\n")
    else:
        file1.write("  UseMaster: " + "No"  + "\n")
        file1.write("  MasterRandom: " + "No"  + "\n")
        file1.write("  # If the path for the Master List is left blank the script will create the path " + "\n")
        file1.write("  # based on if Monthly, Weekly, or Daily are set to be used in the Master List " + "\n")
        file1.write("  # otherwise you can populate the path with your own set of trailers" + "\n")
        file1.write("  Path: "  + "\n")
    file1.write("Monthly: "  + "\n")
    x = input("Do you want to enable Monthly Trailers? (Y/N)")
    if x.lower() == 'y':
        print('Make sure plex can access the path(s) or folders you enter!')
        res = []
        x = input("Enter the January trailer path(s) or folder name:" + "\n")
        if len(x) > 0:
            res = res + re.split(',|;', x)
        file1.write("  Jan: " + x  + "\n")
        x = input("Enter the February trailer path(s) or folder name:" + "\n")
        if len(x) > 0:
            res = res + re.split(',|;', x)
        file1.write("  Feb: " + x  + "\n")
        x = input("Enter the March trailer path(s) or folder name:" + "\n")
        if len(x) > 0:
            res = res + re.split(',|;', x)
        file1.write("  Mar: " + x  + "\n")
        x = input("Enter the April trailer path(s) or folder name:" + "\n")
        if len(x) > 0:
            res = res + re.split(',|;', x)
        file1.write("  Apr: " + x  + "\n")
        x = input("Enter the May trailer path(s) or folder name:" + "\n")
        if len(x) > 0:
            res = res + re.split(',|;', x)
        file1.write("  May: " + x  + "\n")
        x = input("Enter the June trailer path(s) or folder name:" + "\n")
        if len(x) > 0:
            res = res + re.split(',|;', x)
        file1.write("  June: " + x  + "\n")
        x = input("Enter the July trailer path(s) or folder name:" + "\n")
        if len(x) > 0:
            res = res + re.split(',|;', x)
        file1.write("  July: " + x  + "\n")
        x = input("Enter the August trailer path(s) or folder name:" + "\n")
        if len(x) > 0:
            res = res + re.split(',|;', x)
        file1.write("  Aug: " + x  + "\n")
        x = input("Enter the September trailer path(s) or folder name:" + "\n")
        if len(x) > 0:
            res = res + re.split(',|;', x)
        file1.write("  Sept: " + x  + "\n")
        x = input("Enter the October trailer path(s) or folder name:" + "\n")
        if len(x) > 0:
            res = res + re.split(',|;', x)
        file1.write("  Oct: " + x  + "\n")
        x = input("Enter the November trailer path(s) or folder name:" + "\n")
        if len(x) > 0:
            res = res + re.split(',|;', x)
        file1.write("  Nov: " + x  + "\n")
        x = input("Enter the December trailer path(s) or folder name:" + "\n")
        if len(x) > 0:
            res = res + re.split(',|;', x)
        file1.write("  Dec: " + x  + "\n")
        x = input("Do you want to use the Monthly list in the Master list? (Y/N)")
        if x.lower() == 'y':
            file1.write("  MasterList: Yes" + "\n")
            listToStr = Master.join([str(elem) for elem in res])
            file1.write("  MasterListValue: " + listToStr)
        else:
            file1.write("  MasterList: No" + "\n")
            file1.write("  MasterListValue: " + "\n")
        file1.write("  UseMonthly: Yes" + "\n")
    else:
        file1.write("  Jan: " + "\n")
        file1.write("  Feb: " + "\n")
        file1.write("  Mar: " + "\n")
        file1.write("  Apr: " + "\n")
        file1.write("  May: " + "\n")
        file1.write("  June: " + "\n")
        file1.write("  July: " + "\n")
        file1.write("  Aug: "  + "\n")
        file1.write("  Sept: " + "\n")
        file1.write("  Oct: " + "\n")
        file1.write("  Nov: " + "\n")
        file1.write("  Dec: " + "\n")
        file1.write("  MasterList: No" + "\n")
        file1.write("  MasterListValue: " + "\n")
        file1.write("  UseMonthly: No" + "\n")
    file1.write("Weekly: " + "\n")
    x = input("Do you want to enable Weekly Trailers? (Y/N)")
    if x.lower() == 'y':
        print('Make sure plex can access the path you enter!')
        print("Enter the Start Date: " + "\n")
        year = int(input('Enter a year'))
        month = int(input('Enter a month'))
        day = int(input('Enter a day'))
        date1 = datetime.date(year, month, day)
        file1.write("  StartDate: " + date1 + "\n")
        print("Enter the End Date:")
        year = int(input('Enter a year'))
        month = int(input('Enter a month'))
        day = int(input('Enter a day'))
        date1 = datetime.date(year, month, day + "\n")
        file1.write("  EndDate: " + date1)
        x = input("Enter the trailer path(s) or folder name:" + "\n")
        file1.write("  Path: " + x)
        x = input("Do you want to use the Weekly list in the Master list? (Y/N)")
        if x.lower() == 'y':
            file1.write("  MasterList: Yes" + "\n")
        else:
            file1.write("  MasterList: No" + "\n")
        file1.write("  UseDaily: Yes" + "\n")
    else:
        file1.write("  StartDate: " + "\n")
        file1.write("  EndDate: " + "\n")
        file1.write("  Path: " + "\n")
        file1.write("  MasterList: No" + "\n")
        file1.write("  UseWeekly: No" + "\n")
    file1.write("Daily: " + "\n")
    x = input("Do you want to enable Daily Trailers? (Y/N)")
    if x.lower() == 'y':
        print('Make sure plex can access the path you enter!')
        print("Enter the Start Date: ")
        year = int(input('Enter a year'))
        month = int(input('Enter a month'))
        day = int(input('Enter a day'))
        date1 = datetime.date(year, month, day)
        file1.write("  StartDate: " + date1 + "\n")
        print("Enter the End Date:")
        year = int(input('Enter a year'))
        month = int(input('Enter a month'))
        day = int(input('Enter a day'))
        date1 = datetime.date(year, month, day)
        file1.write("  EndDate: " + date1 + "\n")
        x = input("Enter the trailer path(s) or folder name:")
        file1.write("  Path: " + x + "\n")
        x = input("Do you want to use the Daily list in the Master list? (Y/N)")
        if x.lower() == 'y':
            file1.write("  MasterList: Yes" + "\n")
        else:
            file1.write("  MasterList: No" + "\n")
        file1.write("  UseDaily: Yes" + "\n")
    else:
        file1.write("  StartDate: " + "\n")
        file1.write("  EndDate: " + "\n")
        file1.write("  Path: " + "\n")
        file1.write("  MasterList: No" + "\n")
        file1.write("  UseDaily: No" + "\n")
    file1.write("Misc: " + "\n")
    x = input("Do you want to enable Misc (Random with one static trailer) Trailers? (Y/N)")
    if x.lower() == 'y':
        print('Make sure plex can access the path you enter!')
        x = input("Enter the trailer path(s) or folder name:")
        file1.write("  Path: " + x + "\n")
        x = input("Enter the static trailer path:")
        file1.write("  StaticTrailer: " + x + "\n")
        x = input("Enter the number of trailers to use ex: Path contains 5 trailers you set this value to 2 the "
                  "program will pick two at random as well as the static trailer to play in order:")
        file1.write("  TrailerListLength: " + x + "\n")
        file1.write("  UseMisc: Yes" + "\n")
    else:
        file1.write("  Path: " + "\n")
        file1.write("  StaticTrailer: " + "\n")
        file1.write("  TrailerListLength: " + "\n")
        file1.write("  UseMisc: No" + "\n")
    logging.info("config.yml created!")
    print('config file (config.yml) created')
    file1.close()

def getArguments():
    name = 'Automated-Pl                                                                                                                   ex-Preroll-Trailers'
    version = '1.2.0'
    parser = ArgumentParser(description='{}: Set monthly trailers for Plex'.format(name))
    parser.add_argument("-v", "--version", action='version', version='{} {}'.format(name, version), help="show the version number and exit")
    args = parser.parse_args()

#Automatically generate preroll based on a list of files in a folder
def generatePreRoll(HostDirectory, PreRollPath):
    types = ['.mp4', '.avi', '.mkv', '.mov']
    PreRollFiles = ''
    if any(type in PreRollPath for type in types):
        return PreRollPath
    else:
        PreRollPath = os.path.join(HostDirectory,PreRollPath,'')
        for type in types:
            for file in os.listdir(PreRollPath):
                if file.endswith(type):
                    PreRollFiles+=os.path.join(PreRollPath, file)+';'
        return PreRollFiles

def main():
    sort = ','
    x = datetime.date.today()
    res = "null"
    logging.info("Retreiving config from file config.yml")
    #Open config
    with open('config.yml', 'r') as file:
        doc = yaml.load(file, Loader=yaml.SafeLoader)
    if str(doc["Monthly"]["MasterList"]).lower() == 'true':
        res = re.split(',|;', doc["Monthly"]["MasterListValue"])
    if str(doc["Weekly"]["MasterList"]).lower() == 'true':
        res = res + re.split(',|;', doc["Weekly"]["Path"])
    if str(doc["Daily"]["MasterList"]).lower() == 'true':
        res = res + re.split(',|;', doc["Daily"]["Path"])
    if str(doc["MasterList"]["MasterRandom"]).lower() == 'true' and res != 'null':
        MasterlistToStr = ';'.join([str(elem) for elem in res])
    if str(doc["MasterList"]["MasterRandom"]).lower() == 'false' and res != 'null':
        MasterlistToStr = ','.join([str(elem) for elem in res])
    if doc["MasterList"]["Path"] is not None:
        MasterlistToStr = doc["MasterList"]["Path"]
    if doc["Paths"]["host_dir"] is not None:
        host_dir = doc["Paths"]["host_dir"]
    logging.info("Config loaded")

    # Arguments
    arguments = getArguments()
    #Thanks to https://github.com/agrider for the reordering and error handling for pre-roll paths
    if doc["Plex"]["url"] is not None:
        session = requests.Session()
        session.verify = False
        requests.packages.urllib3.disable_warnings()
        plex = PlexServer(doc["Plex"]["url"], doc["Plex"]["token"], session, timeout=None)
        prerolls = None
        if str(doc["Monthly"]["UseMonthly"]).lower() == 'true':
            prerolls = doc["Monthly"][x.strftime("%b")]
        if str(doc["Weekly"]["UseWeekly"]).lower() == 'true':
            if doc["Weekly"]["StartDate"] <= x <= doc["Weekly"]["EndDate"]:
                prerolls = doc["Weekly"]["Path"]
        if str(doc["Daily"]["UseDaily"]).lower() == 'true':
            if doc["Daily"]["StartDate"] <= x <= doc["Daily"]["EndDate"]:
               prerolls = doc["Daily"]["Path"]
        if str(doc["Misc"]["UseMisc"]).lower() == 'true':
            if str(doc["Misc"]["Random"]).lower() == 'true':
                sort = ';'
            else:
                sort = ','
            res = re.split(',|;', doc["Misc"]["Path"])
            i = 1
            while i < int(doc["Misc"]["TrailerLength"]):
                trailer = trailer + sort + res[random.randint(0, len(res) - 1)]
                i += 1
            trailer = trailer + sort + doc["Misc"]["StaticTrailer"]
            prerolls = trailer
        if prerolls is None:
            if str(doc["MasterList"]["UseMaster"]).lower() == 'true':
                prerolls = MasterlistToStr
            else:
                print("Error: No video paths configured after applying videos matching today's date and master if enabled!")
                raise Exception("No video paths configured after applying videos matching today's date and master if enabled!")
        prerolls = generatePreRoll(host_dir, prerolls)
        logging.debug("Preroll configured to: " + prerolls)
        plex.settings.get('cinemaTrailersPrerollID').set(prerolls)    
        plex.settings.save()
        print('Pre-roll updated')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(e)
        print(e)
