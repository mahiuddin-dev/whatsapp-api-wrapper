from whatsapp_api.base_client import BaseClient


class Profile(BaseClient):
    def __init__(self, access_token, phone_number_id, version="v24.0"):
        """
        Initialize the Profile class.

        Args:
            access_token (str): The access token for authentication.
            phone_number_id (str): The phone number ID associated with the WhatsApp account.
        """
        super().__init__(access_token, version)
        self.endpoint = f"{phone_number_id}/whatsapp_business_profile"

    def get_profile(self):
        parms = {
            "fields": "about,address,email,description,profile_picture_url,websites"
        }
        return self._request("GET", self.endpoint, payload=parms)

    def update_profile(self, about=None, address=None, description=None, email=None, websites=None):
        """
        Update the WhatsApp Business Profile.

        Note: profile_picture_url cannot be updated here; use update_profile_picture instead.
        """
        payload = {"messaging_product": "whatsapp"}
        fields = {
            "about": about,
            "address": address,
            "description": description,
            "email": email,
            "websites": websites,
        }
        payload.update({key: value for key, value in fields.items() if value is not None})
        return self._request("POST", self.endpoint, payload=payload)

    def update_profile_picture(self, uploaded_media_file_id):
        """
        Update the WhatsApp Business Profile picture.

        :param uploaded_media_file_id: ID of a previously uploaded media file to use as the profile picture.
        """
        payload = {
            "messaging_product": "whatsapp",
            "profile_picture_handle": uploaded_media_file_id,
        }
        return self._request("POST", self.endpoint, payload=payload)
