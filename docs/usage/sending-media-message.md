
# Sending Media Messages

This guide explains how to send media messages using the WhatsApp API Python Package. The `MediaClient` class is used to handle all media message-related operations.

---

## Table of Contents

- [Initializing the MediaClient](#initializing-the-mediaclient)
- [Upload Media](#upload-media)
- [Retrieve Media URL by Media ID](#retrieve-media-url-by-media-id)
- [Retrieve Media Content by Media URL](#retrieve-media-content-by-media-url)
- [Delete Media by Media ID](#delete-media-by-media-id)
- [Download Media](#download-media)
- [Sending Media Message By ID](#sending-media-message-by-id)
- [Sending Media Message By URL](#sending-media-message-by-url)
- [Response](#response)

---

## Initializing the MediaClient

To send media messages, you must initialize the `MediaClient` class. The class requires two parameters:
- `access_token`: Your WhatsApp API access token (retrieved from Meta's developer portal).
- `phone_number_id`: The phone number ID associated with your WhatsApp Business account.

### Example: Initialize the MediaClient
```python
from whatsapp_api.media.media_client import MediaClient

access_token = "your_access_token_here"
phone_number_id = "your_phone_number_id_here"

# Initialize the MediaClient
media_client = MediaClient(access_token, phone_number_id)
```
---

## Upload Media

The `upload_media` method is used to upload media files (e.g., images, videos, documents, audio, Sticker) to the WhatsApp Business API. Uploaded media files are encrypted and persist for 30 days unless deleted earlier. After a successful upload, the API returns a unique `media ID` that can be used to send media messages.

---

### Method Signature

```python
upload_media(file_path: str) -> str
```

---

### Parameters

| Name             | Type   | Description                                                                                                 |
|------------------|--------|-------------------------------------------------------------------------------------------------------------|
| **`file_path`**  | `str`  | The path to the media file to be uploaded. For example, `/local/path/to/file.jpg`.                          |

---

### Returns

- An unique media ID returned by the API after a successful upload.

---

### Supported Media Types

The `type` of the media file being uploaded must match one of the supported types listed below. The MIME type is automatically detected by the method based on the file extension.

#### Audio
| Audio Type       | Extension | MIME Type                   | Max Size |
|------------------|-----------|-----------------------------|----------|
| AAC              | `.aac`    | `audio/aac`                 | 16 MB    |
| AMR              | `.amr`    | `audio/amr`                 | 16 MB    |
| MP3              | `.mp3`    | `audio/mpeg`                | 16 MB    |
| MP4 Audio        | `.m4a`    | `audio/mp4`                 | 16 MB    |
| OGG Audio        | `.ogg`    | `audio/ogg` (OPUS codecs)   | 16 MB    |

#### Document
| Document Type       | Extension  | MIME Type                                                                 | Max Size |
|---------------------|------------|---------------------------------------------------------------------------|----------|
| Text               | `.txt`     | `text/plain`                                                              | 100 MB   |
| Microsoft Excel    | `.xls`     | `application/vnd.ms-excel`                                                | 100 MB   |
| Microsoft Excel    | `.xlsx`    | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`        | 100 MB   |
| Microsoft Word     | `.doc`     | `application/msword`                                                      | 100 MB   |
| Microsoft Word     | `.docx`    | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | 100 MB   |
| Microsoft PowerPoint | `.ppt`    | `application/vnd.ms-powerpoint`                                           | 100 MB   |
| Microsoft PowerPoint | `.pptx`   | `application/vnd.openxmlformats-officedocument.presentationml.presentation`| 100 MB   |
| PDF                | `.pdf`     | `application/pdf`                                                         | 100 MB   |

#### Image
| Image Type         | Extension  | MIME Type       | Max Size |
|--------------------|------------|-----------------|----------|
| JPEG               | `.jpeg`   | `image/jpeg`    | 5 MB     |
| PNG                | `.png`    | `image/png`     | 5 MB     |

#### Sticker
| Sticker Type       | Extension  | MIME Type       | Max Size |
|--------------------|------------|-----------------|----------|
| Animated Sticker   | `.webp`   | `image/webp`    | 500 KB   |
| Static Sticker     | `.webp`   | `image/webp`    | 100 KB   |

#### Video
| Video Type         | Extension  | MIME Type       | Max Size |
|--------------------|------------|-----------------|----------|
| 3GPP               | `.3gp`    | `video/3gpp`    | 16 MB    |
| MP4 Video          | `.mp4`    | `video/mp4`     | 16 MB    |

---

### Example: Uploading Media

#### Uploading an Image
```python
from whatsapp_api.media.media_client import MediaClient

# Initialize MediaClient
access_token = "your_access_token"
phone_number_id = "your_phone_number_id"
media_client = MediaClient(access_token, phone_number_id)

# Upload an image file
file_path = "/local/path/to/image.jpg"
media_id = media_client.upload_media(file_path)

print(f"Media ID: {media_id}")
```

#### Uploading a PDF
```python
# Upload a PDF document
file_path = "/local/path/to/document.pdf"
media_id = media_client.upload_media(file_path)

print(f"Media ID: {media_id}")
```

Other file types such as Audio, Stickers, and Videos also utilize the same `upload_media` method for uploading.

---

### Error Handling

The `upload_media` method raises exceptions for the following cases:

1. **File Not Found**:
   - Raised if the specified file does not exist.
   - Exception: `FileNotFoundError`

   ```python
   FileNotFoundError: File '/path/to/nonexistent.jpg' does not exist.
   ```

2. **MIME Type Not Determined**:
   - Raised if the file's MIME type cannot be detected.
   - Exception: `ValueError`

   ```python
   ValueError: Could not determine the MIME type for file: /path/to/unknown.file
   ```

3. **API Request Error**:
   - Raised if the API returns an error (e.g., invalid access token, unsupported file type).


---
## Retrieve Media URL by Media ID

The `get_media_url` method is used to retrieve the URL of a media file from the Meta API by providing a media ID. This media ID is obtained after uploading the media using the WhatsApp Business API. Media URLs will expire after 5 minutes, you need to retrieve the media URL again if it expires. If you click the URL from a browser, you will get an access error. You can download media content from the [Media Download](#media-download) method.

---

### Method Signature
```python
get_media_url(media_id: str) -> dict
```

---

### Parameters
- `media_id` (str): The unique identifier for the media file. This ID is provided by the API when you upload media using the [upload media method](#upload-media).

---

### Returns
A dictionary containing the metadata and URL of the media file. The structure of the response is as follows:
```json
{
    "messaging_product": "whatsapp",
    "url": "<URL>",
    "mime_type": "image/jpeg",
    "sha256": "<HASH>",
    "file_size": "303833",
    "id": "2621233374848975"
}
```

- `messaging_product` *(str)*: Indicates the messaging platform, always set to `"whatsapp"`.
- `url` *(str)*: The URL of the media file that can be used to download it.
- `mime_type` *(str)*: The MIME type of the media file (e.g., `"image/jpeg"` for an image).
- `sha256` *(str)*: The SHA-256 hash of the media file, useful for verifying file integrity.
- `file_size` *(str)*: The size of the media file in bytes.
- `id` *(str)*: The unique identifier of the media file.

---

### Exceptions
The method raises an `Exception` if the API request fails. This includes cases such as:
- Invalid `media_id`
- Unauthorized access due to invalid or expired access tokens
- API errors (e.g., rate limiting, server issues)

---

### Example Usage
```python
from whatsapp_api.media.media_client import MediaClient

access_token = "your_meta_api_access_token"
phone_number_id = "your_phone_number_id"

media_client = MediaClient(access_token, phone_number_id)

# Retrieve media URL
media_id = "2621233374848975"
try:
    media_url = media_client.get_media_url(media_id)
    print(f"Media URL: {media_url}")
except Exception as e:
    print(f"Failed to retrieve media URL: {e}")
```

---

## Retrieve Media Content by Media URL

Use the `get_media_content` method to fetch the binary media content from a media URL. This URL is typically obtained via [`get_media_url`](#retrieve-media-url-by-media-id) and expires after **5 minutes**, so fetch promptly or re-request if needed.
Pass the full media URL returned by the API—no additional base URL is required.

---

### Method Signature
```python
get_media_content(media_url: str) -> MediaResponse
```

---

### Parameters
- `media_url` *(str)*: The temporary media URL returned by `get_media_url`.

---

### Returns
`MediaResponse` with:
- `content` (`bytes`): Raw media bytes.
- `content_type` (`str`): MIME type returned by the server.

---

### Example Usage
```python
from whatsapp_api.media.media_client import MediaClient

access_token = "your_meta_api_access_token"
phone_number_id = "your_phone_number_id"

media_client = MediaClient(access_token, phone_number_id)

# 1) Retrieve the short-lived media URL
media_id = "2621233374848975"
media_meta = media_client.get_media_url(media_id)
media_url = media_meta["url"]

# 2) Fetch the media content and content type
media_response = media_client.get_media_content(media_url)
content_bytes = media_response.content
content_type = media_response.content_type

# Optional: save to a file
with open("downloaded_media", "wb") as file:
    file.write(content_bytes)
```

---

### Related Methods
- [`get_media_url`](#retrieve-media-url-by-media-id) – Get the URL used as input here.
- [`download_media`](#download-media) – Alias with the same behavior as `get_media_content`.

---

---

### Delete Media by Media ID

The `delete_media` method is used to delete a media file from the Meta API by providing a media ID. This media ID is obtained after uploading the media using the WhatsApp Business API. Once deleted, the media file will no longer be accessible.

---

### Method Signature
```python
delete_media(media_id: str) -> bool
```

---

### Parameters
- `media_id` (str): The unique identifier for the media file. This ID is provided by the API when you upload media using the [upload media method](#upload-media).

---

### Returns
A boolean value indicating whether the media was successfully deleted.

- `True`: The media was deleted successfully.
- `False`: The media deletion failed.

---

### Exceptions
The method raises an `Exception` if the API request fails. This includes cases such as:
- Invalid `media_id`
- Unauthorized access due to invalid or expired access tokens
- API errors (e.g., rate limiting, server issues)

---

### Example Usage
```python
from whatsapp_api.media.media_client import MediaClient

access_token = "your_meta_api_access_token"
phone_number_id = "your_phone_number_id"

media_client = MediaClient(access_token, phone_number_id)

# Delete media
media_id = "2621233374848975"
try:
    success = media_client.delete_media(media_id)
    if success:
        print("Media deleted successfully.")
    else:
        print("Failed to delete media.")
except Exception as e:
    print(f"Failed to delete media: {e}")
```

---
## Download Media

The `download_media` method is used to download media files from a given URL retrieved through the [Retrieve Media URL](#retrieve-media-url-by-media-id) method. Since media URLs expire after **5 minutes**, you may need to retrieve a fresh URL if downloading fails due to expiration. This is a convenience alias for [`get_media_content`](#retrieve-media-content-by-media-url) and returns the same binary data.
Pass the absolute media URL returned by the API; the client will request it directly.

### Method Signature
```python
download_media(media_url: str) -> MediaResponse
```

---

### Parameters
- `media_url` *(str)*: The temporary URL of the media file. This URL is retrieved via the [`get_media_url`](#retrieve-media-url-by-media-id) method.

---

### Returns
`MediaResponse` containing:
- `content` (`bytes`): Raw media bytes.
- `content_type` (`str`): MIME type returned by the server.
Functionally identical to `get_media_content`.

Upon a successful request, the media content is returned as raw binary data. You can save this data to a file or process it further.

---


### Example Usage
```python
from whatsapp_api.media.media_client import MediaClient

access_token = "your_meta_api_access_token"
phone_number_id = "your_phone_number_id"

media_client = MediaClient(access_token, phone_number_id)
media_meta = media_client.get_media_url("2621233374848975")
media_url = media_meta["url"]
download = media_client.download_media(media_url)
content_bytes = download.content
content_type = download.content_type

```

---

### Handling Expired Media URLs
Since **media URLs expire after 5 minutes**, follow this approach:

1. **Retrieve the media URL using `get_media_url(media_id)`**.
2. **Immediately download the media file using `get_media_content(media_url)` or `download_media(media_url)`**.
3. **If you get a `404 Not Found` error, retrieve a new media URL and try again.**
---

### Related Methods
- [`get_media_url`](#retrieve-media-url-by-media-id) – Retrieve the media URL before downloading.
- [`get_media_content`](#retrieve-media-content-by-media-url) – Alias with the same behavior as `download_media`.

---


## Sending Media Message by ID

The `send_media_message_by_id` method is used to send various types of media messages (e.g., images, videos, documents, audio, stickers) to a recipient using a media ID obtained from the [upload media method](#upload-media).

### Method Signature
```python
send_media_message_by_id(
    recipient_phone_number: str,
    media_id: str,
    media_type: str,
    context_message_id: Optional[str] = None,
    **kwargs
) -> dict
```

---

## Parameters
- **`recipient_phone_number`** *(str)*: The recipient's WhatsApp phone number in international format (e.g., `1234567890`, without the `+`).
- **`media_id`** *(str)*: The unique media ID of the media to be sent. This ID is obtained after uploading the media to the [upload media method](#upload-media).
- **`media_type`** *(str)*: The type of media to be sent. Supported types:
  - `image`
  - `audio`
  - `document`
  - `sticker`
  - `video`
- **`context_message_id`** *(str, optional)*: The message ID of the previous message, if you are sending the media as a reply. Default is `None`.
- **`kwargs`** *(optional)*: Additional fields based on the media type:
  - **`caption`** *(str)*: A caption for the media (only applicable for `image`, `video`, and `document`). Default is `None`.
  - **`filename`** *(str)*: The filename for the document (only applicable for `document`). Default is `None`.

---

### Returns
A dictionary containing the response from the WhatsApp Business API, including the `message ID` for tracking.

---

### Supported Media Types and Payload Structure
| Media Type  | Additional Fields |
|-------------|-------------------|
| `audio`     | None              |
| `sticker`   | None              |
| `image`     | `caption`         |
| `document`  | `caption`, `filename`|
| `video`     | `caption`         |
---

### Example: Sending an Image
```python
recipient_phone_number = "1234567890"
media_id = "image_media_id"

# Send an image
response = media_client.send_media_message_by_id(
    recipient_phone_number=recipient_phone_number,
    media_id=media_id,
    media_type="image",
    caption="This is an image!" # Optional
)
print("Response:", response)
```

---

### Example: Sending a Document
```python
recipient_phone_number = "1234567890"
media_id = "document_media_id"

# Send a document with a caption and filename
response = media_client.send_media_message_by_id(
    recipient_phone_number=recipient_phone_number,
    media_id=media_id,
    media_type="document",
    caption="Here is your document", # Optional
    filename="example.pdf" # Optional
)
print("Response:", response)
```

---

### Example: Sending an Audio File
```python
recipient_phone_number = "1234567890"
media_id = "audio_media_id"

# Send an audio file
response = media_client.send_media_message_by_id(
    recipient_phone_number=recipient_phone_number,
    media_id=media_id,
    media_type="audio"
)
print("Response:", response)
```

---

### Example: Sending a Sticker
```python
recipient_phone_number = "1234567890"
media_id = "sticker_media_id"

# Send a sticker
response = media_client.send_media_message_by_id(
    recipient_phone_number=recipient_phone_number,
    media_id=media_id,
    media_type="sticker"
)
print("Response:", response)
```

---

### Error Handling
1. **Invalid Media Type**:
   - If an unsupported `media_type` is provided, a `ValueError` is raised with the message:
     ```
     Unsupported media type: <media_type>. Supported types are: image, audio, document, sticker, video.
     ```

2. **Invalid Caption**:
   - If `caption` is used with unsupported media types (`audio` or `sticker`), a `ValueError` is raised with the message:
     ```
     Caption is not allowed for media type: <media_type>.
     ```

3. **General API Errors**:
   - If the API request fails (e.g., due to an invalid `media_id`, `recipient_phone_number`, `context_message_id`, or authentication issues), an `Exception` is raised with the HTTP status code and error message.

---

## Sending Media Message by URL

The `send_media_message_by_url` method is used to send various types of media messages (e.g., images, videos, documents, audio, stickers) to a recipient using a media URL.

### Method Signature
```python
send_media_message_by_url(
    recipient_phone_number: str,
    media_url: str,
    media_type: str,
    context_message_id: Optional[str] = None,
    **kwargs
) -> dict
```

---

### Parameters
- **`recipient_phone_number`** *(str)*: The recipient's WhatsApp phone number in international format (e.g., `1234567890`, without the `+`).
- **`media_url`** *(str)*: The URL of the media to be sent.
- **`media_type`** *(str)*: The type of media to be sent. Supported types:
  - `image`
  - `audio`
  - `document`
  - `sticker`
  - `video`
- **`context_message_id`** *(str, optional)*: The message ID of the previous message, if you are sending the media as a reply. Default is `None`.
- **`kwargs`** *(optional)*: Additional fields based on the media type:
  - **`caption`** *(str)*: A caption for the media (only applicable for `image`, `video`, and `document`). Default is `None`.
  - **`filename`** *(str)*: The filename for the document (only applicable for `document`). Default is `None`.

---

### Returns
A dictionary containing the response from the WhatsApp Business API, including the `message ID` for tracking.

---

### Supported Media Types and Payload Structure
| Media Type  | Additional Fields |
|-------------|-------------------|
| `audio`     | None              |
| `sticker`   | None              |
| `image`     | `caption`         |
| `document`  | `caption`         |
| `video`     | `caption`         |

---

### Example: Sending an Image from a URL
```python
recipient_phone_number = "1234567890"
media_url = "https://example.com/media/image.jpg"

# Send an image
response = media_client.send_media_message_by_url(
    recipient_phone_number=recipient_phone_number,
    media_url=media_url,
    media_type="image"
)
print("Response:", response)
```

---

### Example: Sending a Document from a URL
```python
recipient_phone_number = "1234567890"
media_url = "https://example.com/media/document.pdf"

# Send a document
response = media_client.send_media_message_by_url(
    recipient_phone_number=recipient_phone_number,
    media_url=media_url,
    media_type="document",
    caption="Here is the document you requested."
)
print("Response:", response)
```

---

### Notes
- The `media_url` must be a publicly accessible URL.
- Media types such as `audio`, `sticker`, `image`, `document`, and `video` are supported.
- If a `context_message_id` is provided, the media message will be sent as a reply to that specific message.

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
