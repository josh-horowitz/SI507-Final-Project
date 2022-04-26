from numpy import average
from finalProjectUtils import Airport, Flight
import finalProjectUtils as utils
from pythonds.basic import Queue
from pythonds.graphs import Graph, Vertex


# print('Creating Graph.......')
# g = Graph()

resources = {}
flightsData = {}
airportData = {}


for airport in utils.BUSYAIRPORTS:
    resources[airport] = utils.getResource(utils.CACHE_NAME, f"{utils.BASEURL}/airports/{airport}/flights/arrivals", {'type': 'Airline', 'max_pages': 10})


# for each item in resources, create the necessary airport objects if they don't exist and create a flight object between the two airports if they don't exist

def buildGraph(data):

    g = Graph()

    for flights in data.values():
        for flight in flights['arrivals']:

            #get airport codes
            if airportData.get(flight['origin']['code']):
                origin = airportData.get(flight['origin']['code'])
            else:
                origin = Airport(flight['origin']['code'], [])
                airportData[origin.name] = origin

            if airportData.get(flight['destination']['code']):
                destination = airportData.get(flight['destination']['code'])
            else:
                destination = Airport(flight['destination']['code'], [])
                airportData[destination.name] = destination

            #get flight name
            flightName = f"{origin.name}_to_{destination.name}"

            flightInfo = flightsData.get(flightName)

            #if the flight does not exist, create a new one and put it in the flight dictionary. If it does, put the flight into the airport dictionary
            if not flightInfo:
                flightInfo = Flight(origin, destination, flight['operator'], flight['departure_delay'])
                flightsData[flightName] = flightInfo
                airportData[flightInfo.origin.name].addFlight(flightInfo)
                airportData[flightInfo.destination.name].addFlight(flightInfo)
            else:
                flightInfo.delay = average([flightInfo.delay, flight['departure_delay']])


    #Loop over each airport and connect each airport with a given flight. You don't need to check if the flights against each other
    #like in the Kevin Bacon graph assignment because flights between two airports are unique
    for flight in flightsData.values():
        #cost should be some unique identifier for a given flight
        #currently, key for connected_to is vertex object and value is description. May need to reverse?
        g.addEdge(flight.origin.name, flight.destination.name, cost=flight)
        g.addEdge(flight.destination.name, flight.origin.name, cost=flight)

    return g


def checkAirportForFlight(airport, flight):
    """Check to see if a flight exists in a given airport and add it if it doesn't"""

    if flight not in airportData[airport.name].flights:
        airportData[airport.name].addFlight(flight)


flightGraph = buildGraph(resources)
#traversedVerts = utils.bfs(flightGraph, flightGraph.getVertex('KLAX'))

outputData = {}
for vertex in flightGraph.vertices.values():
    outputData[vertex.id] = []
    for item in vertex.connectedTo:
        outputData[vertex.id].append((item.id, vertex.connectedTo[item].delay))

utils.writeJSON('output.json', outputData)

# for airport in airportData:
#     for flight in airportData[airport].flights:
#         print(f"{airport}: {flight}")


while(True):

    origin = ('k' + input("What airport would you like to start at?: ")).upper()
    destination = ('k' + input("What airport are you flying to?: ")).upper()

    if origin in airportData.keys() and destination in airportData.keys():
        print("Here are the route options and their average delays")
        utils.printAllPaths(flightGraph, flightGraph.getVertex(origin), flightGraph.getVertex(destination))

        goAgain = input("Would you like to search another trip (Y/N)?: ")
        if goAgain.lower() == 'n':
            print("Thank you for trying the route finder")
            break
    else:
        print("We do not have data on one of those airports. Please try again.")