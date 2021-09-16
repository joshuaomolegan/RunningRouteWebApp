import folium
import osmnx as ox

import math

class MapGen:
    def __init__(self, street, city, routeLength):
        self.routeLength = routeLength

        # Get latitude and longitude of the given location
        self.location = ox.geocoder.geocode(street + " " + city)

        # Create the map around the start point
        self.map = folium.Map(self.location, width="100%", height="100%")
        
        # Create di-graph of streets a given radius from start
        self.G = ox.graph_from_point(self.location, self.routeLength//2, network_type='walk')


    def plot_route(self, srcNode, actualRouteLength, forwardPath, returnPath):
        # Plot forward and reverse paths in different colours
        tmpRouteMap = ox.folium.plot_route_folium(self.G, forwardPath, self.map)
        routeMap = ox.folium.plot_route_folium(self.G, returnPath, tmpRouteMap, color="#cc0000")

        #Add marker to start point and show route length as a pop up
        folium.Marker(location=self.location, popup=folium.Popup(f"<b>Route length: {math.floor(actualRouteLength)}m</b>", show=True)).add_to(routeMap)
        
        return routeMap._repr_html_()