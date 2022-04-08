import json
import requests
from urllib.parse import urljoin, urlencode
from pythonds.basic import Queue
from pythonds.graphs import Graph, Vertex
from time import sleep

AEROAPIKEY = 'dtpjbMj9tNnjumdtl1p6EIQ2r67TgHFO'
AEROAPI = requests.Session()
AEROAPI.headers.update({"x-apikey": AEROAPIKEY})
BASEURL = 'https://aeroapi.flightaware.com/aeroapi'
BUSYAIRPORTS = ['KDFW', 'KDEN', 'KORD', 'KLAX', 'KCLT', 'KLAS', 'KPHX', 'KMCO', 'KSEA', 'KATL']
CACHE_NAME = 'cache.json'

def readJSON(filepath, encoding='utf-8'):
    """
    Reads a JSON document, decodes the file content, and returns a list or
    dictionary if provided with a valid filepath.
    Parameters:
        filepath (string): path to file
        encoding (string): optional name of encoding used to decode the file. The default is 'utf-8'.
    Returns:
        dict/list: dict or list representations of the decoded JSON document
    """

    with open(filepath, 'r', encoding=encoding) as file_obj:
        return json.load(file_obj)

def writeJSON(filepath, data):
    """
    This function dumps the JSON object in the dictionary `data` into a file on
    `filepath`.
    Parameters:
        filepath (string): The location and filename of the file to store the JSON
        data (dict): The dictionary that contains the JSON representation of the objects.
    Returns:
        None
    """

    with open(filepath, 'w', encoding='utf-8') as file_obj:
        json.dump(data, file_obj, ensure_ascii=False, indent=2)

def createCacheKey(url, params=None):
    """ Returns a unique cache key value based on the url and params. If the params value is left as None, just returns the url in lowercase.
    If the params parameter contains values, this function starts off with a querystring variable containing just a '?' and uses urlencode to
    replace any spaces in the params value with a '+'. Then, the function returns the return value of urljoin between the url and updated querystring.

    Parameters:
        url (str): url that specifies resource.
        params (dict): an optional dictionary of querystring arguments. Default value is None.

    Returns:
        key (str): unique and referencable querystring
    """
    if params:
        querystring = f"?{urlencode(params)}"
        key = urljoin(url, querystring).lower()
    else:
        key = url.lower()
    return key

def getCache(filepath):
    """ Tries to read the cache file, if it contains anything. If it doesn't contain any information, it returns an empty dictionary.

    Parameters:
        filepath (str): file path to cache file.

    Returns:
        dict/list: dict or list representation of the decoded cache file object.
    """
    try:
        return readJSON(filepath)
    except:
        return {}

def getResource(filepath, url, params=None):
    """
    Gets the cache and uses create_cache_key function to generate the unique referencable value for the desired value.
    If the key already exists in the cache, retrieves the value from the cache and returns it. If not, makes a call to 
    SWAPI and stores the value from the API with the unique key in the cache file and writes to the cache file.

    Parameters:
        filepath (str): filepath to cache file
        url (str): url that specifies the resource
        params (dict): an optional dictionary of querystring arguments. Default value is none.

    Returns:
        dict: dictionary representation of the decoded JSON.
    """
    cache = getCache(filepath)
    key = createCacheKey(url, params)

    if key in cache.keys():
        return cache[key]
    else:
        resources = getFlights(url, params)
        sleep(600)
        cache[key] = resources # add to cache
        writeJSON(filepath, cache) # overwrite cache

        return resources

def getFlights(url, params=None):

    flights = AEROAPI.get(url, params=params).json()

    #clean flights


    return flights

# def buildGraph(flightData, flightDict):

#     g = Graph()
#     # loop over the movie data
#     for flight in flightData:

#         # for each actor, if the actor already exists, add it to the actor list and add the movie to the actor movie list,
#         # else, create a new actor and put it in the actor list in the outer loop
#         for actor in movieData[1:]:
#             actorName = cleanActorName(actor).lower()
#             #movieDict[movieData[0]].append(actorName)
#             if actorDict.get(actorName):
#                 newMovie.addActor(actorDict[actorName])
#             else:
#                 newActor = Actor(actorName, [])
#                 newActor.addMovie(newMovie)
#                 newMovie.addActor(newActor)
#                 actorDict[actorName] = newActor

#     #for each movie in the dictionary, create an edge between all the actors
#     for movie in movieDict.keys():
#         for actor1 in movieDict[movie].actors:
#             for actor2 in movieDict[movie].actors:
#                 if actor1 != actor2:
#                     g.addEdge(actor1.name, actor2.name, cost=movie)

#     return g



def bfs(g, start):
    start.setDistance(0)
    start.setPred(None)
    vertQueue = Queue()
    vertQueue.enqueue(start)
    traversedVerts = []
    while (vertQueue.size() > 0):
        currentVert = vertQueue.dequeue()
        traversedVerts.append(currentVert)
        for nbr in currentVert.getConnections():
            if (nbr.getColor() == 'white'):
                nbr.setColor('gray')
                nbr.setDistance(currentVert.getDistance() + 1)
                nbr.setPred(currentVert)
                vertQueue.enqueue(nbr)
        currentVert.setColor('black')
    return traversedVerts


# def traverse(y):
#     x = y
#     while(x.getPred()):
#         print(f"{x.getId().title()} is in {x.connectedTo[g.getVertex(x.getPred().getId())]} with {x.getPred().getId().title()}")
#         x = x.getPred()


# def findConnections(g, startingActor, endingActor):

#     v1 = g.getVertex(endingActor)
#     v2 = g.getVertex(startingActor)

#     if v1 != None and v2 != None:
#         traversedVerts = bfs(g, v1)

#         traverse(v2)
#     else:
#         print("One or both of those actors are not in the graph. Please try again.")

#     return traversedVerts

# def resetVertices(traversedVerts):

#     for vert in traversedVerts:
#         vert.setColor('white')

