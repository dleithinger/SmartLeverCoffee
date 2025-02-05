import matplotlib.pyplot as plt 
import asyncio
from bleak import BleakClient

address = "C2036E8F-6893-C0CA-0F43-1DA3851BFCBF"  # Replace with your BLE device's address
weight_characteristic_uuid = "0000FF11-0000-1000-8000-00805f9b34fb"  # Replace with the actual characteristic UUID

data_points = []
timestamp = 0

# Create an empty plot 
fig, ax = plt.subplots() 
line, = ax.plot([], [], color= '#884b8f') 
  
# Set the x-axis and y-axis limits to 100 
ax.set_xlim(0, 500) 
ax.set_ylim(0, 500) 

# Show the plot 
plt.show(block=False) 


def notification_handler(sender, data):
    global timestamp
    print("timestamp: ", timestamp)
    # Assuming weight data parsing similar to previous example
    weight = ((data[7] * (2 ** 16)) + (data[8] * (2 ** 8)) + (data[9])) / 100.0
    timestamp += 1
    print("timestamp: ", timestamp)
    data_points.append((timestamp, weight))
    print(f"Real-time Weight: {weight} grams")

    # Update the plot with the new data points 
    x_values = [x for x, y in data_points] 
    y_values = [y for x, y in data_points]
    line.set_data(x_values, y_values) 
    ax.set_xlim(x_values[0], x_values[-1])
    ax.set_ylim(0, max(y_values)) 
    # pause the plot for 0.01s before next point is shown 
    plt.pause(0.01) 

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