# Gecko Opsgenie Alert

## Usage

This application fetches token prices from the Gecko Terminal API and sends alerts to Opsgenie when the price falls below a certain threshold.

### Installation

1. Install the package using pip:

    ```
    pip install -r requirements.txt
    ```

2. Run the application with the following command:

    ```
    main.py --opsgenie-api-key YOUR_API_KEY --network NETWORK --token TOKEN --threshold THRESHOLD
    ```

Replace `YOUR_API_KEY`, `NETWORK`, `TOKEN`, and `THRESHOLD` with appropriate values.

### Glossary

- `opsgenie-api-key`: The API key provided by Opsgenie. This key is required to authenticate and send alerts to the Opsgenie service.
- `network`: The network for which you want to fetch token prices. For example, "ton" for the TON network.
- `token`: The token address for which you want to fetch the price.
- `threshold`: The price threshold below which an alert should be sent to Opsgenie.

### Usage as a Module

If you wish to use this application as a module, you can import the necessary functions into your Python script:

```python
from geckocheck.main import fetch_token_price, send_alert

# Fetch token price
price = fetch_token_price(network, token)

# Send alert if necessary
send_alert(opsgenie_api_key, threshold, price, network, token)
