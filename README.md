# IServ Mail Manager

A Python library for interacting with IServ school management system's email API. This tool allows you to programmatically send emails, create drafts, and manage mail through IServ's web interface.

## Features

- **Send Emails**: Compose and send emails directly through IServ
- **Draft Management**: Create and fetch email drafts
- **Multi-recipient Support**: Send to multiple recipients with CC support
- **Automatic Message ID Generation**: Generates RFC-compliant message IDs
- **Cookie-based Authentication**: Uses browser cookies for secure API access

## Installation

1. Clone this repository or download the files
2. Install required dependencies:
```bash
pip install requests
```

## Cookie Setup

To use this library, you need to extract cookies from your browser after logging into IServ:

### Method 1: Browser Developer Tools
1. Log into your IServ account in your browser
2. Open Developer Tools (F12)
3. Go to the Network tab and refresh the page
4. Find any request to your IServ domain
5. Copy the `Cookie` header value
6. Save it as a JSON object in a file (e.g., `cookies.json`):

```json
{
  "session_id": "your_session_value",
  "csrf_token": "your_csrf_value",
  "other_cookie": "other_value"
}
```

### Method 2: Browser Extensions
Use browser extensions like "Cookie Editor" to export cookies in JSON format.

## Usage

```python
from mail_manager import IservAPI

# Initialize with cookies file
api = IservAPI(
    cookies="cookies.json",  # Path to cookies file or JSON string
    account="your.name@school.domain",
    school_url="https://your-school.iserv-portal.de"
)

# Send an email
response = api.send_mail(
    subject="Test Subject",
    body="This is the email body",
    to=["recipient@example.com"],
    cc=["cc@example.com"]  # Optional
)

# Create a draft (without sending)
response, draft_id = api.create_draft(
    subject="Draft Subject",
    body="Draft content",
    to=["recipient@example.com"],
    cc=[]
)

# Fetch all drafts
drafts = api.fetch_drafts()

# Fetch specific draft by subject
specific_draft = api.fetch_drafts(title="Draft Subject")
```

## Configuration Parameters

- **cookies**: Path to JSON file containing cookies or JSON string
- **account**: Your full IServ email address
- **school_url**: Base URL of your school's IServ installation

## File Structure

```
├── draft_id.py          # Message ID generation utility
├── mail_manager.py      # Main IServ API wrapper class
└── cookies.json         # Your authentication cookies (not included)
```

## Important Notes

- Cookies expire periodically and need to be refreshed
- The library automatically formats sender name from account ID
- All API calls require valid authentication cookies
- Draft IDs are automatically generated using UUID4

## Error Handling

The library includes basic error handling for:
- Invalid email address formats
- Invalid JSON cookie format
- Failed API requests
- Missing draft creation

## Security Considerations

- Store cookies securely and never commit them to version control
- Cookies contain sensitive authentication data
- Consider implementing cookie refresh mechanisms for long-running applications

## Disclaimer

**⚠️ Important Notice:**
- This is **NOT an official IServ API** - it's an unofficial wrapper that interfaces with IServ's internal web API
- Use this library **carefully and responsibly**
- Excessive or improper use may result in account restrictions or violations of your school's usage policies
- Always comply with your institution's IT policies and terms of service
- The authors are not responsible for any misuse or consequences resulting from the use of this library
- This tool is intended for legitimate administrative and educational purposes only

## License

MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.