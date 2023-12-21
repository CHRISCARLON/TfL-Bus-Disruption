# TfL-Bus-Disruption
> [!NOTE] 
> Currently Version 1

--

**Methodology:**

Data Sources: 

- Street Manager permit data from March 2022 to April 2023
- TfL bus passenger data from March 2022 to April 2023
- TfL bus routes (Using TfL's open data API). 

Overview:

- Filter permit data to include only "completed works in London". 
- Assign permits a disruption score from 1-10 based on permit type (Minor, Standard, Major, Emergency, etc) - 
with Minor being the least disruptive and Major/Emergency being the most. 
- Assign Bus routes a usage score based on total passenger numbers for the year 22/23. 
- Place a 30m buffer around all bus routes.
- Overlay permits with bus routes. 
- Calculate the number of permits falling within the buffer zone of each bus route. 
- For each permit falling in the buffer zone of a bus route **multiply the bus route usage score by the permit
disruption score**.
- Add these results to a "bus route disruption score" total for each bus route. 
- Plot bus routes on a map. 
- Set a colour scale and colour bus routes based on bus route disruption score.

Limitations: 

- Around 10-15 bus routes (out of around 600+ ) did not have usage data - there was a slight mismatch between the bus
route data received from TfL's API and those used in the TfL usage data.  
- Bus route usage data was from the last financial year so doesn't 100% reflect today's picture. However, when the 23/24
data is released the analysis can be rerun. 

--

**Version 1 Features:**

- Static folium map 
- Layer control function: filter the map based on the bus route disruption scores (called Impact Levels on the map)
- OS Zoomstack base map

--

**Version 2 Upcoming Features:**

- Use a different TfL source for bus routes: this will hopefully result in all bus routes having a data and will remove
the black lines from the map. 
- Differentiate between regular buses and night buses: for example, add an OS Zoomstack dark layer for night buses. 
- Differentiate between numerous bus routes on the same road: create an option to easily 
cycle through them when clicked. 

--

**Version 3 Upcoming Features:**

- Stop treating bus routes as single blocks and calculate different levels of disruption at different sections of a bus
route - some sections may be more impacted than others and this is an important distinction to make.