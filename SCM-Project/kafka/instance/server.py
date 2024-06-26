import socket
import errno
import time
import json
import random
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
server_host = os.getenv("SERVER_HOST", "localhost")
server_port = int(os.getenv("SERVER_PORT", 8005))

# //creating a Instance from socket// # default argument [ socket.AF_INET, socket.SOCK_STREAM ]
Instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("New Instance Created")

# Bind the socket to the host and port
Instance.bind(("", server_port))

#clients purpose for communication
Instance.listen(2)
print(f"Server is listening on {server_host}:{server_port}")

# Establishing a connection & Accept incoming connections

client_socket , client_addr = Instance.accept()
print(f"Connection established with {client_addr}")

while True :
    try :
        # Generate route data
        route_data = { 
            "Device_Id" : random.randint(2365478910, 2365478912),
            "Battery_level" : round(random.uniform(1.75, 5.00), 3),
            "First_Sensor_Temperature" : round(random.uniform(10.00, 47.50), 2),
            "Route_From" : random.choice(['Sydney, Australia', 'Delhi, India', 'London, Uk', 'Canada, North America', 'Vizag, India', 'Los Angeles, CA']),
            "Route_To" : random.choice(['Houston, USA', 'Dubai, UAE', 'Abu Dhabi, UAE', 'Chile, South America', 'Delhi, India', 'New York City, NY']),
            "Time_Stamp" : str(datetime.now()) # type: ignore
        }
        
        
        # encode; sockets will transmits in bytes, not strings && py -> json f
        # Convert route data to JSON string and encode it(str -> bytes)
        Data = (json.dumps(route_data, indent = 1)).encode('utf-8')

        # Send data to the client
        client_socket.send(Data)

        # Generate new route data for every 8s
        time.sleep(8)

    except IOError as x:
        #to catch and ignore the broken pipe error
        if x.errno == errno.EPIPE: 
            pass

       

