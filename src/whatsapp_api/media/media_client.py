import os
import requests
import mimetypes
from whatsapp_api.base_client import BaseClient


class MediaClient(BaseClient):
    def __init__(self, access_token, phone_number_id):
        """
        Media client for WhatsApp.

        :param access_token: Meta API access token
        :param phone_number_id: Phone number ID from WhatsApp
        """
        super().__init__(access_token)
        self.endpoint = f"{phone_number_id}/media"

    def _request_with_files(self, method, endpoint, payload, files):
        """
        Make an API request with file uploads.

        :param method: HTTP method (e.g., POST)
        :param endpoint: API endpoint (relative to base URL)
        :param payload: JSON payload
        :param files: Files to be uploaded
        :return: API response JSON
        :raises WhatsAppAPIException: If the API request fails
        """
        url = self.base_url + endpoint
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }

        # Send the request with the files and handle the response
        response = requests.request(method, url, data=payload, files=files, headers=headers)

        if response.status_code == 200:
            return response.json()

        raise Exception(f"Error: {response.status_code}, {response.text}")

    # Upload media file
    def upload_media(self, file_path):
        """
        Upload media to the Meta API.

        :param file_path: Path to the file to be uploaded.
        :return: Media ID from the API response.
        :raises FileNotFoundError: If the file does not exist.
        :raises ValueError: If the MIME type cannot be determined.
        """
        # Validate file existence
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File '{file_path}' does not exist.")

        # Determine the MIME type of the file
        mime_type = mimetypes.guess_type(file_path)[0]
        if not mime_type:
            raise ValueError(f"Could not determine the MIME type for file: {file_path}")

        # Prepare the files parameter for the request
        with open(file_path, 'rb') as file:
            files = {
                'file': (os.path.basename(file_path), file, mime_type, {'Expires': '0'}),
            }

            # Prepare the payload
            payload = {
                "messaging_product": "whatsapp",
                "type": mime_type,
            }

            response = self._request_with_files("POST", self.endpoint, payload, files)

        # Return the media ID from the response
        return response.get("id")
