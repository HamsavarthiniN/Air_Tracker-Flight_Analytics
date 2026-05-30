# SQL Queries
import pandas as pd
import mysql.connector 

connection = mysql.connector.connect(
    host = "Localhost",
    user = "root",
    password = "12345",
    )
cursor =  connection.cursor()
cursor
query = "use AeroDataBox"
cursor.execute(query)
## 1. Show the total number of flights for each aircraft model, listing the model and its count.
query1 = "SELECT ROW_NUMBER() OVER () AS no, model, COUNT(flight_number) AS Total_flights FROM aircraft JOIN flight ON aircraft_code=aircraft_registration  GROUP BY model"

df=pd.read_sql(query1, connection)
print(df.to_string(index=False))
#verified manually using SELECT model, aircraft_code, aircraft_registration, COUNT( aircraft_registration) as total_flight FROM flight JOIN aircraft on aircraft_code=aircraft_registration where model = 'A20N' group by model, aircraft_code, aircraft_registration;
## 2. List all aircraft (registration, model) that have been assigned to more than 5 flights
#since flight count is not more than 4, i used greater than or equal to 3
query2 = """SELECT aircraft_registration, model, COUNT(*) AS flight_count 
FROM aircraft JOIN flight ON aircraft_code = aircraft_registration 
GROUP BY aircraft_code, model HAVING COUNT(*) >=3"""
df=pd.read_sql(query2, connection)
df

## 3. For each airport, display its name and the number of outbound flights, but only for airports with more than 5 flights.
query3 = "SELECT icao_code, name, COUNT(flight_number) as number_of_outbound_flights from airport join flight on icao_code=origin_icao GROUP BY icao_code having count(flight_number)>5"
df=pd.read_sql(query3, connection)
df
## 4. Find the top 3 destination airports (name, city) by number of arriving flights, sorted by count descending.
query4 = """SELECT destination_icao, name, city, COUNT(flight_number) AS arriving_flights
FROM flight JOIN airport ON destination_icao = icao_code
GROUP BY icao_code ORDER BY arriving_flights DESC LIMIT 3"""
df=pd.read_sql(query4, connection)
df
## 5. Show for each flight: number, origin, destination, and a label 'Domestic' or 'International' using CASE WHEN on country match
query5 = """SELECT flight_number, origin_icao, destination_icao, 
CASE WHEN airport1.country = airport2.country THEN 'Domestic' ELSE 'International' END AS flight_type
FROM flight 
JOIN airport AS airport1 on origin_icao=airport1.icao_code 
JOIN airport AS airport2 on destination_icao = airport2.icao_code """
df=pd.read_sql(query5, connection)
df
## 6. Show the 5 most recent arrivals at “DEL” airport including flight number, aircraft, departure airport name, and arrival time, ordered by latest arrival.
query6 = """SELECT city, flight_number, aircraft_code AS aircraft, name AS departure_airport_name, DATE_FORMAT(STR_TO_DATE(actual_arrival, '%Y-%m-%d %H:%iZ'), '%Y-%m-%d') as arrival_date, DATE_FORMAT(STR_TO_DATE(actual_arrival, '%Y-%m-%d %H:%iZ'), '%H:%i') AS arrival_time 
FROM airport 
JOIN flight ON airport.icao_code = flight.destination_icao
JOIN aircraft ON aircraft.aircraft_code=flight.aircraft_registration 
WHERE iata_code = 'DEL'
ORDER BY arrival_time DESC
LIMIT 5"""
df=pd.read_sql(query6, connection)
df
## 7. Find all airports with no arriving flights (never used as a destination in flights table)
query7 = """SELECT icao_code, name, city
FROM airport
LEFT JOIN flight ON airport.icao_code = flight.destination_icao
WHERE flight.destination_icao IS NULL"""
df= pd.read_sql(query7, connection)
df
## 8. For each airline, count the number of flights by status (e.g., 'On Time', 'Delayed', 'Cancelled') using CASE WHEN.
query8 = """WITH base AS (SELECT aircraft.airline, airport_delays.dep_status, airport_delays.arr_status
FROM airport_delays JOIN flight ON airport_delays.flight_number = flight.flight_number
JOIN aircraft ON aircraft.aircraft_code = flight.aircraft_registration)
SELECT airline, SUM(CASE WHEN dep_status = 'delayed' THEN 1 ELSE 0 END) AS delayed_departure,
SUM(CASE WHEN dep_status = 'on_time' THEN 1 ELSE 0 END) AS on_time_departure,
SUM(CASE WHEN arr_status = 'delayed' THEN 1  ELSE 0  END) AS delayed_arrival,
SUM(CASE WHEN arr_status = 'on_time' THEN 1 ELSE 0 END) AS on_time_arrival
FROM base GROUP BY airline"""

df= pd.read_sql(query8, connection)
df
## 9. Show all canceled flights, with aircraft and both airports, ordered by departure time descending
query9 = """SELECT flight_number, origin_icao, destination_icao, scheduled_departure, status
FROM flight WHERE status = 'canceled' 
ORDER BY STR_TO_DATE(flight.scheduled_departure, '%Y-%m-%d %H:%iZ') DESC"""

pd.read_sql(query9, connection)
## 10. List all city pairs (origin-destination) that have more than 2 different aircraft models operating flights between them
query10 = """SELECT airport_departure.city AS origin_city, airport_arrival.city AS destination_city, 
COUNT(DISTINCT aircraft.model) AS aircraft_model_count 
FROM flight JOIN airport airport_departure ON flight.origin_icao = airport_departure.icao_code
JOIN airport airport_arrival ON flight.destination_icao = airport_arrival.icao_code
JOIN aircraft ON flight.aircraft_registration = aircraft.aircraft_code
GROUP BY airport_departure.city, airport_arrival.city 
HAVING COUNT(DISTINCT aircraft.model) >= 2"""
df=pd.read_sql(query10, connection)
df
## 11. For each destination airport, compute the % of delayed flights (status='Delayed') among all arrivals, sorted by highest percentage
query11 = """SELECT flight.destination_icao AS destination_airport, COUNT(*) AS total_arrivals, 
SUM(CASE WHEN airport_delays.arr_status = 'delayed' THEN 1 ELSE 0 END) AS delayed_arrivals,
ROUND(100.0 * SUM(CASE WHEN airport_delays.arr_status = 'delayed' THEN 1 ELSE 0 END) / COUNT(*), 2) AS delayed_percentage
FROM airport_delays JOIN flight ON airport_delays.flight_number = flight.flight_number
GROUP BY flight.destination_icao
ORDER BY delayed_percentage DESC"""
df=pd.read_sql(query11, connection)
df
