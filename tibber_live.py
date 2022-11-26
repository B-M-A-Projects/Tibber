from python_graphql_client import GraphqlClient
import asyncio
from influxdb import InfluxDBClient

def print_handle(data):
    print(data)
    print(data["data"]["liveMeasurement"]["timestamp"]+" "+str(data["data"]["liveMeasurement"]["power"]))
    print(data["data"]["liveMeasurement"]["timestamp"]+" "+str(data["data"]["liveMeasurement"]["lastMeterConsumption"]))
    print(data["data"]["liveMeasurement"]["timestamp"]+" "+str(data["data"]["liveMeasurement"]["accumulatedConsumptionLastHour"]))
    print(data["data"]["liveMeasurement"]["timestamp"]+" "+str(data["data"]["liveMeasurement"]["accumulatedCost"]))
    
    print(data["data"]["liveMeasurement"]["timestamp"]+" "+str(data["data"]["liveMeasurement"]["currentL1"]))
    print(data["data"]["liveMeasurement"]["timestamp"]+" "+str(data["data"]["liveMeasurement"]["currentL2"]))
    print(data["data"]["liveMeasurement"]["timestamp"]+" "+str(data["data"]["liveMeasurement"]["currentL3"]))
    print(data["data"]["liveMeasurement"]["timestamp"]+" "+str(data["data"]["liveMeasurement"]["signalStrength"]))    
    
    power = str(data["data"]["liveMeasurement"]["power"])
    print(power)
    currentL1 = str(data["data"]["liveMeasurement"]["currentL1"])
    currentL2 = str(data["data"]["liveMeasurement"]["currentL2"])
    currentL3 = str(data["data"]["liveMeasurement"]["currentL3"])
    
    accumulatedConsumption = str(data["data"]["liveMeasurement"]["accumulatedConsumption"])
    accumulatedCost = str(data["data"]["liveMeasurement"]["accumulatedCost"])
    
    tibber_data = [
        {
            "measurement" : "power",
            "tags" : {
                "location": "home"
            },
            "fields" : {
                "power": float(power),
                "currentL1": float(currentL1),
                "currentL2": float(currentL2),
                "currentL3": float(currentL3),
                "accumulatedConsumption": float(accumulatedConsumption),
                "accumulatedCost": float(accumulatedCost)
            }
        }
    ]
    print(tibber_data)
    influxclient.write_points(tibber_data)
    
influxclient = InfluxDBClient('localhost', 8086, 'tibbermonitor', '********************', 'tibber')

client = GraphqlClient(endpoint="wss://api.tibber.com/v1-beta/gql/subscriptions")
query = """
subscription {
  liveMeasurement(homeId:"******************************") {
    timestamp
    power
    lastMeterConsumption
    accumulatedConsumptionLastHour
    currentL1
    currentL2
    currentL3
    signalStrength
    accumulatedConsumption
    accumulatedCost
  }
}
"""
asyncio.run(client.subscribe(query=query, headers={'Authorization': "*********************************"}, handle=print_handle))