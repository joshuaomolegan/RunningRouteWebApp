import heapq
import random
import networkx as nx
import osmnx as ox

class PathFinder:
    def __init__(self, graph, location, length):
        self.G = graph
        self.src = ox.distance.nearest_nodes(graph, location[0], location[1])
        self.len = length

    def generate_circuit(self):
        TOL = 100 # Stop when we find route within 100m of the desired route

        T = list(self.G.nodes)
        T.remove(self.src)

        bestCircuitWeight = 0
        bestCircuit = (None, None)

        graph = nx.Graph(self.G)
        self.__mark_bridges(graph)

        # Get a list of shortest paths to all nodes reachable from the source
        pathWeights, paths = nx.single_source_dijkstra(graph, self.src, weight='length')

        while T:
            t = random.choice(T)
            T.remove(t)

            # Convert path list to a dictionary
            path1 = self.__path_to_dict(paths[t])
            weight1 = pathWeights[t]            

            # Remove the edges in the direction of this path (but keep ones in reverse direction) and negate weight
            self.__reverse_path_weights(graph, path1)

            weight2, path2 = self.__modified_dijkstra(graph, t, path1)

            if not path2:
                # If we couldnt find a 2nd path, move on to the next iteration
                self.__reverse_path_weights(graph, path1)
                continue

            # Get weight and path for both the forward and reverse path of the circuit
            forwardWeight, forwardCircuit = self.__edge_disjoint_circuit(t, path1, path2, graph)
            reverseWeight, reverseCircuit = self.__edge_disjoint_circuit(t, path2, path1, graph)

            currentWeight = forwardWeight + reverseWeight
            
            if abs(currentWeight - self.len) < abs(bestCircuitWeight - self.len):
                bestCircuit = (forwardCircuit, reverseCircuit)
                bestCircuitWeight = currentWeight
            
            # Stop if we have a good enough circuit length
            if abs(bestCircuitWeight - self.len) < TOL:
                break

            self.__reverse_path_weights(graph, path1)

        # If while loop breaks we went through all nodes
        return bestCircuitWeight, bestCircuit

    # Helper function to update graph edge weights
    def __reverse_path_weights(self, graph, path):
        for u, v in path.items():
                # Don't negate weight if path is a bridge
                if v and not graph[u][v].get("isBridge", False):
                    graph[u][v]["length"] *= -1


    # Function to remove mark edges that contain bridges
    def __mark_bridges(self, graph):
        bridgeList = list(nx.bridges(graph))
        for u, v in bridgeList:
            graph[u][v].update({"isBridge": True})

    # Helper function to turn a path list into a dictionary
    def __path_to_dict(self, pathList):
        path = {pathList[-1]: None}
        i = len(pathList) - 1
        while i > 0:
            path[pathList[i-1]] = pathList[i]
            i -= 1
        
        return path

    # Modified dijkstras algorithm as described in R.Lewis paper
    def __modified_dijkstra(self, graph, target, path1):
        lenToNode = {n: float('inf') for n in graph.nodes}
        pred = {n: None for n in graph.nodes}

        lenToNode[self.src] = 0
        S = [(0, self.src, None)]

        while S:
            len_u, u, prev_u = heapq.heappop(S)
            if u == target:
                return (len_u, self.__generate_path(pred, u, graph))
            else:
                for v in graph.neighbors(u):
                    # Restrict traversing edges in path 1 in a direction away from source unless edge is a bridge
                    if path1.get(u, -1) == v and not graph[u][v].get("isBridge", False):
                        continue

                    # Don't allow traversal of edge just travelled
                    if v == prev_u:
                        continue
        
                    if len_u + graph[u][v]["length"] < lenToNode[v]:
                        lenToNode[v] = len_u + graph[u][v]["length"]
                        pred[v] = u
                        heapq.heappush(S, (lenToNode[v], v, u))
                
        return (None, None)

    # Function to generate a path from the target and the dictionary of predecessors
    def __generate_path(self, pred, target, graph):
        path = {}
        current = target

        while current != self.src:
            path[pred[current]] = current
            current = pred[current]
        
        return path

    # Function to create an edge disjoint circuit from the paths created by Dijkstra and Modified Dijstra
    def __edge_disjoint_circuit(self, t, path1, path2, graph):
        current = self.src
        currentDict, otherDict = path1, path2
        currentWeight = 0
        ans = []

        while True:

            u = current
            ans.append(u)
            
            if u == t:
                break
            else:
                v = currentDict[current]
                if otherDict.get(v, -1) == u: # Prevents error if v is not in dictionary
                    currentDict, otherDict = otherDict, currentDict

                current = currentDict[u]
                currentWeight += graph[u][current]["length"]
                
        return currentWeight, ans
