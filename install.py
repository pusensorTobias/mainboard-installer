import subprocess
import configparser
import sys
import time
from swis import Swis

config = configparser.ConfigParser()
config.read('config.ini')

exe = config['MSPFlasher']['exe']
hex = config['MSPFlasher']['hex']

cmd = f'{exe} -n MSP432P401R -w "{hex}" -v -z [VCC]'

completedprocess = subprocess.run(cmd)

if completedprocess.returncode != 0:
    print("Flashing returned error.")
    sys.exit(completedprocess.returncode)

print()
serial = input("Serial number: ")
time.sleep(0.1)

print("Connecting to mainboard.")
with Swis() as swis:

    print("Connected to mainboard.")
    tryiterator = 10
    while tryiterator > 0:
        time.sleep(0.2)
        print("Flushing swis.")
        swis.flush()
        time.sleep(0.1)
        print("Setting serial number.")
        res = swis.transfer(f'VZ {serial}')
        time.sleep(0.01)
        res = swis.transfer('VI')
        time.sleep(0.01)
        print(f"Serial number set: '{res}'.")
        if res:
            res = res.value
            print(f'"{res}"')
            if res == serial:
                print("Set serial successfully!")
                tryiterator = -1
            else:
                tryiterator -= 1
                print("Mismatch of serials, trying again...")
        else:
            tryiterator -= 1
            print("Set failed, trying again...")
