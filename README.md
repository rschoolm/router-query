# router-query
Home Assistant Add on to query AC2300 TP-Link Router for known MAC Addresses

In the Home Assistant configuration interface, go to the HACS page and click the "Custom Repositories" tab.

Add the URL of the GitHub repository for the custom addon to the "Custom Repositories" list.

Click the "Save" button to save the changes.

Go to the "Integrations" tab and click the "+" button to add a new integration.

Select the "Router Query" integration from the list of available integrations.

Follow the prompts to enter the IP address of the TP-Link AC2300 router and the login credentials that are required to access the router's web-based management interface.

Click the "Submit" button to save the integration and finish the setup process.

Once the custom addon is installed and configured in Home Assistant, you can use the router.query service to query the TP-Link AC2300 router for the MAC addresses of connected devices. For example, you might use the following code to call the service and print the list of MAC addresses:

service_data = {
}

hass.services.call("router", "query", service_data, True)

mac_addresses = service_data["mac_addresses"]

print(mac_addresses)
