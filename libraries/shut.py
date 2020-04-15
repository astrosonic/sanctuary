import time, sqlite3
from libraries.conf import baseloca

def execqury(qurytext):
    location = baseloca["roomlist"]["loca"]
    database = sqlite3.connect(location)
    acticurs = database.cursor()
    acticurs.execute(qurytext)
    database.commit()
    database.close()

def bildrcrd(username, roomlink):
    qurytext = "update roomlist set IsItPurged = '" + str(True) + "', " + \
                                   "PurgerName = '" + str(username) + "', " + \
                                   "TimeOfPurging = '" + str(time.time()) + "' " + \
                                   "where RoomIdentity = '" + str(roomlink) + "'"
    execqury(qurytext)

def generate(shutdict):
    username = shutdict["username"]
    roomlink = shutdict["roomlink"]
    bildrcrd(username, roomlink)