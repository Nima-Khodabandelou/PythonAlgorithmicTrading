import datetime as dt


dtm = dt.datetime

localTime = dtm.now()
localTimeUTC = dtm.now().timestamp()
print("localTimeUTC: ", int(localTimeUTC))
print("localTime: ", localTime)
IFCMTimeUTC = localTimeUTC - 1.5*3600
print("IFCMTimeUTC: ", IFCMTimeUTC)
IFCMTime = localTime.fromtimestamp(IFCMTimeUTC)
print("IFCMTime: ", IFCMTime)
weekDays = {0: 'mon', 1: 'tue', 2: 'wed', 3: 'thu', 4: 'fri', 5: 'sat', 6: 'sun'}
print("IFCMWeekDay", weekDays[IFCMTime.weekday()])
