
# Workhub API Client

The Workhub API Client is a Python package designed to simplify interactions with the Workhub API. It supports user authentication, company information retrieval, conversation management, message handling, and direct integration with GPT-4 for processing messages.

## Features

- User authentication
- Fetch company information
- Manage conversations
- Send messages with optional GPT-4 processing
- Stream bot responses directly after sending a message

## Installation

To install the Workhub API Client, use pip:

```
pip install workhub-client
```

## Quick Start

### Initialize the Client

First, create an instance of the WorkhubClient:

```python
from workhub_client import WorkhubClient

client = WorkhubClient()
```

### Authenticate

Log in using your Workhub credentials:

```python
client.login('your_email@example.com', 'your_password')
```

### Fetch Company Information

Retrieve and automatically set your active company UUID:

```python
company_info = client.get_company_info()
print(company_info)
```

### Send a Message

Send a message to a specific conversation. You can specify GPT-4 processing by setting `document_type='GPT4'`.

```python
conversation_uuid = 'your_conversation_uuid_here'
response = client.send_user_message(
    conversation_uuid,
    "What's the weather like today?",
    document_type='GPT4'
)
print(response)
```

### Stream Bot Responses

Send a user message and directly stream the bot's response:

```python
client.stream_bot_message(
    conversation_uuid="your_conversation_uuid",
    content="when was uark founded?",
    document_type="GPT4"
)
```

This method sends a message and immediately starts listening for and printing the streamed response from the bot.

# Workhub API Client Example

This section provides a simple Python program example that uses the Workhub API Client to authenticate, fetch company information, send a message with GPT-4 processing, and stream the bot's response.

## Example Program

```python
from workhub_client import WorkhubClient

def main():
    # Initialize the Workhub API client
    client = WorkhubClient()

    # Login with your Workhub credentials
    print("Logging in...")
    client.login('your_email@example.com', 'your_password')

    # Fetch and display company information
    print("Fetching company information...")
    company_info = client.get_company_info()
    print(f"Company Info: {company_info}")

    # Specify the UUID of the conversation you want to interact with
    conversation_uuid = 'your_conversation_uuid_here'

    # Send a message using GPT-4 processing and display the response
    print("Sending a message with GPT-4 processing...")
    message_response = client.send_user_message(
        conversation_uuid,
        "What's the weather like today?",
        document_type='GPT4'
    )
    print(f"Message Response: {message_response}")

    # Stream bot's response directly after sending a message
    print("Streaming bot's response...")
    client.stream_bot_message(
        conversation_uuid=conversation_uuid,
        content="when was uark founded?",
        document_type="GPT4"
    )

if __name__ == "__main__":
    main()
```

## Running the Example

1. Replace `'your_email@example.com'`, `'your_password'`, and `'your_conversation_uuid_here'` with your actual Workhub credentials and the UUID of the conversation you want to send a message to.
2. Save the program to a file, for example, `workhub_example.py`.
3. Run the program using Python:

```sh
python workhub_example.py
```

This example demonstrates the core functionalities of the Workhub API Client, making it easy for users to understand how to use the package in their applications. Remember, when sharing or using your credentials and sensitive information, always ensure they are secured and not hardcoded in production scripts.


## Contributing

Contributions to the Workhub API Client are welcome. Please feel free to submit pull requests or report issues to improve the project.

## License

This project is released under the MIT License.
