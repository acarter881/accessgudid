import requests
import json
import concurrent.futures
import pandas as pd
import time

class myMedicalDevices:
    def __init__(self, textPath) -> None:
        self.textPath = textPath
        self.records = []
        self.startTime = time.perf_counter()

    def getGTINs(self):
        with open(file=self.textPath, mode='r') as f:
            self.lines = [identifier.strip() for identifier in f.readlines()]

    def main(self, GTIN):
        # Create the full API URL
        self.URL = 'https://accessgudid.nlm.nih.gov/api/v2/devices/lookup.json?di=' + GTIN
        
        # Create the response object and check if the request is successful
        self.res = requests.get(self.URL)
        self.res.raise_for_status()
        
        # Deserialize the response object's text property (a string) to a variable named deviceData
        self.deviceData = json.loads(self.res.text)

        # Relevant data to gather
        self.companyName = self.deviceData['gudid']['device']['companyName']
        self.singleUse = self.deviceData['gudid']['device']['singleUse']
        self.rxUse = self.deviceData['gudid']['device']['rx']
        self.gmdnPTDefinition = self.deviceData['gudid']['device']['gmdnTerms']['gmdn'][0]['gmdnPTDefinition']

        # Append relevant data to list
        return self.records.append((self.companyName, GTIN, self.singleUse, self.rxUse, self.gmdnPTDefinition))

    def myThreads(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.main, self.lines)

    def toPandas(self):
        # Create pandas data frame    
        self.df = pd.DataFrame(data=self.records, columns=['Company Name', 'Device ID', 'Single Use', 'Prescription Use', 'Definition'])

        # Write relevant data to an Excel file
        self.df.to_excel(excel_writer=r'C:\Users\Alex\Desktop\hello\Python\testing.xlsx', sheet_name='Medical Devices', index=False, freeze_panes=(1,0))
    
    def endTime(self):
        self.endTime = time.perf_counter()
        print(f'It took {round(self.endTime - self.startTime, 2)} seconds to go through {len(self.lines)} items.')

# Instantiate the class and run the necessary functions
c = myMedicalDevices(textPath=r'C:\Users\Alex\Desktop\hello\Python\list.txt')
c.getGTINs()
c.myThreads()
c.toPandas()
c.endTime()
