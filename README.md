# Now-Spinning

A plugin for OBS that displays what record plays on the turntable.


# Details and Thoughts

This should be an all-in-one self-contained app with the following modules
 * A database for persisting the track meta information and locations of the artwork
 * A web server that is the link to OBS - serves a "Now Playing" web page that is picked up by the OBS' browser module 

# How will the "Now Playing" be updated?
* Expose an API, so I'd be able to do it from my phone
* Have functionality in the UI app
* To Be Considered - expose a web page

# OBS Settings
* Have Two scenes:
    * One for the camera
    * Another for the "Now Playing Layout"
* Now Playing Layout
    * Browser Module - should cover the bottom 15-20 % of the streamed screen
        * Width = 2400
        * Height = 250

# How it's supposed to look
![Screenshot](screenshots/example.png)

# Dev Notes
* The flask app is just one piece of the puzzle, I need some basic UI native app as well
  * That will allow for importing of directories with cover art images and track info (from JSON files for example)
  * Also, it makes more sense to the non-technical person
* Add a database that will keep the meta information for each track so it can be easily displayed

# TODO List
* Prepare Json file with track data
    * Include image location and track length(Stretch)
* Write tests for the existing views
* Add functionality to change the now-playing track that is served for the OBS browser
* 
