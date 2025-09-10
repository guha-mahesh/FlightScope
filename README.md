# FlightScope 

FlightScope utilizes data from Cornell's “eBird Basic Dataset (EBD) version 2025-09-10" to create 35 different Poisson Distribution Models to predict the probability of seeing a specific bird species given your location.
The Poisson Distribution Models were trained based off of: 
- Location (Latitude and Longitude)
- The Date
- The Temperature
- Precipitation
- Sun Insolation
- Wind Speed
- Clearness Index
- Relative Humidity
- Pressure

The models turned out to be quite weak due to the lack of *Absence* Data, so I do not highly recommend using this model in day to day application. I plan on improving it in the future with aggregated *Absence Data*, to have a control for when the specific bird species *aren't* present. 
Until then, enjoy messing around with the model by:

1. Open your terminal in a directory of your choice and type
   `git clone git@github.com:guha-mahesh/FlightScope.git`
   `cd FlightScope`
2. Run the Servers:
   `cd backend `
   `python app.py`
   `cd ../frontend`
   `npm run dev`
3. [Start Scrolling](http://localhost:5173/)


## Thank You
