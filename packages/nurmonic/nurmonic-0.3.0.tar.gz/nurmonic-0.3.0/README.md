[![PyPI version](https://badge.fury.io/py/nurmonic.svg)](https://pypi.org/project/nurmonic/)

# Nurmonic

Nurmonic is a Python client library for interacting with the Nurmonic chat API, facilitating the integration of AI-powered chat functionalities into your Python applications. This library streamlines the process of sending messages and receiving chat completions from the Nurmonic API.

## Installation

Install Nurmonic using pip:

```sh
pip install nurmonic
```

# Usage

To use Nurmonic, you will need an API key from Nurmonic. Visit the Official Website to obtain your API key. Once you have it, you can begin making API requests to interact with Nurmonic’s AI.

```py
from nurmonic import Nurmonic

nurmo = Nurmonic(api_key="your_nurmonic_api_key")

def main():
    ai_response = nurmo.create_completion(
        messages=[{"role": "user", "content": "Say this is a test"}],
        model="gpt-3.5-turbo",
    )

    print(ai_response)

if __name__ == "__main__":
    main()
```

# Features

- Easy initialization and configuration with environment variables or direct options
- Much cheaper than the official API
- Fast responses for most requests, typically within 1ms
- A simplified method to create chat completions with the Nurmonic API

# Documentation

For more detailed information about the Nurmonic API and its capabilities, please visit the Nurmonic API Page on the official website.

# Pricing

Gain access to a high number of messages per minute for as low as $5 per month at the Premium Page.