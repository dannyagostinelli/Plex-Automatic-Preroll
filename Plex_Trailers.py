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

import requests
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

print('###########################')
print('#                         #')
print('#  Plex Monthly Preroll!  #')
print('#                         #')
print('###########################' + '\n')

print('Pre-roll updating...')
file = pathlib.Path("config.ini")
if file.exists():
    file1 = open("config.ini","r")
else:
    print('No config file found! Lets set one up!')
    file1 = open("config.ini","w+")
    file1.write("[SERVER]" + "\n")
    x = input("Enter your (https) plex url:")
    file1.write("plex_url = " + x + "\n")
    x = input("Enter your plex token: (not sure what that is go here: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)")
    file1.write("plex_token = " + x + "\n\n")
    file1.write("[MONTHS]" + "\n")
    print('Make sure plex can access the path you enter!')
    x = input("Enter the January trailer path:")
    file1.write("Jan = " + x + "\n")
    x = input("Enter the February trailer path:")
    file1.write("Feb = " + x + "\n")
    x = input("Enter the March trailer path:")
    file1.write("Mar = " + x + "\n")
    x = input("Enter the April trailer path:")
    file1.write("Apr = " + x + "\n")
    x = input("Enter the May trailer path:")
    file1.write("May = " + x + "\n")
    x = input("Enter the June trailer path:")
    file1.write("June = " + x + "\n")
    x = input("Enter the July trailer path:")
    file1.write("July = " + x + "\n")
    x = input("Enter the August trailer path:")
    file1.write("Aug = " + x + "\n")
    x = input("Enter the September trailer path:")
    file1.write("Sept = " + x + "\n")
    x = input("Enter the October trailer path:")
    file1.write("Oct = " + x + "\n")
    x = input("Enter the November trailer path:")
    file1.write("Nov = " + x + "\n")
    x = input("Enter the December trailer path:")
    file1.write("Dec = " + x + "\n\n")
    file1.write("[PATHS]" + "\n")
    x = input("Enter the Host directory path: (Path where your PreRoll folders are located)")
    file1.write("host_dir = " + x + "\n")
    x = input("OPTIONAL: Enter the Docker directory path: (Path where your PreRoll folders are located when using docker. (Path that Plex uses))")
    file1.write("docker_dir = " + x + "\n")
    print('config file (config.ini) created')
    file1.close()
    file1 = open("config.ini","r")

def getArguments():
    name = 'Monthly-Plex-Preroll-Trailers'
    version = '1.0.1'
    parser = ArgumentParser(description='{}: Set monthly trailers for Plex'.format(name))
    parser.add_argument("-v", "--version", action='version', version='{} {}'.format(name, version), help="show the version number and exit")
    args = parser.parse_args()

def getConfig():
    config = ConfigParser()
    config.read(os.path.split(os.path.abspath(__file__))[0]+'/config.ini')
    configdict = {}

    if 'SERVER' in config:
        if 'plex_url' in config['SERVER']:
            configdict['plex_url'] = config.get('SERVER', 'plex_url')
        else:
            print('Plex URL not found. Please update your config.')
            raise SystemExit
        if 'plex_token' in config['SERVER']:
            configdict['plex_token'] = config.get('SERVER', 'plex_token')
        else:
            print('Plex token not found. Please update your config.')
            raise SystemExit     
    else:
        print('Invalid config. SERVER not found. Please update your config.')
        raise SystemExit


    if 'PATHS' in config:
        if 'host_dir' in config['PATHS']:
            host_dir = os.path.join(config.get('PATHS', 'host_dir'),'')
            if 'docker_dir' in config['PATHS'] and config.get('PATHS', 'docker_dir'):
                docker_dir = os.path.join(config.get('PATHS', 'docker_dir'),'')
            else:
                docker_dir = host_dir
        else:
            print('host_dir not found in config. Please update your config.')
            raise SystemExit
    else:
        print('Invalid config. PATHS not found. Please update your config.')
        raise SystemExit
    
    for month in config['MONTHS']:
        path = config['MONTHS'][month].replace(docker_dir,host_dir)
        path = generatePreRoll(path).replace(host_dir,docker_dir)
        configdict[month] = path
    return configdict
    

#Automatically generate preroll based on a list of files in a folder
def generatePreRoll(PreRollPath):
    types = ['.mp4', '.avi', '.mkv']
    PreRollFiles = ''
    if any(type in PreRollPath for type in types):
        return PreRollPath
    else:
        PreRollPath = os.path.join(PreRollPath,'')
        for type in types:
            for file in os.listdir(PreRollPath):
                if file.endswith(type):
                    PreRollFiles+=os.path.join(PreRollPath, file)+';'
        return PreRollFiles

def main():
    # Arguments
    arguments = getArguments()
    # Settings
    config = getConfig()
    if config['plex_url'] is not None: 
        session = requests.Session()
        session.verify = False
        requests.packages.urllib3.disable_warnings()
        url = str(config['plex_url'])
        token = str(config['plex_token'])
        plex = PlexServer(url, token, session, timeout=None)
        currentMonth = datetime.today().strftime('%b').lower()
        if currentMonth in config:
            plex.settings.get('cinemaTrailersPrerollID').set(config[currentMonth])
            plex.settings.save()
            print(f'Pre-roll updated to {config[currentMonth]}')
        else:
            print(f'{currentMonth} not found in config. Please update your config. Pre-Roll not updated.')

if __name__ == '__main__':
    main()
    #getConfig()
