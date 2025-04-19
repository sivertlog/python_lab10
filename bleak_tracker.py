import asyncio
import shelve
from bleak import BleakScanner
import time

KNOWN_DEVICES = {
    "None": "1C:AF:4A:72:97:DD"  #tv
}

async def scan_for_devices():
    print("Scanning for Bluetooth devices...")
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"Device Name: {device.name}, Address: {device.address}")
    return devices

async def check_for_known_devices():
    devices = await BleakScanner.discover()
    nearby_known_devices = {}

    for device in devices:
        if device.address in KNOWN_DEVICES.values():
            device_name = [name for name, addr in KNOWN_DEVICES.items() if addr == device.address][0]
            print(f"{device_name} is nearby!")
            nearby_known_devices[device_name] = device.address

    return nearby_known_devices

def log_devices(devices):
    with shelve.open( "device_log" ) as db:
        for name, address in devices.items():
            key = name + '_' + address
            formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            if key in db:
                time_list = db[key]
                time_list.append(formatted_time)
                db[key] = time_list
            else:
                db[key] = [formatted_time]
    print( "Logged devices in the shelf database." )

async def scan():
    nearby_devices = await check_for_known_devices()
    if nearby_devices:
        log_devices( nearby_devices )
    else:
        print( "No known devices nearby." )

def main():
    # asyncio.run( scan_for_devices() )
    while True:
        print("Scanning...")
        asyncio.run( scan() )
        print("sleeping till next loop...")
        time.sleep(15)
        # This is the verifying portion
        print("Verifying log...")
        with shelve.open( "device_log" ) as db:
            for name, address in db.items():
                print( f"{name}: {address}" )

if __name__ == '__main__':
    main()