from ast import literal_eval
import os

from db_connector import DBConnector

connector = DBConnector()
cursor = connector.get_db_cursor()
print("Successfully connect to DB")

path = "./drive_stat_out/"
items = ['carPlate', 'speedUp', 'slowDown', 'neutralSlide', 'neutralSlideTime', 'overspeed', 'overspeedTime', 'fatigue', 'hthrottleStop', 'oilLeak']

for item in items:
    print("Processing: %-40s" % (item))
    for filename in os.listdir(path + item):
        with open(path + item + "/" + filename) as file:
            for record in file.readlines():
                (k, v) = literal_eval(record)
                if len(k) == 0:
                    continue
                query = f"INSERT INTO {connector.SUMMARY_TABLE} (DriverID, {item}) VALUES (\"{k}\", \"{v}\") on DUPLICATE KEY UPDATE {item} = VALUES ({item});"
                cursor.execute(query)
                print("insert success:", k, v, "\r", end="")
                
print("writeStats Completed! %-30s" % (''))