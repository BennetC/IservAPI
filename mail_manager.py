import json
import os
import base64

import requests

from draft_id import generate_draft_id


class IservAPI:
    def __init__(self, cookies, account, school_url):
        self.base_url = f"{school_url}/iserv"
        self.account_id = account

        # Handle cookies as either a JSON string or a file path
        if os.path.isfile(cookies):
            # If cookies is a file path, read the file
            with open(cookies, 'r') as f:
                self.cookies_dict = json.load(f)
        else:
            # Otherwise, treat it as a JSON string
            try:
                self.cookies_dict = json.loads(cookies)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON string provided for cookies. Please provide a valid JSON string or file path.")

        # Format cookies as a string for HTTP headers
        self.cookies_str = '; '.join(f"{k}={v}" for k, v in self.cookies_dict.items())

        self.mail_api = f"{self.base_url}/mail/api/v2/account/{account}"

        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Cookie": self.cookies_str,
            "Origin": "https://iserv-gis.de"
        }

    def create_draft(
            self,
            subject,
            body,
            cc,
            to
    ):
        api_url = f"{self.mail_api}/draft"
        headers = self.headers
        headers["X-ISERV-CSRF-PROTECTION"] = "yes pls"

        account_name = self.account_id.split('@')[0].split(".")
        first_name = account_name[0].capitalize()
        last_name = account_name[-1].capitalize()

        draft_id = generate_draft_id(self.account_id)

        request = {
            "attachments": [],
            "bcc": [],
            "cc": cc if isinstance(cc, list) else [cc],
            "context": None,
            "draftId": draft_id,
            "dsn": False,
            "from": f"{first_name} {last_name} <{self.account_id}>",
            "mdn": False,
            "plain": body,
            "rich": None,
            "subject": subject,
            "to": to if isinstance(to, list) else [to],
        }

        response = requests.post(api_url, headers=headers, json=request)

        return response, draft_id

    def send_mail(
            self,
            subject,
            body,
            cc,
            to
    ):
        headers = self.headers
        headers["X-ISERV-CSRF-PROTECTION"] = "yes pls"

        _, draft_id = self.create_draft(
            subject,
            body,
            cc,
            to
        )

        draft = self.fetch_drafts(title=subject)
        message_id = draft.get("messageId")

        if not message_id:
            raise ValueError("Draft creation failed, no messageId returned.")

        api_url = f"{self.mail_api}/draft/{message_id}/send"

        response = requests.post(api_url, headers=headers)

        return response

    def fetch_drafts(self, title="", limit=25, offset=0):
        return self.fetch_mailbox(title=title, inbox_type="drafts", limit=limit, offset=offset)

    def fetch_sent(self, title="", limit=25, offset=0):
        return self.fetch_mailbox(title=title, inbox_type="sent", limit=limit, offset=offset)

    def fetch_received(self, title="", limit=25, offset=0):
        return self.fetch_mailbox(title=title, inbox_type="received", limit=limit, offset=offset)

    def fetch_trash(self, title="", limit=25, offset=0):
        return self.fetch_mailbox(title=title, inbox_type="trash", limit=limit, offset=offset)

    def fetch_unwanted(self, title="", limit=25, offset=0):
        return self.fetch_mailbox(title=title, inbox_type="unwanted", limit=limit, offset=offset)

    def fetch_archive(self, title="", limit=25, offset=0):
        return self.fetch_mailbox(title=title, inbox_type="archive", limit=limit, offset=offset)

    def fetch_mailbox(self, title="", inbox_type="received", limit=25, offset=0):
        inbox_types = {
            "received": "INBOX",
            "sent": "INBOX/Sent",
            "drafts": "INBOX/Drafts",
            "trash": "INBOX/Trash",
            "unwanted": "INBOX/Junk",
            "archive": "INBOX/Archive"
        }

        inbox_name = inbox_types.get(inbox_type.lower())
        if not inbox_name:
            raise ValueError(f"Invalid inbox type: {inbox_type}")

        encoded_inbox = base64.b64encode(inbox_name.encode('utf-8')).decode('utf-8')

        api_url = f"{self.mail_api}/message?mailbox[]={encoded_inbox}&limit={limit}&offset={offset}&sort=date&order=desc"

        headers = self.headers
        headers["X-ISERV-CSRF-PROTECTION"] = "yes pls"
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            response = response.json()
            if title:
                # Filter results by title if provided
                drafts = [item for item in response.get("items", []) if title.lower() == item.get("subject", "").lower()]
                return drafts
            else:
                return response.get("items", [])
        else:
            return {"error": "Failed to fetch mailbox", "status_code": response.status_code, "message": response.text}


if __name__ == "__main__":
    account = "bennet.collins@iserv-gis.de"
    cookies = "cookies.json"
    school_url = "https://iserv-gis.de"
    iserv_api = IservAPI(cookies, account, school_url)
    mails = iserv_api.fetch_mailbox(inbox_type="received")
