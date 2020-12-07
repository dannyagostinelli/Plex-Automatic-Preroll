#!/usr/bin/python
import subprocess
import sys
try:
    from plexapi.server import PlexServer

except:
    print('\033[91mERROR:\033[0m PlexAPI is not installed.')
    x = input("Do you want to install it? y/n:")
    if x == 'y':
        subprocess.check_call([sys.executable, "-m", "pip", "install", 'PlexAPI==4.2.0'])
        from plexapi.server import PlexServer
    elif x == 'n':
        sys.exit()

import re
import requests
import yaml
from urllib.parse import quote_plus, urlencode
from datetime import datetime

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
    print('Pre-roll updating...')
else:
    Master = ','
    print('No config file found! Lets set one up!')
    file1 = open("config.yml", "w+")
    file1.write("Plex: ")
    x = input("Enter your (https) plex url:")
    file1.write("  url: " + x)
    x = input("Enter your plex token: (not sure what that is go here: "
              "https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)")
    file1.write("  token: " + x)
    file1.write("MasterList: ")
    x = input("Do you want to enable a Masterlist of Trailers? (Y/N)")
    if x.lower() == 'y':
        file1.write("  UseMaster: " + "Yes")
        x = input("Do you want Plex to play the items in the Masterlist randomly? (Y/N)")
        if x.lower() == 'y':
            Master = ';'
            file1.write("  MasterRandom: " + "Yes")
        else:
            Master = ','
            file1.write("  MasterRandom: " + "No")
        file1.write("# If the path for the Master List is left blank the script will create the path ")
        file1.write("# based on if Monthly, Weekly, or Daily are set to be used in the Master List ")
        file1.write("# otherwise you can populate the path with your own set of trailers")
        file1.write("  Path: ")
    else:
        file1.write("  UseMaster: " + "No")
        file1.write("  MasterRandom: " + "No")
        file1.write("  # If the path for the Master List is left blank the script will create the path ")
        file1.write("  # based on if Monthly, Weekly, or Daily are set to be used in the Master List ")
        file1.write("  # otherwise you can populate the path with your own set of trailers")
        file1.write("  Path: ")
    file1.write("Monthly: ")
    x = input("Do you want to enable Monthly Trailers? (Y/N)")
    if x.lower() == 'y':
        print('Make sure plex can access the path(s) you enter!')
        x = input("Enter the January trailer path(s):")
        res = re.split(',|;', x)
        file1.write("  Jan: " + x)
        x = input("Enter the February trailer path(s):")
        res = res + re.split(',|;', x)
        file1.write("  Feb: " + x)
        x = input("Enter the March trailer path(s):")
        res = res + re.split(',|;', x)
        file1.write("  Mar: " + x)
        x = input("Enter the April trailer path(s):")
        res = res + re.split(',|;', x)
        file1.write("  Apr: " + x)
        x = input("Enter the May trailer path(s):")
        res = res + re.split(',|;', x)
        file1.write("  May: " + x)
        x = input("Enter the June trailer path(s):")
        res = res + re.split(',|;', x)
        file1.write("  June: " + x)
        x = input("Enter the July trailer path(s):")
        res = res + re.split(',|;', x)
        file1.write("  July: " + x)
        x = input("Enter the August trailer path(s):")
        res = res + re.split(',|;', x)
        file1.write("  Aug: " + x)
        x = input("Enter the September trailer path(s):")
        res = res + re.split(',|;', x)
        file1.write("  Sept: " + x)
        x = input("Enter the October trailer path(s):")
        res = res + re.split(',|;', x)
        file1.write("  Oct: " + x)
        x = input("Enter the November trailer path(s):")
        res = res + re.split(',|;', x)
        file1.write("  Nov: " + x)
        x = input("Enter the December trailer path(s):")
        res = res + re.split(',|;', x)
        file1.write("  Dec: " + x)
        x = input("Do you want to use the Monthly list in the Master list? (Y/N)")
        if x.lower() == 'y':
            file1.write("  MasterList: Yes")
        else:
            file1.write("  MasterList: No")
        listToStr = Master.join([str(elem) for elem in res])
        file1.write("  MasterListValue: " + listToStr)
        file1.write("  UseMonthly: Yes")
    else:
        file1.write("  Jan: ")
        file1.write("  Feb: ")
        file1.write("  Mar: ")
        file1.write("  Apr: ")
        file1.write("  May: ")
        file1.write("  June: ")
        file1.write("  July: ")
        file1.write("  Aug: ")
        file1.write("  Sept: ")
        file1.write("  Oct: ")
        file1.write("  Nov: ")
        file1.write("  Dec: ")
        file1.write("  MasterList: No")
        file1.write("  MasterListValue: ")
        file1.write("  UseMonthly: No")
    file1.write("Weekly: ")
    x = input("Do you want to enable Weekly Trailers? (Y/N)")
    if x.lower() == 'y':
        print('Make sure plex can access the path you enter!')
        print("Enter the Start Date: \n")
        year = int(input('Enter a year'))
        month = int(input('Enter a month'))
        day = int(input('Enter a day'))
        date1 = datetime.date(year, month, day)
        file1.write("  StartDate: " + date1)
        print("Enter the End Date:")
        year = int(input('Enter a year'))
        month = int(input('Enter a month'))
        day = int(input('Enter a day'))
        date1 = datetime.date(year, month, day)
        file1.write("  EndDate: " + date1)
        x = input("Enter the trailer path(s):")
        file1.write("  Path: " + x)
        x = input("Do you want to use the Weekly list in the Master list? (Y/N)")
        if x.lower() == 'y':
            file1.write("  MasterList: Yes")
        else:
            file1.write("  MasterList: No")
        file1.write("  UseDaily: Yes")
    else:
        file1.write("  StartDate: ")
        file1.write("  EndDate: ")
        file1.write("  Path: ")
        file1.write("  MasterList: No")
        file1.write("  UseWeekly: No")
    file1.write("Daily: ")
    x = input("Do you want to enable Daily Trailers? (Y/N)")
    if x.lower() == 'y':
        print('Make sure plex can access the path you enter!')
        print("Enter the Start Date: \n")
        year = int(input('Enter a year'))
        month = int(input('Enter a month'))
        day = int(input('Enter a day'))
        date1 = datetime.date(year, month, day)
        file1.write("  StartDate: " + date1)
        print("Enter the End Date:")
        year = int(input('Enter a year'))
        month = int(input('Enter a month'))
        day = int(input('Enter a day'))
        date1 = datetime.date(year, month, day)
        file1.write("  EndDate: " + date1)
        x = input("Enter the trailer path(s):")
        file1.write("  Path: " + x)
        x = input("Do you want to use the Daily list in the Master list? (Y/N)")
        if x.lower() == 'y':
            file1.write("  MasterList: Yes")
        else:
            file1.write("  MasterList: No")
        file1.write("  UseDaily: Yes")
    else:
        file1.write("  StartDate: ")
        file1.write("  EndDate: ")
        file1.write("  Path: ")
        file1.write("  MasterList: No")
        file1.write("  UseDaily: No")
    file1.write("Misc: ")
    x = input("Do you want to enable Misc (Random with one static trailer) Trailers? (Y/N)")
    if x.lower() == 'y':
        print('Make sure plex can access the path you enter!')
        x = input("Enter the trailer path(s):")
        file1.write("  Path: " + x)
        x = input("Enter the static trailer path:")
        file1.write("  StaticTrailer: " + x)
        x = input("Enter the number of trailers to use ex: Path contains 5 trailers you set this value to 2 the "
                  "program will pick two at random as well as the static trailer to play in order:")
        file1.write("  TrailerListLength: " + x)
        file1.write("  UseMisc: Yes")
    else:
        file1.write("  Path: ")
        file1.write("  StaticTrailer: ")
        file1.write("  TrailerListLength: ")
        file1.write("  UseMisc: No")
    print('config file (config.yml) created')
    file1.close()

def getArguments():
    name = 'Automated-Plex-Preroll-Trailers'
    version = '1.1.0'
    parser = ArgumentParser(description='{}: Set monthly trailers for Plex'.format(name))
    parser.add_argument("-v", "--version", action='version', version='{} {}'.format(name, version), help="show the version number and exit")
    args = parser.parse_args()


def main():
    sort = ','
    x = datetime.today()
    res = "null"
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

    # Arguments
    arguments = getArguments()

    if doc["Plex"]["url"] is not None:
        session = requests.Session()
        session.verify = False
        requests.packages.urllib3.disable_warnings()
        plex = PlexServer(doc["Plex"]["url"], doc["Plex"]["token"], session, timeout=None)
        if str(doc["MasterList"]["UseMaster"]).lower() == 'true':
            plex.settings.get('cinemaTrailersPrerollID').set(MasterlistToStr)
        else:
            if str(doc["Monthly"]["UseMonthly"]).lower() == 'true':
                plex.settings.get('cinemaTrailersPrerollID').set(doc["Monthly"][x.strftime("%b")])
            if str(doc["Weekly"]["UseWeekly"]).lower() == 'true':
                if doc["Weekly"]["StartDate"] <= x <= doc["Weekly"]["EndDate"]:
                    plex.settings.get('cinemaTrailersPrerollID').set(doc["Weekly"]["Path"])
            if str(doc["Daily"]["UseDaily"]).lower() == 'true':
                if doc["Daily"]["StartDate"] <= x <= doc["Daily"]["EndDate"]:
                    plex.settings.get('cinemaTrailersPrerollID').set(doc["Daily"]["Path"])
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
                plex.settings.get('cinemaTrailersPrerollID').set(trailer)
        plex.settings.save()
        print('Pre-roll updated')

if __name__ == '__main__':
    main()
