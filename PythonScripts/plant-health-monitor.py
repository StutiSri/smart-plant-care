# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os
import asyncio
import random
import logging
import json

from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device.aio import ProvisioningDeviceClient
from azure.iot.device import MethodResponse
from datetime import timedelta, datetime
import pnp_helper


############################SENSOR CODE######################
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

import RPi.GPIO as GPIO
import time
from six.moves import input
import threading
# from azure.iot.device import IoTHubDeviceClient
channel = 21
# create the spi bus

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

#create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P0)
chan1 = AnalogIn(mcp, MCP.P1)

##############################SENSOR CODE####################

logging.basicConfig(level=logging.ERROR)

model_id = "dtmi:com:example:PlantHealthMonitor;2"

plant_health_monitor_component_name = "plant-health-monitor"

# define behavior for receiving a message
def message_handler(message):
    print("####################################################################### ")
    print("#################### WATERING THE PLANT  ############################## ")
    print("####################################################################### ")
    try:
        # GPIO setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel, GPIO.OUT)
        time.sleep(5)
        
        GPIO.cleanup(channel)
    except KeyboardInterrupt:
        GPIO.cleanup(channel)

def remap_range(value, left_min, left_max, right_min, right_max):
    # this remaps a value from original (left) range to new (right) range
    # Figure out how 'wide' each range is
    left_span = left_max - left_min
    right_span = right_max - right_min

    # Convert the left range into a 0-1 range (int)
    valueScaled = int(value - left_min) / int(left_span)

    # Convert the 0-1 range into a value in the right range.
    return int(right_min + (valueScaled * right_span))

#####################################################
# TELEMETRY TASKS


async def send_telemetry_from_sensors(device_client, telemetry_msg, component_name=None):
    msg = pnp_helper.create_telemetry(telemetry_msg, component_name)
    await device_client.send_message(msg)
    print("<<<< Sending message" , msg , ">>>>>")
#    print(msg)
    await asyncio.sleep(2)


# An # END KEYBOARD INPUT LISTENER to quit application


def stdin_listener():
    """
    Listener for quitting the sample
    """
    while True:
        selection = input("Press Q to quit\n")
        if selection == "Q" or selection == "q":
            print("Quitting...")
            break


# END KEYBOARD INPUT LISTENER
#####################################################

async def main():
    switch = os.getenv("IOTHUB_DEVICE_SECURITY_TYPE")

    conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
    print("Connecting using Connection String " + conn_str)
    device_client = IoTHubDeviceClient.create_from_connection_string(
            conn_str, product_info=model_id
        )
    # Connect the client.
    await device_client.connect()

    # set the message handler on the client
    device_client.on_message_received = message_handler
    ################################################
    print("Listening for command requests and property updates")

    # Function to send telemetry every  seconds

    async def send_telemetry():
        print("Sending telemetry from various components")

        while True:
            luminosity_raw = chan0.value
            moisture_raw = chan1.value

            moisture = 100 - remap_range(moisture_raw, 15000, 65535, 0, 100) 
            luminosity = 100 - remap_range(luminosity_raw, 4000, 65535, 0, 100)

            sensor_data = {"luminosity": luminosity, "moisture": moisture}

            await send_telemetry_from_sensors(
                device_client, sensor_data, plant_health_monitor_component_name
            )


    send_telemetry_task = asyncio.ensure_future(send_telemetry())

    # Run the stdin listener in the event loop
    loop = asyncio.get_running_loop()
    user_finished = loop.run_in_executor(None, stdin_listener)
    # # Wait for user to indicate they are done listening for method calls
    await user_finished

    send_telemetry_task.cancel()

    # Finally, shut down the client
    await device_client.shutdown()


#####################################################
# EXECUTE MAIN

if __name__ == "__main__":
    asyncio.run(main())

