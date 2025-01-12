from whatsapp_api.base_client import BaseClient
from whatsapp_api.Message.validation import validate_buttons, validate_list_message


class MessagingClient(BaseClient):
    def __init__(self, access_token, phone_number_id):
        """
        Messaging client for WhatsApp.

        :param access_token: Meta API access token
        :param phone_number_id: Phone number ID from WhatsApp
        """
        super().__init__(access_token)
        self.endpoint = f"{phone_number_id}/messages"

    # Send Text Message
    def send_text_message(self, recipient_id, message, preview_url=False):
        """
        Send a text message.

        :param recipient_id: The recipient's WhatsApp number
        :param message: The message content - Maximum 4096 characters.
        :param preview_url: Preview URL render a link preview of any URL in the body text string. (optional)
        :return: API response JSON
        """

        # Prepare the payload
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "text",
            "text": {
                "preview_url": preview_url, 
                "body": message
            },
        }
        return self._request("POST", self.endpoint, payload)

    # Send Reply to Text Message
    def reply_text_message(self, recipient_id, message, previous_message_id, preview_url=False):
        """
        Send a reply to a text message.

        :param recipient_id: The recipient's WhatsApp number
        :param message: The reply message content - Maximum 4096 characters.
        :param previous_message_id: The ID of the previous message in the conversation.
        :param preview_url: Preview URL render a link preview of any URL in the body text string. (optional)
        :return: API response JSON
        """

        # Prepare the payload
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_id,
            "context": {
                "message_id": previous_message_id
            },
            "type": "text",
            "text": {
                "preview_url": preview_url,
                "body": message
            }
        }

        return self._request("POST", self.endpoint, payload)

    # Send Reply with Reaction Message
    def send_reaction_message(self, recipient_id, message_id, emoji):
        """
        Send a reaction to a specific WhatsApp message.

        :param recipient_id: The recipient's WhatsApp phone number in international format (e.g., 1234567890).
        :param message_id: The ID of the message to which the reaction applies.
        :param emoji: The emoji for the reaction (e.g., 👍, ❤️, 😂).
        :return: API response JSON
        """
        # Prepare the payload
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_id,
            "type": "reaction",
            "reaction": {
                "message_id": message_id,
                "emoji": emoji,
            },
        }

        return self._request("POST", self.endpoint, payload)

    # Send Interactive Message with Buttons
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

    # Send Interactive List Message with Header and Footer
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
