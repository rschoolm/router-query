import requests
import json

def get_mac_addresses(router_ip, username, password):
  # Build the API URL
  api_url = "http://{}/api/device.json".format(router_ip)

  # Set the HTTP headers
  headers = {
    "Content-Type": "application/x-www-form-urlencoded"
  }

  # Set the HTTP payload
  payload = {
    "method": "getDeviceList",
    "params": {}
  }

  # Send the HTTP request
  response = requests.post(api_url, headers=headers, auth=(username, password), data=json.dumps(payload))

  # Check the HTTP response status code
  if response.status_code != 200:
    raise ValueError("Failed to retrieve device list: {}".format(response.status_code))

  # Parse the HTTP response body
  response_data = response.json()

  # Extract the MAC addresses from the response
  mac_addresses = []
  for device in response_data["result"]["deviceList"]:
    mac_addresses.append(device["mac"])

  return mac_addresses

def setup(hass, config):
  # Get the router IP address and login credentials from the configuration
  router_ip = config["router_ip"]
  username = config["username"]
  password = config["password"]

  # Define a service to query the router for the MAC addresses of connected devices
  def query_router(call):
    # Get the MAC addresses from the router
    mac_addresses = get_mac_addresses(router_ip, username, password)

    # Set the service data
    call.data["mac_addresses"] = mac_addresses

  # Register the service with Home Assistant
  hass.services.register("router", "query", query_router)

