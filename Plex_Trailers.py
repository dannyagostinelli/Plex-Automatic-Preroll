#!/usr/bin/python
try:
    from plexapi.server import PlexServer

except:
    print('\033[91mERROR:\033[0m PlexAPI is not installed.')
    try:
        from plexapi.server import PlexServer
    except:
        x = input("Plexapi is not installed do you want to install it? y/n:")
        if x == 'y':
            subprocess.check_call([sys.executable, "-m", "pip", "install", 'PlexAPI==4.2.0'])
        elif x == 'n':
            sys.exit()
    finally:
        if x == 'y':
            from plexapi.server import PlexServer
        elif x == 'n':
            sys.exit()
import requests
import subprocess
from urllib.parse import quote_plus, urlencode
from datetime import datetime

from plexapi import media, utils, settings, library
from plexapi.base import Playable, PlexPartialObject
from plexapi.exceptions import BadRequest, NotFound

from argparse import ArgumentParser
import os
import random
import sys
import pathlib
from configparser import *

print('#########################')
print('#                       #')
print('# Plex Monthly Preroll! #')
print('#                       #')
print('#########################' + '\n')

print('Pre-roll updating...')
file = pathlib.Path("config.ini")
if file.exists():
    file1 = open("config.ini","r")
else:
    print('No config file found! Lets set one up!')
    file1 = open("config.ini","w+")
    file1.write("[DEFAULT]" + "\n")
    x = input("Enter your (https) plex url:")
    file1.write("plex_url = " + x + "\n")
    x = input("Enter your plex token: (not sure what that is go here: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)")
    file1.write("plex_token = " + x + "\n")
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
    file1.write("Dec = " + x + "\n")
    print('config file (config.ini) created')
    file1.close()
    file1 = open("config.ini","r")

def getArguments():
    name = 'Monthly-Plex-Preroll-Trailers'
    version = '1.0.0'
    parser = ArgumentParser(description='{}: Set monthly trailers for Plex'.format(name))
    parser.add_argument("-v", "--version", action='version', version='{} {}'.format(name, version), help="show the version number and exit")
    args = parser.parse_args()

def getConfig():
    config = ConfigParser()
    config.read(os.path.split(os.path.abspath(__file__))[0]+'/config.ini')
    return {
        'plex_url': config.get('DEFAULT', 'plex_url'),
        'plex_token': config.get('DEFAULT', 'plex_token'),
        'Jan': config.get('DEFAULT', 'Jan'),
        'Feb': config.get('DEFAULT', 'Feb'),
        'Mar': config.get('DEFAULT', 'Mar'),
        'Apr': config.get('DEFAULT', 'Apr'),
        'May': config.get('DEFAULT', 'May'),
        'June': config.get('DEFAULT', 'June'),
        'July': config.get('DEFAULT', 'July'),
        'Aug': config.get('DEFAULT', 'Aug'),
        'Sep': config.get('DEFAULT', 'Sept'),
        'Oct': config.get('DEFAULT', 'Oct'),
        'Nov': config.get('DEFAULT', 'Nov'),
        'Dec': config.get('DEFAULT', 'Dec')
    }

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
        currentMonth = int(datetime.today().month)
        if currentMonth == 1:
            plex.settings.get('cinemaTrailersPrerollID').set(config['Jan'])
        elif currentMonth == 2:
            plex.settings.get('cinemaTrailersPrerollID').set(config['Feb'])
        if currentMonth == 3:
            plex.settings.get('cinemaTrailersPrerollID').set(config['Mar'])
        elif currentMonth == 4:
            plex.settings.get('cinemaTrailersPrerollID').set(config['Apr'])
        if currentMonth == 5:
            plex.settings.get('cinemaTrailersPrerollID').set(config['May'])
        elif currentMonth == 6:
            plex.settings.get('cinemaTrailersPrerollID').set(config['June'])
        if currentMonth == 7:
            plex.settings.get('cinemaTrailersPrerollID').set(config['July'])
        elif currentMonth == 8:
            plex.settings.get('cinemaTrailersPrerollID').set(config['Aug'])
        if currentMonth == 9:
            plex.settings.get('cinemaTrailersPrerollID').set(config['Sep'])
        elif currentMonth == 10:
            plex.settings.get('cinemaTrailersPrerollID').set(config['Oct'])
        if currentMonth == 11:
            plex.settings.get('cinemaTrailersPrerollID').set(config['Nov'])
        elif currentMonth == 12:
            plex.settings.get('cinemaTrailersPrerollID').set(config['Dec'])
        plex.settings.save()
        print('Pre-roll updated')

if __name__ == '__main__':
    main()