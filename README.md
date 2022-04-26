# SI507-Final-Project

## Special Instructions for setup:
**Current code does not work 100% as expected. I could not figure out a great way to limit the printing of graph paths to only one or two edges so it will print all the connections for several minutes**
finalProjectUtils.py and finalProject.py must be in the same directory. Use provided cache.json file to speed up running of program.

## Dependencies:
- requests
- urllib
- pythonds
- time
- numpy

- There is no need to provide an API key, the one needed is coded into the project and, after one run, will create a cache.json file with the data needed for the program to function.

## Data Sources
I only used one data source for this. AEROAPI is an API provided by a company called flightaware that provides realtime flight tracking. 

- **Origin:** https://flightaware.com/aeroapi/portal/documentation#overview
*Note: This documentation is available once you sign up for a free account.*

- **Formats:** JSON, CSV
*I used this project to create data for another project which required I convert a CSV of airport latitude and longitude to json so that code is included here.*

- **How I accessed the data:** I created a utils file that contained all the functionality to pull the data from the API. From the main finalProject.py file, I get the resources and store them in a dictionary in the main file. From there, I build the graph with that data by connecting airports based on the flights between airports along with the average delay.

- **Summary of Data:**
There are thousands of records available per airport per day. The free tier of the API allows for 3 months of data so there are potentially hundreds of thousands of records. However, the API costs money so I’m limited to around 10,000 records total.
I’ve retrieved around 3,000 records so far, but about half of those records were test calls that I couldn’t end up using for different reasons. 
The most important pieces of data in each record are:
•	Departing Airport: This will be used as a prompt for the user)
•	Arrival Airport: This will also be used as a prompt for the user)
•	Departure Delay: Represented in seconds, this indicates how late an aircraft was departing
•	Arrival Delay: Represented in seconds, this indicates how late an aircraft is arriving

## Data Structure:
I created two classes, Flight and Airport, to store the primary information about the flights and airports. This was very similar to how I stored data for the Kevin Bacon project. Each Flight contains an origin and destination airport along with an average delay and each Airport contains a name with a list of flights into and out of that airport. 
From there, I loop over the flights from the API and create edges between each airport based on the average delay. I have to create edges in both directions so both airports are connected to each other. 

<img width="832" alt="image" src="https://user-images.githubusercontent.com/89586887/165114126-d694a517-4448-44f3-8258-01477e671be7.png">
<img width="916" alt="image" src="https://user-images.githubusercontent.com/89586887/165114222-a9ca4060-f406-4e6a-9dad-098c4661455c.png">


## Interacting with Project Code:
The code will prompt users for two airports (an origin and destination) that someone is trying to plan a trip between.

## Demo Link:
https://umich.zoom.us/rec/share/x4629Lz54ekcTwwKwaUTQuUtj0SOGJnFBO96usLZrx_miWOWMj_M7aA6EKKhZVL4.Q0Len8kKkhL1f1FS

