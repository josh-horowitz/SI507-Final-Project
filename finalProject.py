from time import sleep
import finalProjectUtils as utils
from pythonds.basic import Queue
from pythonds.graphs import Graph, Vertex


# print('Creating Graph.......')
# g = Graph()

resources = {}

for airport in utils.BUSYAIRPORTS:
    resources[airport] = utils.getResource(utils.CACHE_NAME, f"{utils.BASEURL}/airports/{airport}/flights/arrivals", {'type': 'Airline', 'max_pages': 10})
    print(resources[airport])

# testFile = open('find_flights.json', 'r')

# testResults = json.load(testFile)

# print(len(testResults['flights']))

# testData = requests.get("https://aeroapi.flightaware.com/aeroapi/airports/KLAX/flights/departures",{'type': 'Airline'}, headers={'x-apikey': 'dtpjbMj9tNnjumdtl1p6EIQ2r67TgHFO'}).json()