import serial

with serial.Serial('/dev/ttyS1', 9600, timeout=1) as ser:
    print("connected to: " + ser.portstr)
    while True:
        # this will store the line
        line = []

        for c in ser.read():
            line.append(c)
            if c == '\n':
                print("Line: " + ''.join(line))
                line = []
                break
