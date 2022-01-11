from bluedot.btcomm import BluetoothServer
from signal import pause

def data_received(data):
    print(data)
    s.send(data)

s = BluetoothServer(data_received)
pause()

#description of project which describes blinds used

#What constitutes a successful user interaction
#change 4 to focus on mechanical enclosure that successfully encloses and attaches to blinds
