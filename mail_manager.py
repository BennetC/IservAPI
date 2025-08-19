import json
import os

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

    def fetch_drafts(self, title=""):
        inbox_encoded = "SU5CT1gvRHJhZnRz" # Base64 encoded value for "INBOX/Drafts"
        api_url = f"{self.mail_api}/message?mailbox[]={inbox_encoded}&limit=25&offset=0&sort=date&order=desc"

        headers = self.headers
        headers["X-ISERV-CSRF-PROTECTION"] = "yes pls"
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            response = response.json()
            inbox = response.get("items", [])

            if title:
                draft = next((item for item in inbox if item.get("subject") == title), None)
                if draft:
                    return draft

            return inbox

        else:
            return {"error": "Failed to fetch drafts", "status_code": response.status_code, "message": response.text}