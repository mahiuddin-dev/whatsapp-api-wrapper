from whatsapp_api.base_client import BaseClient
from whatsapp_api.validation import validate_buttons, validate_list_message


class MessagingClient(BaseClient):
    def __init__(self, access_token, phone_number_id):
        """
        Messaging client for WhatsApp.

        :param access_token: Meta API access token
        :param phone_number_id: Phone number ID from WhatsApp
        """
        super().__init__(access_token)
        self.endpoint = f"{phone_number_id}/messages"

    def send_text_message(self, recipient_id, message):
        """
        Send a text message.

        :param recipient_id: The recipient's WhatsApp number
        :param message: The message content
        :return: API response JSON
        """

        # Prepare the payload
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "text",
            "text": {"body": message},
        }
        return self._request("POST", self.endpoint, payload)

    def send_button_message(self, recipient_id, text, buttons):
        """
        Send an interactive button message.

        :param recipient_id: The recipient's WhatsApp number
        :param text: The message text
        :param buttons: List of button dictionaries 
        :return: API response JSON
        """
        # Validate the buttons
        validate_buttons(buttons)

        # Prepare the payload
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": text},
                "action": {"buttons": buttons},
            },
        }
        return self._request("POST", self.endpoint, payload)

    def send_list_message(self, recipient_id, body_text, sections, button_cta, header_text=None, footer_text=None):
        """
        Send an interactive list message.

        :param recipient_id: The recipient's WhatsApp number.
        :param body_text: The main body text of the message.
        :param sections: List of section dictionaries (with title and rows).
        :param button_cta: Button label text (CTA button).
        :param header_text: Optional header text (max 60 characters).
        :param footer_text: Optional footer text (max 60 characters).
        :return: API response JSON.
        """
        # Validate the inputs
        validate_list_message(body_text, sections, button_cta, header_text, footer_text)

        # Prepare the payload
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_id,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {"text": body_text},
                "action": {"button": button_cta, "sections": sections},
            },
        }

        # Add optional header
        if header_text:
            payload["interactive"]["header"] = {"type": "text", "text": header_text}

        # Add optional footer
        if footer_text:
            payload["interactive"]["footer"] = {"text": footer_text}

        return self._request("POST", self.endpoint, payload)
