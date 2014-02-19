'''
    WritePagesDB.py
    Purpose: Reads entries from pages.db and outputs each entry as a line of 
    custom delimited values in a plain text file for processing in Hadoop

'''

import sqlite3

delimiter = 'AFUCKINGDELIMITER'

#Open output file for writing, open database file for reading
db = sqlite3.connect('pages.db')
cur = db.cursor()
f = open('output.txt', 'w')

#Run 300 times and index all the object in the database
for index in range(1, 301):
    entries = list()
    statement = "SELECT ID FROM PAGES WHERE ID="+str(index)
    cur.execute(statement)
    entries.append(cur.fetchall()[0])
    statement = "SELECT URL FROM PAGES WHERE ID="+str(index)
    cur.execute(statement)
    entries.append(cur.fetchall()[0])
    statement = "SELECT SUBDOMAIN FROM PAGES WHERE ID="+str(index)
    cur.execute(statement)
    entries.append(cur.fetchall()[0])
    statement = "SELECT BODY FROM PAGES WHERE ID="+str(index)
    cur.execute(statement)
    entries.append(cur.fetchall())
    statement = "SELECT HTML FROM PAGES WHERE ID="+str(index)
    cur.execute(statement)
    entries.append(cur.fetchall())

    #make all entries strings
    entries[0] = str(entries[0][0])
    entries[1] = entries[1][0]
    entries[2] = entries[2][0]

    #entry 3/4 are Text and URL, which need to have newline characters removed
    entries[3] = str(entries[3][0]).replace("\r\n", " ").replace("\n", " ").replace("\r", " ").replace("\\n", " ").replace('\\r\\n', " ").replace('\\r', " ")
    entries[4] = str(entries[4][0]).replace("\r\n", " ").replace("\n", " ").replace("\r", " ").replace("\\n", " ").replace('\\r\\n', " ").replace('\\r', " ")
    line = delimiter.join(entries) + '\n'

    #write into the file
    f.write(line)

#close all t3h things
f.close()
db.close()









