import argparse
import requests
from dmacheck import opsgenie_utils
import opsgenie_sdk
import time

# Gecko Terminal API endpoint
GECKO_API_URL = (
    "https://api.geckoterminal.com/api/v2/simple/networks/{network}/token_price/{token}"
)


def fetch_token_price(network, token):
    url = GECKO_API_URL.format(network=network, token=token)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("price")
    else:
        # Handle API error
        print("Failed to fetch token price:", response.text)
        return None


def send_alert(opsgenie_api_key, threshold, price, network, token):
    # Example condition to send alert if price is below the threshold
    if price < threshold:
        # Create Opsgenie alert payload
        alert_payload = opsgenie_utils.create_alert_payload(
            "token_price_alert", ["monitor_id_1", "monitor_id_2"]
        )

        try:
            # Create an Opsgenie API client
            config = opsgenie_sdk.configuration.Configuration()
            config.api_key["Authorization"] = opsgenie_api_key
            client = opsgenie_sdk.AlertApi(opsgenie_sdk.ApiClient(config))

            # Create an alert using Opsgenie SDK
            response = client.create_alert(alert_payload)
            print("Alert created successfully:", response)
        except opsgenie_sdk.ApiException as e:
            print("Failed to create alert:", e)
            # Handle exception if needed

        # If needed, use network and token here
        print("Network:", network)
        print("Token:", token)


def main(opsgenie_api_key, network, token, threshold):
    while True:
        # Fetch token price
        price = fetch_token_price(network, token)
        if price is not None:
            print("Token price:", price)
            # Call send_alert function to send alert if necessary
            send_alert(opsgenie_api_key, threshold, price, network, token)
        else:
            print("Token price is not available")

        # Sleep for 5 minutes
        time.sleep(300)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch token price and send alert to Opsgenie"
    )
    parser.add_argument("--opsgenie-api-key", required=True, help="Opsgenie API key")
    parser.add_argument("--network", required=True, help="Network")
    parser.add_argument("--token", required=True, help="Token address")
    parser.add_argument(
        "--threshold", type=float, required=True, help="Threshold for price alert"
    )
    args = parser.parse_args()

    main(args.opsgenie_api_key, args.network, args.token, args.threshold)
