"""
e-road network.
"""

__author__ = "Yuan Jia"

from collections import defaultdict
import sys
import math
import re
import heapq


def twoPointsDistance(lat1, lon1, lat2, lon2):
  """
    cite from https://www.movable-type.co.uk/scripts/latlong.html
    """
  R = 6371
  φ1 = lat1 * (math.pi / 180)
  # φ, λ in radians
  φ2 = lat2 * (math.pi / 180)
  Δφ = (lat2 - lat1) * (math.pi / 180)
  Δλ = (lon2 - lon1) * (math.pi / 180)
  a = math.sin(Δφ / 2) * math.sin(Δφ / 2) + math.cos(φ1) * math.cos(φ2) * math.sin(
      Δλ / 2) * math.sin(Δλ / 2)
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

  d = R * c

  return d


def loadName(vertexName):

  vNfile = open(vertexName, "r")
  vNList = [""]
  vNStr = vNfile.read()
  vN = re.split("\t|\n", vNStr)

  for i in range(1, len(vN), 2):
    vNList.append(vN[i])

  vNfile.close()

  return vNList


def loadLocation(vertexLocation):

  vLList = [""]
  location = []
  vLfile = open(vertexLocation, "r")
  vLStr = vLfile.read()
  vL = vLStr.split()
  for i in range(1, len(vL), 3):
    location.append(float(vL[i]))
    location.append(float(vL[i + 1]))
    vLList.append(location)
    location = []
  vLfile.close()

  return vLList


def loadEdges(vNList, vLList, network):
  """
    load the network into a nested list
    """
  roadNet = []
  edge = []

  nFile = open(network, "r")
  nStr = nFile.read()
  nL = nStr.split()
  for i in range(0, len(nL), 2):
    edge.append(vNList[int(nL[i])])
    edge.append(vNList[int(nL[i + 1])])

    l1 = vLList[int(nL[i])]
    l2 = vLList[int(nL[i + 1])]
    d = twoPointsDistance(l1[0], l1[1], l2[0], l2[1])

    edge.append(d)
    roadNet.append(edge)

    edge = []

    edge.append(vNList[int(nL[i + 1])])
    edge.append(vNList[int(nL[i])])

    edge.append(d)

    roadNet.append(edge)
    edge = []
  nFile.close()

  return roadNet


def graph_Dijkstra(graph, start, end):

  if start == end:
    return [start]

  distance = {}
  previous = {}

  for vert in loadName("vertex_names.txt"):
    distance[vert] = math.inf
    previous[vert] = None

  distance[start] = 0
  pq = []
  heapq.heapify(pq)
  heapq.heappush(pq, (0, start))

  while len(pq) > 0:
    length, node = heapq.heappop(pq)
    for neighbor in list(graph[node].keys()):
      new_distance = length + graph[node][neighbor]
      if new_distance < distance[neighbor]:
        distance[neighbor] = new_distance
        previous[neighbor] = node
        heapq.heappush(pq, (new_distance, neighbor))

  path = []
  if previous[end] is None:
    return "No path from {} to {}!".format(start, end)
  path.append(end)
  preNode = previous[end]
  while preNode is not None:
    path.append(preNode)
    preNode = previous[preNode]

  return path[::-1]


if __name__ == "__main__":

  startPoint = sys.argv[1]
  EndPoint = sys.argv[2]

  g = defaultdict(dict)
  vNames = loadName("vertex_names.txt")
  vLocations = loadLocation("vertex_locations.txt")
  edges = loadEdges(vNames, vLocations, "network.txt")
  for [v_from, v_to, weight] in edges:
    g[v_from][v_to] = weight

  if startPoint not in vNames or EndPoint not in vNames:
    sys.stderr.write("invalid city\n")
    sys.exit(1)

  shortestPath = graph_Dijkstra(g, startPoint, EndPoint)

  if len(sys.argv) > 3:
    url = "https://www.google.com/maps/dir"
    for city in shortestPath:
      url = (url + "/" + str("{0:.3f}".format(vLocations[vNames.index(city)][0])) + "," +
             str("{0:.3f}".format(vLocations[vNames.index(city)][1])))
    sys.stdout.write(url + '\n')
  elif isinstance(shortestPath, str):
    sys.stderr.write(shortestPath + '\n')
    sys.exit(1)
  else:
    for vertex in shortestPath:
      sys.stdout.write(vertex + "\n")
