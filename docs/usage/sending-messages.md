
# Sending Messages

This guide explains how to send different types of messages using the WhatsApp API Python Package. The `MessagingClient` class is used to handle all message-related operations.

---

## Table of Contents

- [Initializing the MessagingClient](#initializing-the-messagingclient)
- [Mark as Read and Typing Indicator](#mark-message-as-read-and-typing-indicator)
- [Sending a Text Message](#sending-a-text-message)
- [Sending Media Message](./sending-media-message.md)
- [Send Reaction Message](#send-reaction-message)
- [Sending Contact Message](#sending-contact-message)
- [Sending a Button Message](#sending-a-button-message)
- [Validation Rules for Button Messages](#validation-rules-for-button-messages)
- [Sending a List Message](#sending-a-list-message)
- [Validation Rules for List Messages](#validation-rules-for-list-messages)
- [Sending a Location Message](#sending-a-location-message)
- [Sending a Location Request Message](#sending-a-location-request-message)
- [Sending an Interactive Catalog Message](#sending-an-interactive-catalog-message)
- [Response](#response)

---

## Initializing the MessagingClient

To send messages, you must initialize the `MessagingClient` class. The class requires two parameters:
- `access_token`: Your WhatsApp API access token (retrieved from Meta's developer portal).
- `phone_number_id`: The phone number ID associated with your WhatsApp Business account.

### Example: Initialize the MessagingClient
```python
from whatsapp_api.message.messaging import MessagingClient

access_token = "your_access_token_here"
phone_number_id = "your_phone_number_id_here"

# Initialize the MessagingClient
client = MessagingClient(access_token, phone_number_id)
```

---
## Mark Message as Read and Typing Indicator
The `mark_message_as_read` method used to message read status and a reply typing indicator.

### Method Signature
```python
mark_message_as_read(
    context_message_id: str
) -> dict
```

### Parameters
- **`context_message_id`** *(str)*: The message ID of a previous message.

---

## Sending a Text Message

The `send_text_message` method is used to send plain text messages to a recipient.

### Method Signature
```python
send_text_message(
    recipient_phone_number: str, 
    message: str, 
    preview_url: bool = False, 
    context_message_id: Optional[str] = None
) -> dict
```

### Parameters
- **`recipient_phone_number`** *(str)*: The recipient's WhatsApp phone number in international format (e.g., 1234567890, without the +).
- **`message`** *(str)*: The text message content.
- **`preview_url`** *(bool)*: Whether to render a link preview for any URL in the body text string (optional). Default is **`False`**. If multiple URLs are in the body text string, only the first URL will be rendered.
- **`context_message_id`** *(str, optional)*: The message ID of a previous message, if you are sending the contact message as a reply to an existing message. Default is `None`.

### Example: Sending a Text Message
```python
recipient_phone_number = "1234567890"
message = "Hello from WhatsApp API!"

# Send a text message
response = client.send_text_message(recipient_phone_number, message)
print("Response:", response)
```

### Example: Sending a Reply Text Message
```python
response = client.send_text_message(
    recipient_phone_number = "1234567890",
    message = "Hello from WhatsApp API!",
    context_message_id="previous_message_id"
)
print("Response:", response)
```

---


## Send Reaction Message

The `send_reaction_message` method allows you to send a reaction (emoji) to a specific message in a WhatsApp conversation.

### Method Signature
```python
send_reaction_message(recipient_phone_number: str, message_id: str, emoji: str) -> dict
```

### Parameters
- ****`recipient_phone_number`**** *(str)*:  
  The recipient's WhatsApp phone number in international format (e.g., 1234567890, without the +).

- **`message_id`** *(str)*:  
  The ID of the message to which the reaction applies.

- **`emoji`** *(str)*:  
  The emoji for the reaction (e.g., 👍, ❤️, 😂).

### Returns
- A JSON response from the WhatsApp API indicating the success or failure of the operation.

### Example Usage
```python
recipient_phone_number = "1234567890"
message_id = "wam1234567890"
emoji = "❤️"

response = client.send_reaction_message(recipient_phone_number, message_id, emoji)
print("Response:", response)
```

### Notes
- The `message_id` must reference a valid message ID from the conversation.
- Only emojis are allowed in the `emoji` field.

### Related Methods
- [`send_text_message`](#sending-a-text-message)

---
## Sending Contact Message

The `send_contact_message` method allows you to send a contact message to a recipient on WhatsApp. The message includes contact details, such as name, phone numbers, addresses, emails, and other optional information.

### Method Signature
```python
send_contact_message(
    recipient_phone_number: str,
    contact_data: dict,
    context_message_id: Optional[str] = None
) -> dict
```

---

### Parameters
- **`recipient_phone_number`** *(str)*: The recipient's WhatsApp phone number in international format (e.g., `1234567890`, without the `+`).
- **`contact_data`** *(dict)*: A dictionary containing the contact details to send. The structure of `contact_data` should include the following:
  - **`name`** *(dict)*: The contact's full name (required). The object can contain:
    - `formatted_name`: Full name as it normally appears.
    - `first_name`: First name (optional).
    - `last_name`: Last name (optional).
    - `middle_name`: Middle name (optional).
    - `suffix`: Name suffix (optional).
    - `prefix`: Name prefix (optional).
  - **`phones`** *(list)*: A list of phone numbers (required). Each phone object can contain:
    - `phone`: The phone number (required).
    - `wa_id`: WhatsApp ID (optional).
    - `type`: Phone type (optional; possible values: `CELL`, `MAIN`, `IPHONE`, `HOME`, `WORK`).
  - **`addresses`** *(list, optional)*: A list of addresses (optional). Each address object can contain:
    - `street`: Street name and number.
    - `city`: City name.
    - `state`: State abbreviation.
    - `zip`: ZIP code.
    - `country`: Country name.
    - `country_code`: Two-letter country abbreviation.
    - `type`: Address type (optional; possible values: `HOME`, `WORK`).
  - **`birthday`** *(str, optional)*: The contact's birthday in `YYYY-MM-DD` format.
  - **`emails`** *(list, optional)*: A list of emails (optional). Each email object can contain:
    - `email`: Email address.
    - `type`: Email type (optional; possible values: `HOME`, `WORK`).
  - **`org`** *(dict, optional)*: Contact organization information (optional). The object can contain:
    - `company`: Name of the contact's company.
    - `department`: Name of the contact's department.
    - `title`: The contact's business title.
  - **`urls`** *(list, optional)*: A list of URLs (optional). Each URL object can contain:
    - `url`: URL.
    - `type`: URL type (optional; possible values: `HOME`, `WORK`).
  
- **`context_message_id`** *(str, optional)*: The message ID of a previous message, if you are sending the contact message as a reply to an existing message. Default is `None`.

---

### Returns
A dictionary containing the response from the WhatsApp Business API. The response will include a `message ID` for tracking.

---

### Example: Sending a Contact Message

```python
from whatsapp_api.message.messaging import MessagingClient

access_token = "your_access_token_here"
phone_number_id = "your_phone_number_id_here"

# Initialize the MessagingClient
client = MessagingClient(access_token, phone_number_id)

contact_data = {
    "name": {
        "formatted_name": "John Doe",
        "first_name": "John",
        "last_name": "Doe",
        "prefix": "Mr.",
    },
    "phones": [
        {
            "phone": "1234567890",
            "wa_id": "1234567890",
            "type": "HOME"
        }
    ],
    "addresses": [
        {
            "street": "1234 Elm St",
            "city": "Springfield",
            "state": "IL",
            "zip": "62701",
            "country": "USA",
            "country_code": "US",
            "type": "HOME"
        }
    ],
    "emails": [
        {
            "email": "john.doe@example.com",
            "type": "HOME"
        }
    ],
    "org": {
        "company": "Example Inc.",
        "department": "Marketing",
        "title": "Manager"
    },
    "urls": [
        {
            "url": "https://www.johndoe.com",
            "type": "WORK"
        }
    ]
}



# Send a contact message

response = client.send_contact_message(
    recipient_phone_number="9876543210",
    contact_data=contact_data,
    context_message_id="previous_message_id"
)

print("Response:", response)
```

---

### Example Request Payload
The payload sent to the API will look like this:

```json
{
  "messaging_product": "whatsapp",
  "to": "9876543210",
  "type": "contacts",
  "contacts": [
    {
      "name": {
        "formatted_name": "John Doe",
        "first_name": "John",
        "last_name": "Doe",
        "prefix": "Mr."
      },
      "phones": [
        {
          "phone": "1234567890",
          "wa_id": "1234567890",
          "type": "HOME"
        }
      ],
      "addresses": [
        {
          "street": "1234 Elm St",
          "city": "Springfield",
          "state": "IL",
          "zip": "62701",
          "country": "USA",
          "country_code": "US",
          "type": "HOME"
        }
      ],
      "emails": [
        {
          "email": "john.doe@example.com",
          "type": "HOME"
        }
      ],
      "org": {
        "company": "Example Inc.",
        "department": "Marketing",
        "title": "Manager"
      },
      "urls": [
        {
          "url": "https://www.johndoe.com",
          "type": "WORK"
        }
      ]
    }
  ]
}
```

---

### Notes
- The `contact_data` dictionary must include at least a `name` object with a `formatted_name` and a `phones` array with at least one phone number.
- All fields in the `contact_data` dictionary are optional except for `name` and `phones`.
- The `context_message_id` is optional and is used to reply to a previous message.
- The API will return a `message ID` for the sent contact message, which can be used for tracking.

---

## Sending a Button Message

The `send_button_message` method is used to send interactive button messages. These messages can contain up to 3 buttons that the recipient can tap.

### Method Signature
```python
send_button_message(recipient_phone_number: str, text: str, buttons: list[dict]) -> dict
```

### Parameters
- **`recipient_phone_number`** *(str)*: The recipient's WhatsApp phone number in international format (e.g., 1234567890, without the +).
- **`text`** *(str)*: The message text to display above the buttons.
- **`buttons`** *(list[dict])*: A list of button objects. Each button must include:
  - **`type`** *(str)*: The type of the button (e.g., `"reply"`).
  - **`reply`** *(dict)*:
    - **`id`** *(str)*: A unique identifier for the button.
    - **`title`** *(str)*: The button text (max 20 characters).
- **`context_message_id`** *(str, optional)*: The message ID of a previous message, if you are sending the contact message as a reply to an existing message. Default is `None`.

### Example: Sending a Button Message

```python
recipient_phone_number = "1234567890"
text = "Do you agree with our terms?"
buttons = [
    {"type": "reply", "reply": {"id": "btn_yes", "title": "Yes"}},
    {"type": "reply", "reply": {"id": "btn_no", "title": "No"}},
]

# Send a button message
response = client.send_button_message(recipient_phone_number, text, buttons)
print("Response:", response)
```

---

## Validation Rules for Button Messages

When sending button messages, the **`buttons`** parameter must adhere to the following rules. If any rule is violated, a `ValueError` is raised.

### Button Validation Table

| **Attribute**   | **Type**        | **Constraints**                                                          |
|------------------|-----------------|---------------------------------------------------------------------------|
| `buttons`        | List[dict]      | Must be a list of dictionaries.                                           |                                      |
| `type`           | String          | Must be `"reply"`.                                                        |
| `reply.id`       | String          | Must be unique for each button.                                           |
| `reply.title`    | String          | Maximum 20 characters.                                                   |

### Example: Invalid Button Configuration
```python
try:
    buttons = [
        {"type": "reply", "reply": {"id": "duplicate_id", "title": "Yes"}},
        {"type": "reply", "reply": {"id": "duplicate_id", "title": "No"}},
    ]
    client.send_button_message("1234567890", "Choose an option:", buttons)
except ValueError as e:
    print("Validation Error:", e)
```

---

## Sending a List Message

The `send_list_message` method is used to send an interactive list message. List messages allow you to present a set of selectable options to the recipient.

### Method Signature
```python
send_list_message(
    recipient_phone_number: str,
    body_text: str,
    sections: list[dict],
    button_cta: str,
    header_text: Optional[str] = None,
    footer_text: Optional[str] = None,
) -> dict
```

### Parameters
- **`recipient_phone_number`** *(str)*: The recipient's WhatsApp phone number in international format (e.g., 1234567890, without the +).
- **`body_text`** *(str)*: The main body text of the message (max 4096 characters).
- **`sections`** *(list[dict])*: A list of sections, where each section must include:
  - **`title`** *(str)*: The title of the section (max 24 characters).
  - **`rows`** *(list[dict])*: A list of rows, where each row must include (1–10):
    - **`id`** *(str)*: A unique identifier for the row.
    - **`title`** *(str)*: The row title (max 24 characters).
    - **`description`** *(Optional[str])*: A brief description of the row (max 72 characters).
- **`button_cta`** *(str)*: The label text for the Call-To-Action button (max 20 characters).
- **`header_text`** *(Optional[str])*: An optional header for the message (max 60 characters).
- **`footer_text`** *(Optional[str])*: An optional footer for the message (max 60 characters).
- **`context_message_id`** *(str, optional)*: The message ID of a previous message, if you are sending the contact message as a reply to an existing message. Default is `None`.

### Example: Sending a List Message
```python
recipient_phone_number = "1234567890"
body_text = "Choose one of the following options:"
button_cta = "View Options"
sections = [
    {
        "title": "Available Options",
        "rows": [
            {"id": "option1", "title": "Option 1", "description": "Description for option 1"},
            {"id": "option2", "title": "Option 2", "description": "Description for option 2"},
        ],
    }
]
header_text = "Choose an Option"
footer_text = "Thank you for using our service!"

# Send a list message
response = client.send_list_message(recipient_phone_number, body_text, sections, button_cta, header_text, footer_text)
print("Response:", response)
```

---

## Validation Rules for List Messages

When sending list messages, the parameters must meet the following rules. If any rule is violated, a `ValueError` is raised.

### List Validation Table

| **Parameter**    | **Type**        | **Constraints**                                                          |
|-------------------|-----------------|---------------------------------------------------------------------------|
| `body_text`       | String          | Required. Maximum 4096 characters.                                       |
| `button_cta`      | String          | Required. Maximum 20 characters.                                         |
| `header_text`     | String          | Optional. Maximum 60 characters.                                         |
| `footer_text`     | String          | Optional. Maximum 60 characters.                                         |
| `sections`        | List[dict]      | Required. Maximum 10 sections.                                           |
| **Section Title** | String          | Maximum 24 characters.                                                   |
| **Rows**          | List[dict]      | Must contain a list of rows (1–10).                         |
| `row.id`          | String          | Must be unique for each row. Maximum 200 characters.                     |
| `row.title`       | String          | Maximum 24 characters.                                                   |
| `row.description` | String          | Optional. Maximum 72 characters.                                         |

### Example: Invalid List Configuration
```python
try:
    sections = [
        {
            "title": "Section Title That Is Too Long To Be Valid",
            "rows": [
                {"id": "row1", "title": "Row 1", "description": "Valid description"},
            ],
        },
    ]
    client.send_list_message("1234567890", "Choose an option:", sections, "Options")
except ValueError as e:
    print("Validation Error:", e)
```

---

## Sending a Location Message

The `send_location_message` method sends a precise latitude/longitude location to a WhatsApp user.

### Method Signature
```python
send_location_message(
    recipient_phone_number: str,
    latitude: str | float,
    longitude: str | float,
    name: Optional[str] = None,
    address: Optional[str] = None,
    context_message_id: Optional[str] = None,
) -> dict
```

### Parameters
- **`recipient_phone_number`** *(str)*: The recipient's WhatsApp phone number in international format (e.g., 1234567890, without the +).
- **`latitude`** *(str | float)*: Location latitude in decimal degrees (required).
- **`longitude`** *(str | float)*: Location longitude in decimal degrees (required).
- **`name`** *(str, optional)*: Optional location name.
- **`address`** *(str, optional)*: Optional location address.
- **`context_message_id`** *(str, optional)*: Message ID of a previous message if replying within an existing thread. Default is `None`.

### Example: Sending a Location Message
```python
recipient_phone_number = "1234567890"

response = client.send_location_message(
    recipient_phone_number=recipient_phone_number,
    latitude="37.7749",
    longitude="-122.4194",
    name="Golden Gate Park",
    address="San Francisco, CA",
    context_message_id="previous_message_id"
)

print("Response:", response)
```

### Example Request Payload
```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "1234567890",
  "type": "location",
  "location": {
    "latitude": "37.7749",
    "longitude": "-122.4194",
    "name": "Golden Gate Park",
    "address": "San Francisco, CA"
  },
  "context": {
    "message_id": "previous_message_id"
  }
}
```

---

## Sending a Location Request Message

The `send_location_request_message` method asks the user to share their location via the WhatsApp interactive "Send Location" flow.

### Method Signature
```python
send_location_request_message(
    recipient_phone_number: str,
    body_text: str,
    context_message_id: Optional[str] = None,
) -> dict
```

### Parameters
- **`recipient_phone_number`** *(str)*: The recipient's WhatsApp phone number in international format (e.g., 1234567890, without the +).
- **`body_text`** *(str)*: The body text for the prompt (max 1024 characters).
- **`context_message_id`** *(str, optional)*: Message ID of a previous message if replying within an existing thread. Default is `None`.

### Example: Sending a Location Request Message
```python
recipient_phone_number = "1234567890"
body_text = "Please share your location to find nearby stores."

response = client.send_location_request_message(
    recipient_phone_number=recipient_phone_number,
    body_text=body_text,
    context_message_id="previous_message_id"
)

print("Response:", response)
```

### Example Request Payload
```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "1234567890",
  "type": "interactive",
  "interactive": {
    "type": "location_request_message",
    "body": {
      "text": "Please share your location to find nearby stores."
    },
    "action": {
      "name": "send_location"
    }
  },
  "context": {
    "message_id": "previous_message_id"
  }
}
```

---

## Sending an Interactive Catalog Message

The `send_interactive_catalog_message` method sends a catalog message that highlights a single product from your WhatsApp catalog.

### Method Signature
```python
send_interactive_catalog_message(
    recipient_phone_number: str,
    body_text: str,
    product_retailer_id: str,
    footer_text: Optional[str] = None,
    context_message_id: Optional[str] = None,
) -> dict
```

### Parameters
- **`recipient_phone_number`** *(str)*: The recipient's WhatsApp phone number in international format (e.g., 1234567890, without the +).
- **`body_text`** *(str)*: The text shown above the catalog item. Maximum 1024 characters.
- **`product_retailer_id`** *(str)*: The retailer ID of the product you want to feature.
- **`footer_text`** *(str, optional)*: Optional footer text for the message (max 60 characters).
- **`context_message_id`** *(str, optional)*: Message ID of a previous message if replying within an existing thread.

### Example: Sending an Interactive Catalog Message
```python
recipient_phone_number = "1234567890"
body_text = "Explore our featured planter"
product_retailer_id = "SKU-PLANTER-001"

response = client.send_interactive_catalog_message(
    recipient_phone_number=recipient_phone_number,
    body_text=body_text,
    product_retailer_id=product_retailer_id,
    footer_text="Limited time offer",
    context_message_id="previous_message_id"
)

print("Response:", response)
```

---

## Response

All methods return the API response as a dictionary. On success, the response typically includes a `message_id` or confirmation details.

### Example Response
```json
{
    "messaging_product": "whatsapp",
    "contacts": [
        {
            "input": "1234567890",
            "wa_id": "1234567890",
            "messages": [
                {
                    "id": "wamid.HBgMNTk0Mxxxxxxxxxxxxxxxxxxxxxxxx"
                }
            ]
        }
    ]
}
```
---
