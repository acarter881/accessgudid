#! python3
import json
import requests
import pandas as pd

# Reads each line of a text file as a medical device identifier
med_devices = open('list.txt', 'r')
lines = med_devices.readlines()

# Start reading from the first line of the text file
devicePos = 0

# Create an empty list that stores all of the medical device data 
records = []

for i in range(len(lines)):
    # Base URL for the medical device lookup in JSON format
    URL = 'https://accessgudid.nlm.nih.gov/api/v2/devices/lookup.json?di='

    # Variable for the medical device identifier
    deviceNum = lines[devicePos].strip()

    # Append the device identifier to the base URL to form the completed URL
    URL += deviceNum

    # Increment devicePos, so the script goes to the next medical device identifier on its next iteration
    devicePos += 1
    
    # Create the response object and check if the request is successful
    res = requests.get(URL)
    res.raise_for_status()

    # Print information about the search to the terminal
    print(f'Searching for device number: {deviceNum}...')

    # Deserialize the response object's text property (a string) to a variable named deviceData
    deviceData = json.loads(res.text)

    # Relevant data to gather
    companyName = deviceData['gudid']['device']['companyName']
    deviceID = deviceData['gudid']['device']['identifiers']['identifier'][0]['deviceId']
    rxUse = deviceData['gudid']['device']['rx']
    singleUse = deviceData['gudid']['device']['singleUse']
    gmdnPTDefinition = deviceData['gudid']['device']['gmdnTerms']['gmdn'][0]['gmdnPTDefinition']

    # Append relevant data to list
    records.append((companyName, deviceID, rxUse, singleUse, gmdnPTDefinition))

# Create pandas data frame    
df = pd.DataFrame(records, columns=['Company Name', 'Device ID', 'Prescription Use', 'Single Use', 'Definition'])

# Write relevant data to an Excel file
df.to_excel('testing.xlsx', sheet_name = 'Medical Devices', index=False, freeze_panes=(1,0))

# Close the text file
med_devices.close()
