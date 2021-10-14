---
page_type: sample
languages:
- javascript
- html
products:
- azure-iot-hub
name: IoTHub data visualization in web application
urlFragment: web-app-visualization
description: "This repo acts a self serve tool for anyone that wants to enable smart plant care on their plant."
---

# Smart Plant Care

This repo acts a self serve tool for anyone that wants to enable smart plant care on their plant. It shows the luminosity and humidity data and allows the user to send the command to water the plant to the PI.

## Browser compatiblity

| Browser | Verified version |
| --- | --- |
| Edge | 44 |
| Chrome | 76 |
| Firefox | 69 |

This tutorial shows how to deploy the app and IOT Hub to azure, the python script to PI and setup the circuitry for you pump and sensor. In this tutorial, you learn how to:

- Deploy the required infra to Azure
- Setup the sensor for PI
- Hook the pump to the PI
- Deploy the python script to PI
- View the data on the webpage
- Water your plant

## Pre-requisite
1. A raspberry Pi (3B or higher version) and micro-USB (for power)
2. A capacitive moisture sensor ()
3. LM393 Sensor module (optional)
4. MCP3008 Analog-to-Digital Convertor
5. A 5V DC water pump
6. 5V DC relay module
7. Breadboard and Connecting wires
8. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/) before you begin.

## Hardware setup

1. Setup the PI using the instructions [here](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-raspberry-pi-kit-node-get-started#set-up-raspberry-pi)

2. Both the above sensors give analog output and raspberry cannot convert it to digital. To convert the data to digital using MCP3008, we need to follow instructions [here](https://learn.adafruit.com/reading-a-analog-in-and-controlling-audio-volume-with-the-raspberry-pi?view=all)

2. Your pump will function through the relay. Follow the instructions [here](https://www.instructables.com/5V-Relay-Raspberry-Pi/) (replace motor with your 5V DC pump)

## Software Setup

1. Install the [Az CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)

2. Run the following command for infra deployment
```
deployment/deploy.sh --subscriptionId "<subscription id>" --rg-name "<new resource group name>" --location "<location>" --iotHubName "<Name to be used for the ITO Hub creation>" --webAppName "<DNS name of the web app>" --targetDevice "<Name of the PI device>"
```
3. Note the displayed connection string it will be required for integration with PI in Step 7

4. Navigate to the URL - https://<Web app name used in the above command>.azurewebsites.net/. It should be up an running, saying that the PI is offline.

5. SSH into your raspberry pi and run the following commands

```
sudo su root
pip3 install azure-iot-device
pip3 install azure-iot-hub
git clone https://github.com/StutiSri/smart-plant-care.git
```
6. Update .bashrc so that the python code is run on boot
```
vi .bashrc or nano .bashrc 
```

7. Add the lines to bashrc
```
export IOTHUB_DEVICE_SECURITY_TYPE="connectionString"
export IOTHUB_DEVICE_CONNECTION_STRING="<connection string that was exposed as output of infra deployment>"
#TODO: Add the python command to deploy the python script
```

8. Reboot the PI

9. Head to the app URL and you should start seeing Luminosity and Moisture data. 

10. To Water the Plant
    - Click on the Water the Plant button
    - Use the creds - admin and plantcare when asked for Authorization
    - The pump should water your plant for 5 seconds.

NOTE: If required, you can check the logs at - https://<Web app name>.scm.azurewebsites.net/api/logstream

## Local deployment for development

```
npm install
export IotHubConnectionString="<connection string for the device>"
export EventHubConsumerGroup="<consumer group name to be used for the message>"
export TargetDevice="IOT Hub device name"
npm start
```

Navigate to localhost:3000 for local testing.




