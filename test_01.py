import serial
import argparse
import threading
import json

def read_serial():
    while True:
        data = ser.readline().decode('utf-8')
        if data:
            print(f"Received: {data}", end='')

def main():
    json_command = json.dumps({
        "T": 1051,
        "x": 373.8055574,
        "y": 287.1348881,
        "z": 112.6639825,
        "b": 0.655009796,
        "s": 0.813009818,
        "e": 0.859029241,
        "t": 3.136990711,
        "torB": 80,
        "torS": 200,
        "torE": -116,
        "torH": 0
    })

    global ser
    parser = argparse.ArgumentParser(description='Serial JSON Communication')
    parser.add_argument('port', type=str, help='Serial port name (e.g., COM1 or /dev/ttyUSB0)')

    args = parser.parse_args()

    ser = serial.Serial(args.port, baudrate=115200)
    ser.setRTS(False)
    ser.setDTR(False)

    serial_recv_thread = threading.Thread(target=read_serial)
    serial_recv_thread.daemon = True
    serial_recv_thread.start()

    try:
        while True:
            ser.write(json_command.encode() + b'\n')
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()

    # Quit program
    serial_recv_thread.join()
    ser.close()
    exit(0)


if __name__ == "__main__":
    main()