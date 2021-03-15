from flask import Flask, render_template, request
#from flask_ngrok import run_with_ngrok #for use with google colab
from mapGen import plot_route

app = Flask(__name__)
#run_with_ngrok(app) #allows the web app to run in google colab
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
  
  folium_map = plot_route(street, city, route_length)
  
  return render_template("map.html", folium_map=folium_map)

if __name__ == "__main__":
  app.run()
