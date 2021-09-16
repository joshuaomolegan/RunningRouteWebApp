from pathFinder import PathFinder
from MapGen import MapGen
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = "sEcrEt.kEy" # Necessary for flash to work (ideally should be encrypted)
app.debug = True

@app.route("/")
@app.route("/home")
def index():
  return render_template("home.html")
  
@app.route("/", methods=["POST"])
def show_map():
  street = str(request.form["streetName"])
  city = str(request.form["cityName"])
  route_length = int(request.form["routeLength"])
  mapGen = MapGen(street, city, route_length)
  pathFinder = PathFinder(mapGen.G, mapGen.location, route_length)

  if route_length < 500: # Set minimum length to be 500m
    flash("Please enter a length greater than 500m") # Display an error message
  else:
    try:
      length, (path1, path2) = pathFinder.generate_circuit()
      folium_map = mapGen.plot_route(pathFinder.src, length, path1, path2) # Plot the route
      return render_template("map.html", folium_map=folium_map) # Display the map
    except Exception as error:
      flash("The following error occured: " + repr(error)) # Display an error message
    
  return render_template("home.html") # If an error occured, simply load the original page

  

if __name__ == "__main__":
  app.run()
