# StaffBot

An attempt to save the scarebot® from sabotage! 

## What?

This just grabs the SCC staff names and images from the webpage and servers them on a webpage. This is split between an API and webserver simply to allow people to do other stuff with the API side of things if they so please 😊

## Using the API

Current Version: 1

So, currently there isn't much to this, but the API should be accessible from https://api.staffbot.net.scc.lancs.ac.uk/v{current version number} .

Right now, a random staff member's name and photo is served at the end ```get_member``` and this can take a var ```name``` to get a specific member.

The end ```rebuild``` forces a re-scrape of the people webpage, however, requires a key to passed in the ```key``` var.