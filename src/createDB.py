import sqlite3
import datetime

con = sqlite3.connect('DB/dummy.db')

cur = con.cursor()

airport_id   = "DM"
runway_id    = "DM-1A" 
new_table    = airport_id+"_"+runway_id+" "+str(datetime.datetime.now().date())

# Create table
cur.execute("CREATE TABLE '%s'(timestamp text, airport text, runway text, lightid integer, v1 real, v2 real, v3 real, v4 real, v5 real, distance real, s integer)" %new_table)

# Insert a row of data
cur.execute("INSERT INTO '%s' VALUES ('2021-03-26 0:00:00','DM','DM-1A',1,51.8,42.9,53.4,50.3,60.2,2.0,1)"%new_table)

# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()