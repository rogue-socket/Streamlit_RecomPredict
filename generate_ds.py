import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Define parameters
parameters = [
    "Engine Oil Pressure",
    "Engine Temperature",
    "Engine RPM",
    "Hard Braking",
    "Fuel Temperature",
    "Fuel Level",
    "Fuel Consumption",
    "Water in Fuel",
    "Fuel Pressure",
    "Environmental Temperature",
    "Environmental Humidity",
    "Transmission Pressure",
    "System Voltage",
    "Exhaust Gas Temperature",
    "Hydraulic Pump Rate",
    "Air Filter Pressure Drop",
    "Throttle Position"
]

# Number of machines
num_machines = 10

# Generate machine IDs
machine_ids = [f"BH-{str(i).zfill(4)}" for i in range(1, num_machines + 1)]

# Start time
start_time = datetime(2023, 1, 1)

# Time interval between records (in minutes)
time_interval = 5

# Total number of records per machine
records_per_machine = int(10000 / num_machines)

# Initialize list to store all data
data = []

for machine_id in machine_ids:
    current_time = start_time
    for _ in range(int(records_per_machine / len(parameters))):
        for param in parameters:
            # Generate realistic values based on parameter
            if param == "Engine Oil Pressure":
                value = round(np.random.normal(55, 5), 2)
            elif param == "Engine Temperature":
                value = round(np.random.normal(190, 10), 2)
            elif param == "Engine RPM":
                value = int(np.random.normal(1500, 100))
            elif param == "Hard Braking":
                value = random.choice([0, 1])
            elif param == "Fuel Temperature":
                value = round(np.random.normal(85, 5), 2)
            elif param == "Fuel Level":
                value = round(np.random.uniform(0, 100), 2)
            elif param == "Fuel Consumption":
                value = round(np.random.normal(3, 0.5), 2)
            elif param == "Water in Fuel":
                value = random.choice([0, 1])
            elif param == "Fuel Pressure":
                value = round(np.random.normal(45, 5), 2)
            elif param == "Environmental Temperature":
                value = round(np.random.normal(70, 15), 2)
            elif param == "Environmental Humidity":
                value = round(np.random.uniform(30, 90), 2)
            elif param == "Transmission Pressure":
                value = round(np.random.normal(230, 20), 2)
            elif param == "System Voltage":
                value = round(np.random.normal(14, 0.5), 2)
            elif param == "Exhaust Gas Temperature":
                value = round(np.random.normal(600, 50), 2)
            elif param == "Hydraulic Pump Rate":
                value = round(np.random.normal(120, 10), 2)
            elif param == "Air Filter Pressure Drop":
                value = round(np.random.normal(1, 0.2), 2)
            elif param == "Throttle Position":
                value = round(np.random.uniform(0, 100), 2)

            # Determine failure status
            failure = "Normal"
            if param == "Engine Temperature" and value > 220:
                failure = "High"
            elif param == "Engine Oil Pressure" and value < 30:
                failure = "Low"

            # Append data
            data.append({
                "Machine ID": machine_id,
                "Machine": "Backhoe_Loader",
                "Time": current_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "Parameter": param,
                "Value": value,
                "Failure Status": failure
            })

            # Increment time
            current_time += timedelta(minutes=time_interval)

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("telematics_dataset.csv", index=False)

print("Dataset generated and saved as 'telematics_dataset.csv'.")
