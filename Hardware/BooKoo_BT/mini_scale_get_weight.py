import asyncio
from bleak import BleakClient

address = "C2036E8F-6893-C0CA-0F43-1DA3851BFCBF"  # Replace with your BLE device's address
weight_characteristic_uuid = "0000FF11-0000-1000-8000-00805f9b34fb"  # Replace with the actual characteristic UUID

def notification_handler(sender, data):
    # Assuming weight data parsing similar to previous example
    weight = ((data[7] * (2 ** 16)) + (data[8] * (2 ** 8)) + (data[9])) / 100.0
    print(f"Real-time Weight: {weight} grams, 7: {data[7]}, 8: {data[8]}, 9: {data[9]}")

async def connect_and_subscribe(address):
    async with BleakClient(address) as client:
        if await client.is_connected():
            print(f"Connected to {address}")
            await client.start_notify(weight_characteristic_uuid, notification_handler)
            print("Subscribed to weight updates. Listening for data...")
            # Keep the script running while listening for notifications.
            await asyncio.sleep(60)  # Adjust duration as needed
            await client.stop_notify(weight_characteristic_uuid)
        else:
            print("Failed to connect.")

asyncio.run(connect_and_subscribe(address))