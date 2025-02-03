import asyncio
from bleak import BleakScanner

async def discover_devices():
    scanner = BleakScanner()
    await scanner.start()
    await asyncio.sleep(5)  # Scan for 5 seconds
    devices = await scanner.get_discovered_devices()
    await scanner.stop()

    for device in devices:
        print(f"Device: {device.name}, Address: {device.address}")

if __name__ == "__main__":
    asyncio.run(discover_devices())