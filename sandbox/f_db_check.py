#!/usr/bin/python

import sqlite3
import os
import sys
import time
import datetime
from datetime import datetime, timedelta
from random import randrange

# === VAR definition ===
DEBUG = 0
db_path = '/Users/cedric_lemarchand/git/meetme-selfservice/sandbox/mod.db'
time_now = datetime.now()
time_outdated = time_now - timedelta(seconds=10)
room_range = range(100,105) # use db_init() after changing this value
random_pin = randrange(100000,999999) # to be improved with rstr

conn = sqlite3.connect(db_path)
c = conn.cursor()

time_minus_1h = time_now - timedelta(hours=1)
time_minus_2h = time_now - timedelta(hours=2)
time_minus_3h = time_now - timedelta(hours=3)
time_minus_4h = time_now - timedelta(hours=4)


# === FUNC definition ===
def db_drop():
    "Drop the db 'mod'"
    c.execute("DROP TABLE IF EXISTS mod")
    conn.commit
    return

def db_init():
    "Create/re-create the db 'mod' and table 'mod'"
    db_drop()
    c.execute("CREATE TABLE IF NOT EXISTS mod (room_number UNIQUE, pin, time_created DATE)" )

def db_init_test_datas():
    "Put some data for testing purpose"
    test_datas = [('100', '123456', time_minus_1h),
                    ('101', '123456', time_minus_2h),
                    ('102', '123456', time_minus_3h),
                    ('103', '123456', time_minus_4h),
                    ]
    c.executemany("INSERT INTO mod VALUES (?,?,?)", test_datas )
    conn.commit()
    return


def db_print_all():
    "Print all db content"
    print "### DEBUG PRINT ALL:"
    c.execute("SELECT * FROM mod")
    #print c.fetchall()
    for row in c:
        print row
    return

def db_clean():
    "Remove oudated entry, cf 'time_outdated' variable "
    #print "time_now = %s" % time_now
    #print "time_outdated = %s" % time_outdated
    #time_diff = time_now - time_outdated
    #print "NOW - OUTDATE %s" % time_diff
    c.execute("SELECT * FROM mod WHERE time_created < '%s' " % time_outdated )
    if DEBUG: print "### Deleted outdated row : %s" % c.fetchall()
    c.execute("DELETE FROM mod WHERE time_created < '%s' " % time_outdated )
    conn.commit()
    #print "### AFTER DEL"
    #db_print_all()

def db_find_free_room():
    for i in room_range:
        #print "### i = %s" % i
        try:
            new_room = (i, random_pin, time_now)
            c.execute("INSERT INTO mod VALUES (?,?,?)", new_room )
            print i, random_pin
            if DEBUG: print "### New room created with : ", new_room
            conn.commit()
            break
        except sqlite3.IntegrityError:
            if DEBUG : print "### IntegrityError, table %s exist" % i
    else:
        if DEBUG : print "### No more available room "

#db_init()
if DEBUG: db_print_all()

db_clean()
db_find_free_room()

conn.commit()
conn.close()
