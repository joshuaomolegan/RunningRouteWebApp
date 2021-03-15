# Flask-Running-App
A simple web app made using flask and bootstrap that, when given a length and a location, will generate a circuit of that length nearby. This can be used to plan a running route. To use the web app please run:
> python app.py

## Libraries:
flask  
osmnx  
networkx  
math  
folium  
random  

## Files:
**app.py** - Contains the code to initialise the web app and display the map once created  
**mapGen.py** - Contains functions to generate and plot the route on a map of the area around the given location  
**/templates** - Contains the html files used for the web app

## Improvements:
* Error Handling
* Add loading screen while paths are being generates
* Stop if a path is found within a given tolerance of the desired length (e.g. 50m)
* Remove brides and implement heuristics as suggested in R.Lewis' paper

## References:
A Heuristic Algorithm for Finding Attractive Fixed-Length Circuits in Street Maps - R. Lewis  
Survivable Networks - R. Bhandari
