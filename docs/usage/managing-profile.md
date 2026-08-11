
# Managing the Business Profile

This guide explains how to view and update your WhatsApp Business Profile using the WhatsApp API Python Package. The `Profile` class is used to handle all business profile-related operations.

---

## Table of Contents

- [Initializing the Profile Client](#initializing-the-profile-client)
- [Get Profile](#get-profile)
- [Update Profile](#update-profile)
- [Update Profile Picture](#update-profile-picture)

---

## Initializing the Profile Client

To manage your business profile, you must initialize the `Profile` class. The class requires two parameters:
- `access_token`: Your WhatsApp API access token (retrieved from Meta's developer portal).
- `phone_number_id`: The phone number ID associated with your WhatsApp Business account.

### Example: Initialize the Profile Client
```python
from whatsapp_api.wa_profile.profile import Profile

access_token = "your_access_token_here"
phone_number_id = "your_phone_number_id_here"

# Initialize the Profile client
profile = Profile(access_token, phone_number_id)
```
---

## Get Profile

The `get_profile` method retrieves the current WhatsApp Business Profile, including `about`, `address`, `email`, `description`, `profile_picture_url`, and `websites`.

---

### Method Signature
```python
get_profile() -> dict
```

---

### Returns
A dictionary containing the business profile fields. The structure of the response is as follows:
```json
{
    "data": [
        {
            "about": "This is a test business.",
            "address": "1 Hacker Way, Menlo Park, CA 94025",
            "description": "We sell the best products.",
            "email": "contact@example.com",
            "profile_picture_url": "https://example.com/picture.jpg",
            "websites": ["https://example.com"]
        }
    ]
}
```

---

### Exceptions
The method raises an `Exception` if the API request fails. This includes cases such as:
- Unauthorized access due to invalid or expired access tokens
- API errors (e.g., rate limiting, server issues)

---

### Example Usage
```python
from whatsapp_api.wa_profile.profile import Profile

access_token = "your_meta_api_access_token"
phone_number_id = "your_phone_number_id"

profile = Profile(access_token, phone_number_id)

try:
    business_profile = profile.get_profile()
    print("Business Profile:", business_profile)
except Exception as e:
    print(f"Failed to retrieve business profile: {e}")
```

---

## Update Profile

The `update_profile` method is used to update the text fields of the business profile. Only the fields you pass in are sent to the API, so you can update a single field without affecting the others. The profile picture cannot be updated with this method; use [`update_profile_picture`](#update-profile-picture) instead.

---

### Method Signature
```python
update_profile(
    about: Optional[str] = None,
    address: Optional[str] = None,
    description: Optional[str] = None,
    email: Optional[str] = None,
    websites: Optional[list] = None,
) -> dict
```

---

### Parameters
| Name              | Type          | Description                                                        |
|-------------------|---------------|----------------------------------------------------------------------|
| **`about`**       | `str`         | A short description shown at the top of the business profile.        |
| **`address`**     | `str`         | The business address.                                                |
| **`description`** | `str`         | A longer description of the business.                                |
| **`email`**       | `str`         | The business contact email address.                                  |
| **`websites`**    | `list[str]`   | Up to two website URLs associated with the business.                 |

All parameters are optional. Only the fields explicitly passed in are included in the update request.

---

### Returns
A dictionary containing the response from the WhatsApp Business API confirming the update.

---

### Exceptions
The method raises an `Exception` if the API request fails, such as invalid field values or authentication issues.

---

### Example Usage
```python
from whatsapp_api.wa_profile.profile import Profile

access_token = "your_meta_api_access_token"
phone_number_id = "your_phone_number_id"

profile = Profile(access_token, phone_number_id)

# Update only the "about" and "email" fields
response = profile.update_profile(
    about="We sell the best products.",
    email="contact@example.com"
)
print("Response:", response)
```

---

## Update Profile Picture

The `update_profile_picture` method updates the business profile picture using the ID of an already uploaded media file. Upload the image first using [`MediaClient.upload_media`](sending-media-message.md#upload-media) to obtain the media ID.

---

### Method Signature
```python
update_profile_picture(uploaded_media_file_id: str) -> dict
```

---

### Parameters
- `uploaded_media_file_id` *(str)*: The media ID of a previously uploaded image to use as the new profile picture.

---

### Returns
A dictionary containing the response from the WhatsApp Business API confirming the update.

---

### Exceptions
The method raises an `Exception` if the API request fails, such as an invalid or expired media ID.

---

### Example Usage
```python
from whatsapp_api.media.media_client import MediaClient
from whatsapp_api.wa_profile.profile import Profile

access_token = "your_meta_api_access_token"
phone_number_id = "your_phone_number_id"

media_client = MediaClient(access_token, phone_number_id)
profile = Profile(access_token, phone_number_id)

# 1) Upload the new profile picture
media_id = media_client.upload_media("/local/path/to/picture.jpg")

# 2) Set it as the profile picture
response = profile.update_profile_picture(media_id)
print("Response:", response)
```

---

### Related Methods
- [`upload_media`](sending-media-message.md#upload-media) – Upload the image and get the media ID used here.
