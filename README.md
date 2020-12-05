# Plex-Monthly-Preroll
Automated script to change out plex preroll every month

## Requirements
-[Python 3.7+](https://www.python.org/)
(Probably works on a lower version haven't tested)

-[PlexAPI](https://github.com/pkkid/python-plexapi)


## Installation
Nothing! well maybe the plex api if you don't already have it but the script should prompt you for that.

## Settings
The config.ini file is created through the script for ease of use. If you need to update it than you can edit the config.ini file I might add a in scrpt editor later.

## Usage

### Setting Plex Preroll

You need to schedule a job for updating the preroll each month.

**macOS or Linux:**

```
crontab -e
0 0 * 1-12 * python /path/to/scripts/Plex_Trailers.py 2>&1
```

**Windows:**

Verify python is added to the PATH environmental variable
Search for task schedular and open it. Click "Create Basic Task" and enter a name and description. Then set the task to run monthly. Choose "Start a program" then for "Program/script" add the full path of the Plex_Trailers.py script Click "Finish" and you are done!


## Running For The First Time

Since you just downloaded the script the first time you run it you will be prompted to fill in some information to create the config file.

```
python /path/to/scripts/Plex_Trailers.py
```

I hope this is useful for some people and feel free to modify it for your own use!
