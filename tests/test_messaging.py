import os
import sys
import unittest
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from whatsapp_api.Message.messaging import MessagingClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class TestMessagingClient(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        # Load variables from .env
        self.access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
        self.phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        self.recipient_id = os.getenv("TEST_RECIPIENT_ID")

        if not self.access_token or not self.phone_number_id or not self.recipient_id:
            raise EnvironmentError("Missing environment variables in .env file.")

        # Initialize the MessagingClient
        self.client = MessagingClient(self.access_token, self.phone_number_id)


    @patch("whatsapp_api.base_client.BaseClient._request")
    def test_send_text_message(self, mock_request):
        """Test sending a text message."""
        mock_request.return_value = {"success": True}

        response = self.client.send_text_message(self.recipient_id, "Hello, World!")
        self.assertEqual(response, {"success": True})

        mock_request.assert_called_once_with(
            "POST",
            f"{self.phone_number_id}/messages",
            {
                "messaging_product": "whatsapp",
                "to": self.recipient_id,
                "type": "text",
                "text": {
                    'preview_url': False,
                    "body": "Hello, World!"
                },
            },
        )

    @patch("whatsapp_api.base_client.BaseClient._request")
    def test_reply_text_message(self, mock_request):
        """Test replying to a text message."""
        mock_request.return_value = {"success": True}

        previous_message_id = "abc123"
        message = "Thank you for your message!"

        response = self.client.reply_text_message(self.recipient_id, message, previous_message_id)
        self.assertEqual(response, {"success": True})

        mock_request.assert_called_once_with(
            "POST",
            f"{self.phone_number_id}/messages",
            {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": self.recipient_id,
                "context": {
                    "message_id": previous_message_id
                },
                "type": "text",
                "text": {
                    "preview_url": False,
                    "body": message
                }
            },
        )

    @patch("whatsapp_api.base_client.BaseClient._request")
    def test_send_button_message(self, mock_request):
        """Test sending a button message."""
        mock_request.return_value = {"success": True}

        buttons = [
            {"type": "reply", "reply": {"id": "btn1", "title": "Button 1"}},
            {"type": "reply", "reply": {"id": "btn2", "title": "Button 2"}},
        ]

        response = self.client.send_button_message(self.recipient_id, "Choose an option:", buttons)
        self.assertEqual(response, {"success": True})

        mock_request.assert_called_once_with(
            "POST",
            f"{self.phone_number_id}/messages",
            {
                "messaging_product": "whatsapp",
                "to": self.recipient_id,
                "type": "interactive",
                "interactive": {
                    "type": "button",
                    "body": {"text": "Choose an option:"},
                    "action": {"buttons": buttons},
                },
            },
        )

    @patch("whatsapp_api.base_client.BaseClient._request")
    def test_send_list_message(self, mock_request):
        """Test sending a list message."""
        mock_request.return_value = {"success": True}

        sections = [
            {
                "title": "I want it ASAP!",
                "rows": [
                    {"id": "priority_express", "title": "Priority Mail Express", "description": "Next Day to 2 Days"},
                    {"id": "priority_mail", "title": "Priority Mail", "description": "1–3 Days"},
                ],
            },
        ]

        response = self.client.send_list_message(
            self.recipient_id,
            body_text="Which shipping option do you prefer?",
            sections=sections,
            button_cta="Shipping Options",
            header_text="Choose Shipping Option",
            footer_text="Lucky Shrub: Your gateway to succulents™"
        )
        self.assertEqual(response, {"success": True})

        mock_request.assert_called_once_with(
            "POST",
            f"{self.phone_number_id}/messages",
            {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": self.recipient_id,
                "type": "interactive",
                "interactive": {
                    "type": "list",
                    "body": {"text": "Which shipping option do you prefer?"},
                    "header": {"type": "text", "text": "Choose Shipping Option"},
                    "footer": {"text": "Lucky Shrub: Your gateway to succulents™"},
                    "action": {
                        "button": "Shipping Options",
                        "sections": sections,
                    },
                },
            },
        )

if __name__ == "__main__":
    unittest.main()
