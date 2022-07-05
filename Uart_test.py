import serial

with serial.Serial('/dev/ttyS0', 9600, timeout=5) as ser:
    print("connected to: " + ser.portstr)
    while True:
        # this will store the line
        line = []

        print(ser.readline().decode("utf-8"))

