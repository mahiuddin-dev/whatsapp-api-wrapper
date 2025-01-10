
# Sending Messages

This guide explains how to send different types of messages using the WhatsApp API Python Package. The `MessagingClient` class is used to handle all message-related operations.

---

## Table of Contents

- [Initializing the MessagingClient](#initializing-the-messagingclient)
- [Sending a Text Message](#sending-a-text-message)
- [Sending a Button Message](#sending-a-button-message)
- [Validation Rules for Button Messages](#validation-rules-for-button-messages)
- [Sending a List Message](#sending-a-list-message)
- [Validation Rules for List Messages](#validation-rules-for-list-messages)
- [Response](#response)
- [Error Handling](#error-handling)

---

## Initializing the MessagingClient

To send messages, you must initialize the `MessagingClient` class. The class requires two parameters:
- `access_token`: Your WhatsApp API access token (retrieved from Meta's developer portal).
- `phone_number_id`: The phone number ID associated with your WhatsApp Business account.

### Example: Initialize the MessagingClient
```python
from whatsapp_api.messaging import MessagingClient

access_token = "your_access_token_here"
phone_number_id = "your_phone_number_id_here"

# Initialize the MessagingClient
client = MessagingClient(access_token, phone_number_id)
```

---

## Sending a Text Message

The `send_text_message` method is used to send plain text messages to a recipient.

### Method Signature
```python
send_text_message(recipient_id: str, message: str) -> dict
```

### Parameters
- `recipient_id` *(str)*: The recipient's WhatsApp phone number in international format (e.g., `+1234567890`).
- `message` *(str)*: The text message content.

### Example: Sending a Text Message
```python
recipient_id = "+1234567890"
message = "Hello from WhatsApp API!"

# Send a text message
response = client.send_text_message(recipient_id, message)
print("Response:", response)
```
---
## Sending a Button Message

The `send_button_message` method is used to send interactive button messages. These messages can contain up to 3 buttons that the recipient can tap.

### Method Signature
```python
send_button_message(recipient_id: str, text: str, buttons: list[dict]) -> dict
```

### Parameters
- `recipient_id` *(str)*: The recipient's WhatsApp phone number in international format (e.g., `+1234567890`).
- `text` *(str)*: The message text to display above the buttons.
- `buttons` *(list[dict])*: A list of button objects. Each button must include:
  - `type` *(str)*: The type of the button (e.g., `"reply"`).
  - `reply` *(dict)*:
    - `id` *(str)*: A unique identifier for the button.
    - `title` *(str)*: The button text (max 20 characters).

### Example: Sending a Button Message

```python
recipient_id = "+1234567890"
text = "Do you agree with our terms?"
buttons = [
    {"type": "reply", "reply": {"id": "btn_yes", "title": "Yes"}},
    {"type": "reply", "reply": {"id": "btn_no", "title": "No"}},
]

# Send a button message
response = client.send_button_message(recipient_id, text, buttons)
print("Response:", response)
```

---

## Validation Rules for Button Messages

When sending button messages, the `buttons` parameter must adhere to the following rules. If any rule is violated, a `ValueError` is raised.

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
    client.send_button_message("+1234567890", "Choose an option:", buttons)
except ValueError as e:
    print("Validation Error:", e)
```

---

## Sending a List Message

The `send_list_message` method is used to send an interactive list message. List messages allow you to present a set of selectable options to the recipient.

### Method Signature
```python
send_list_message(
    recipient_id: str,
    body_text: str,
    sections: list[dict],
    button_cta: str,
    header_text: Optional[str] = None,
    footer_text: Optional[str] = None,
) -> dict
```

### Parameters
- `recipient_id` *(str)*: The recipient's WhatsApp phone number in international format (e.g., `+1234567890`).
- `body_text` *(str)*: The main body text of the message (max 4096 characters).
- `sections` *(list[dict])*: A list of sections, where each section must include:
  - `title` *(str)*: The title of the section (max 24 characters).
  - `rows` *(list[dict])*: A list of rows, where each row must include (1–10):
    - `id` *(str)*: A unique identifier for the row.
    - `title` *(str)*: The row title (max 24 characters).
    - `description` *(Optional[str])*: A brief description of the row (max 72 characters).
- `button_cta` *(str)*: The label text for the Call-To-Action button (max 20 characters).
- `header_text` *(Optional[str])*: An optional header for the message (max 60 characters).
- `footer_text` *(Optional[str])*: An optional footer for the message (max 60 characters).


### Example: Sending a List Message
```python
recipient_id = "+1234567890"
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
response = client.send_list_message(recipient_id, body_text, sections, button_cta, header_text, footer_text)
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
    client.send_list_message("+1234567890", "Choose an option:", sections, "Options")
except ValueError as e:
    print("Validation Error:", e)
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

## Error Handling

### Example
```python
try:
    client.send_list_message("+1234567890", "Choose an option:", [], "CTA Button")
except ValueError as e:
    print("Validation Error:", e)
```
Output:
```plaintext
Validation Error: Sections must be a non-empty list of dictionaries.
```
