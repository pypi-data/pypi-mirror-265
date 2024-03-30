# Workhub API Client

The Workhub API Client is a versatile Python package designed for interacting with the Workhub API. It simplifies tasks such as user authentication, company information retrieval, conversation management, and message handling within the Workhub platform.

## Quick Start

To get started with the Workhub API Client, you'll need to initialize it with your API credentials:

```python
from client import WorkhubClient

client = WorkhubClient()
```

By default, the client is configured with the standard API endpoints. If your endpoints differ, you can specify them when initializing the client:

```python
client = WorkhubClient(auth_base_url='https://api-admin.workhub.ai', api_base_url='https://api-teamgpt.workhub.ai')
```

### Authenticating

Authenticate using your Workhub credentials to begin making API calls:

```python
client.login(email='your_email@example.com', password='your_password')
```

### Fetching Company Information

Retrieve your company's information and automatically set your active company UUID:

```python
company_info = client.get_company_info()
print(company_info)
```

### Managing Conversations

Fetch existing conversations, create new ones, or send messages:

- **Fetch Conversations**

  ```python
  conversations = client.fetch_conversations()
  print(conversations)
  ```

- **Create a New Conversation**

  ```python
  new_conversation = client.create_conversation(conversation_users=["user_uuid"], name="Team Meeting")
  print(new_conversation)
  ```

- **Send a Message**

  ```python
  message_response = client.send_user_message(conversation_uuid="conversation_uuid", content="Hello, team!")
  print(message_response)
  ```

### Polling for Bot Messages

You can poll for messages from a bot in a conversation, specifying a timeout as needed:

```python
bot_message = client.poll_for_bot_message(conversation_uuid="conversation_uuid", bot_message_uuid="bot_message_uuid", user_message_uuid="user_message_uuid", timeout=30)
print(bot_message)
```

## Error Handling

The client uses built-in exceptions for error handling. Make sure to handle these appropriately in your code to manage API call failures and other errors gracefully.

## Contributing

Contributions to the Workhub API Client are welcome. Please feel free to submit pull requests or issues to improve the project.

## License

This is released under MIT license.
