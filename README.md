# Plex-Automatic-Preroll
Automated script to change out plex preroll every month

## Requirements
-[Python 3.7+](https://www.python.org/)
(Probably works on a lower version haven't tested)

-[PlexAPI](https://github.com/pkkid/python-plexapi)



## Installation
First make sure you have Python installed version 3.7 and above. Next run:


```
pip install -r requirements.txt
```
That will install all the needed packages 

## Step by step instructions by Danny at smarthomepursuits.com

https://smarthomepursuits.com/configure-plex-automatic-prerolls-on-windows/

## Settings
The config.ini file is created through the script for ease of use. Optionaly you can just create it by hand by filling in the exampleconfig.ini file and then renaming it to config.ini. If you need to update it than you can edit the config.ini file.

Below is an example of the config file:

```
[DEFAULT]

plex_url = https://your ip or localhost here must be https:32400

plex_token =  

jan = /path/to/file.mp4

feb = 

mar = 

apr = 

may = 

june =

july =

aug = 

sept = 

oct = 

nov = 

dec = 
```


**If you want multiple random pre-roll videos to play in a specific month all you need to do is seperate the paths with a semi-colon**
Example when it ask you to add the December trailer path and you want to play two videos randomly for that month type:

```
/path/to/file1.mp4;/path/to/file2.mp4
```

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

Since you just downloaded the script the first time you run if you don't already have a config file you will be prompted to fill in some information to create the config file.

```
python /path/to/scripts/Plex_Trailers.py
```

I hope this is useful for some people and feel free to modify it for your own use!
