# client.py
import requests
import time
import json
import re

class WorkhubClient:
    def __init__(self, auth_base_url='https://api-admin.workhub.ai', api_base_url='https://api-teamgpt.workhub.ai'):
        self.auth_base_url = auth_base_url
        self.api_base_url = api_base_url
        self.token = None
        self.user_uuid = None
        self.company_uuid = None
    
    def login(self, email, password):
        """Authenticate the user and store the authentication token."""
        url = f'{self.auth_base_url}/api/auth'
        response = requests.post(url, json={'email': email, 'password': password})
        response.raise_for_status()  # This will raise an exception for HTTP error codes
        data = response.json()
        self.token = data.get('token')
        self.user_uuid = data.get('userUuid')
        return data

    def get_company_info(self):
        """Fetch company information for the logged-in user and set the company UUID."""
        if not self.user_uuid or not self.token:
            raise Exception('User must be logged in to fetch company information.')
        url = f'{self.auth_base_url}/api/users/{self.user_uuid}'
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Assuming the response structure includes a list of companyUuids
        # and we're interested in setting the first one as the active company_uuid
        company_uuids = data.get('companyUuids')
        if not company_uuids:
            raise ValueError("No company UUIDs found in the response.")
        self.company_uuid = company_uuids[0]  # Set the first company UUID as the active one
        
        return data


    def fetch_conversations(self):
        """Fetch all conversations for a specific company."""
        if not self.company_uuid or not self.token:
            raise Exception('User must be logged in and company UUID must be set to fetch conversations.')
        url = f'{self.api_base_url}/api/companies/{self.company_uuid}/conversations'
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def send_user_message(self, conversation_uuid, content, output_mode="MD", document_type='DEFAULT'):
        """Send a message to a specific conversation."""
        if not self.token:
            raise Exception('User must be logged in to send a message.')
        url = f'{self.api_base_url}/api/conversations/{conversation_uuid}/user_message'
        headers = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
        data = {
            'content': content,
            'output_mode': output_mode,
            'document_type': document_type,
        }
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    
    def create_conversation(self):
        """Create a new conversation for the company."""
        if not self.company_uuid or not self.token:
            raise Exception('User must be logged in and company UUID must be set to create a new conversation.')
        url = f'{self.api_base_url}/api/companies/{self.company_uuid}/conversations'
        headers = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
        # Explicitly sending an empty JSON object as the payload
        response = requests.post(url, json={}, headers=headers) 
        response.raise_for_status()  # This will throw an error for HTTP error responses
        return response.json()


    def poll_for_bot_message(client, conversation_uuid, bot_message_uuid, user_message_uuid):
        url = f'{client.api_base_url}/api/conversations/{conversation_uuid}/bot_message'
        headers = {'Authorization': f'Bearer {client.token}', 'Content-Type': 'application/json'}
        data = {
            'user_message_uuid': user_message_uuid,
            'bot_message_uuid': bot_message_uuid,
            'use_json_stream': True,
        }
        response = requests.post(url, json=data, headers=headers, stream=True)

        buffer = []  # Initialize buffer as an array of strings

        try:
            # Read the streamed content
            for chunk in response.iter_content(chunk_size=1, decode_unicode=True):
                if chunk:  # If chunk is not empty
                    buffer.append(chunk)  # Append chunk to buffer
                else:  # If chunk is empty, we've reached the end of the message
                    break  # Exit the loop as we've received all parts of the message

            # Join the buffer to form the complete message and split by newlines
            complete_message = ''.join(buffer).split('\n')

        except Exception as e:
            print(f"An error occurred while polling for bot message: {e}")
        
        complete_message_str = complete_message[-1]  # The large string with multiple JSON objects
        last_json_object = extract_last_json_object(complete_message_str)
        return last_json_object

def extract_last_json_object(complete_message_str):
    # Regex pattern to match JSON objects
    # This pattern assumes that your JSON does not contain strings with unescaped curly braces.
    # If your JSON objects can contain strings with curly braces, this approach may need refinement.
    json_objects = re.findall(r'\{.*?\}', complete_message_str, re.DOTALL)
    
    if json_objects:
        last_json_str = json_objects[-1]  # Get the last match
        try:
            last_json = json.loads(last_json_str)
            return last_json
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    else:
        print("No JSON objects found.")
        return None