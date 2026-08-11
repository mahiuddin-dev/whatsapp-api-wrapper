import os
import sys
import unittest
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from whatsapp_api.wa_profile.profile import Profile


class TestProfile(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        self.access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
        self.phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

        # Initialize Profile
        self.profile = Profile(self.access_token, self.phone_number_id)

    @patch("requests.request")
    def test_get_profile_success(self, mock_request):
        """Test successful profile retrieval."""
        mock_request.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "data": [
                    {
                        "about": "Mock about",
                        "address": "Mock address",
                        "email": "mock@example.com",
                        "description": "Mock description",
                        "profile_picture_url": "https://example.com/pic.jpg",
                        "websites": ["https://example.com"],
                    }
                ]
            },
        )

        response = self.profile.get_profile()

        self.assertEqual(response["data"][0]["about"], "Mock about")
        mock_request.assert_called_once_with(
            "GET",
            f"{self.profile.base_url}{self.profile.endpoint}",
            params={
                "fields": "about,address,email,description,profile_picture_url,websites"
            },
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            },
        )

    @patch("requests.request")
    def test_update_profile_only_sends_provided_fields(self, mock_request):
        """Test that update_profile only includes fields that were passed in."""
        mock_request.return_value = MagicMock(status_code=200, json=lambda: {"success": True})

        response = self.profile.update_profile(about="New about", email="new@example.com")

        self.assertEqual(response, {"success": True})
        mock_request.assert_called_once_with(
            "POST",
            f"{self.profile.base_url}{self.profile.endpoint}",
            json={
                "messaging_product": "whatsapp",
                "about": "New about",
                "email": "new@example.com",
            },
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            },
        )

    @patch("requests.request")
    def test_update_profile_all_fields(self, mock_request):
        """Test update_profile with every supported field set."""
        mock_request.return_value = MagicMock(status_code=200, json=lambda: {"success": True})

        response = self.profile.update_profile(
            about="About",
            address="Address",
            description="Description",
            email="email@example.com",
            websites=["https://example.com"],
        )

        self.assertEqual(response, {"success": True})
        mock_request.assert_called_once_with(
            "POST",
            f"{self.profile.base_url}{self.profile.endpoint}",
            json={
                "messaging_product": "whatsapp",
                "about": "About",
                "address": "Address",
                "description": "Description",
                "email": "email@example.com",
                "websites": ["https://example.com"],
            },
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            },
        )

    @patch("requests.request")
    def test_update_profile_no_fields(self, mock_request):
        """Test update_profile with no fields set only sends messaging_product."""
        mock_request.return_value = MagicMock(status_code=200, json=lambda: {"success": True})

        response = self.profile.update_profile()

        self.assertEqual(response, {"success": True})
        mock_request.assert_called_once_with(
            "POST",
            f"{self.profile.base_url}{self.profile.endpoint}",
            json={"messaging_product": "whatsapp"},
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            },
        )

    @patch("requests.request")
    def test_update_profile_picture_success(self, mock_request):
        """Test successful profile picture update using an uploaded media file ID."""
        mock_request.return_value = MagicMock(status_code=200, json=lambda: {"success": True})

        media_id = "mock_uploaded_media_id"
        response = self.profile.update_profile_picture(media_id)

        self.assertEqual(response, {"success": True})
        mock_request.assert_called_once_with(
            "POST",
            f"{self.profile.base_url}{self.profile.endpoint}",
            json={
                "messaging_product": "whatsapp",
                "profile_picture_handle": media_id,
            },
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            },
        )

    @patch("requests.request")
    def test_request_error_raises_exception(self, mock_request):
        """Test that a non-200 response raises an exception."""
        mock_request.return_value = MagicMock(status_code=400, text="Bad Request")

        with self.assertRaises(Exception):
            self.profile.get_profile()


if __name__ == "__main__":
    unittest.main()
