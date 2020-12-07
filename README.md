# Plex-Automatic-Preroll
## Dev branch
This branch should be stable but you have been warned!

This new branch contains an almost fully rewritten code base. This now allows for Pre-rolls by Month, Week, Day, Misc, and Master list. The config is now based on yaml instead of a ini file for easier reading and data config data storage.

## Requirements
-[Python 3.7+](https://www.python.org/)
(Probably works on a lower version haven't tested)

-[PlexAPI](https://github.com/pkkid/python-plexapi)


## Installation
Nothing! well obviously python and maybe the plex api if you don't already have it but the script should prompt you to install that if it is missing.

## Settings
The config.yml file is created through the script for ease of use. If you need to update it than you can edit the config.yml file.

**If you want multiple random pre-roll videos to play in a specific month, week, or day all you need to do is seperate the paths with a semi-colon for the master list you need to specify random or not if allowing the script to make it automaticlly**
Example when it ask you to add the December trailer path and you want to play two videos randomly for that month type:

```
/path/to/file1.mp4;/path/to/file2.mp4
```
**Example config will be provided**

## Usage

### Setting Plex Preroll

You need to schedule a job for updating the preroll each day, week, or month depending how you want your pre-rolls updated.

**macOS or Linux:**
Ex: Monthly

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
