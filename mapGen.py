import osmnx as ox
import networkx as nx
from math import inf
import folium, random, webbrowser

def edge_disjoint_shortest_pair(graph, source, length):
  V = list(graph.nodes) # List of nodes / vertexes

  V.remove(source)
  bestCircuitWeight = 0 # Stores the total weight of the best circuit

  pathWeight, path = nx.single_source_dijkstra(graph, source, weight='length') # Get a list of shortest paths to all nodes reachable from the source
  path1 = []
  path2 = []

  while len(V) != 0:
    G = graph.copy() # Copy original graph
    t = random.choice(V) # Choose a random node from T
    V.remove(t) # Remove the element we chose this iteration

    tmpPath1 = path[t]  # Get the shortest path between source and target

    # Reverse the shortest path direction and negate the weight of each edge in it
    for i in range(len(tmpPath1) - 1):
      u = tmpPath1[i]
      v = tmpPath1[i+1] # Each edge in the path is in the form (u, v)
      G.remove_edge(u, v)
      G[v][u][0]["length"] = -G[v][u][0]["length"]

    try:
      weight2, tmpPath2 = nx.single_source_bellman_ford(G, source, t) # Use bellman ford to find the 2nd path as ot can handle negative edge weights
    except nx.exception.NetworkXNoPath:
      continue # If no path was found move on to the next iteration

    # Update the best weight seen so far
    currentCircuitWeight = pathWeight[t] + weight2 # Since we negated the weights of any edges traversed a 2nd time in the 2nd path, we can just add their weights
    if currentCircuitWeight <= length and currentCircuitWeight > bestCircuitWeight:
      bestCircuitWeight = currentCircuitWeight
      # Update our variables storing the best paths seen so far
      print(bestCircuitWeight)
      path1 = tmpPath1
      path2 = tmpPath2
      target = t
    
    # If we find a path that is exactly equal to the length we're looking for, stop searching
    if bestCircuitWeight == length:
      break
  
  # Turn the list of paths into a dictionary where each entry is {predecessor: child} 
  st_path = _path_to_dict(path1)
  st_path2 = _path_to_dict(path2)
  
  return (bestCircuitWeight, make_circuit(source, target, st_path, st_path2))

# Helper function to turn a path list into a dictionary
def _path_to_dict(pathList):
  path = {pathList[-1]: None}
  i = len(pathList) - 1
  while i != 0:
    path[pathList[i-1]] = pathList[i]
    i -= 1
  
  return path
  
# Function to make a circuit from 2 edge disjoint paths
def make_circuit(source, target, path1, path2):

  # For each node in the 1st shortest path, if we find an edge traversed in both paths (in different directions), take the edge leaving this node in the other path and continue taking edges from this other path
  current = source
  forwardPath = {}
  takeFrom1 = True # Flag to determine which path we take edges from
  while current != None:
    if takeFrom1:
      if path1[current] in path2.keys() and path2[path1[current]] == current:
        forwardPath[current] = path2[current]
        takeFrom1 = False
        current = path2[current]
      else: 
        forwardPath[current] = path1[current]
        current = path1[current]
    else:
      if path2[current] in path1.keys() and path1[path2[current]] == current:
        forwardPath[current] = path1[current]
        takeFrom1 = True
        current = path1[current]
      else: 
        forwardPath[current] = path2[current]
        current = path2[current]

  # For each node in the 1st shortest path, if we find an edge traversed in both paths (in different directions), take the edge leaving this node in the other path and continue taking edges from this other path
  current = source
  reversePath = {}
  takeFrom1 = False    
  while current != None:
    if not takeFrom1: 
      if path2[current] in path1.keys() and path1[path2[current]] == current:
        reversePath[current] = path1[current]
        takeFrom1 = True
        current = path1[current]
      else: 
        reversePath[current] = path2[current]
        current = path2[current]
    else:
      if path1[current] in path2.keys() and path2[path1[current]] == current:
        reversePath[current] = path2[current]
        takeFrom1 = False
        current = path2[current]
      else: 
        reversePath[current] = path1[current]
        current = path1[current]
  
  # Turn both paths into lists
  forwardPathList = [0]*len(forwardPath) 
  reversePathList = [0]*len(reversePath)

  current = source
  for i in range(len(forwardPath)):
    forwardPathList[i] = current
    current = forwardPath[current]

  current = source
  for i in range(len(reversePath)):
    reversePathList[i] = current
    current = reversePath[current]

  return (forwardPathList, reversePathList)

def plot_route(street, city, route_length):
  location = ox.geocoder.geocode(street + " " + city) # Get (lat, long)
  G = ox.graph_from_point(location, route_length//2, network_type="walk") # Graph around given location
  closest_to_start = ox.get_nearest_node(G, location, "euclidean") # Find node closest to start

  length, (path1, path2) = edge_disjoint_shortest_pair(G, closest_to_start, route_length) # Get the length and paths of the generated cycle

  # Plot the path on a folium map
  folium_map = folium.Map(location, width="100%", height="100%")
  tmp_route_map = ox.folium.plot_route_folium(G, path1, folium_map)
  route_map = ox.folium.plot_route_folium(G, path2, tmp_route_map, color="#cc0000") # Make the colour of the 2nd path red
  folium.Marker(location=location).add_to(route_map)
  return route_map._repr_html_()







