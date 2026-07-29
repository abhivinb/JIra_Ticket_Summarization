"""
jira_service.py

Responsible for:

- Jira Authentication
- Fetch Issue Details
- Parse Description
- Parse Comments
- Collect Attachments
- Download Attachments
"""
import mimetypes
import shutil

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config.settings import Settings
from models.ticket import Ticket
from utils.adf_parser import ADFParser
from utils.logger import logger
from utils.exceptions import JiraConnectionError
from config.settings import Settings


class JiraService:

    def __init__(self) -> None:

        self.base_url = Settings.JIRA_BASE_URL.rstrip("/")
        self.parser = ADFParser()

        self.session = requests.Session()

        self.session.auth = (
            Settings.JIRA_EMAIL,
            Settings.JIRA_API_TOKEN
        )

        self.session.headers.update(
            {
                "Accept": "application/json"
            }
        )

        retry_strategy = Retry(
            total=3,
            backoff_factor=2,
            status_forcelist=[
                429,
                500,
                502,
                503,
                504
            ],
            allowed_methods=[
                "GET",
                "POST"
            ]
        )

        adapter = HTTPAdapter(
            max_retries=retry_strategy
        )

        self.session.mount(
            "https://",
            adapter
        )

        self.session.mount(
            "http://",
            adapter
        )

    # --------------------------------------------------

    def get_issue(
        self,
        issue_key: str
    ) -> Ticket:

        logger.info(
            "Fetching Jira issue %s",
            issue_key
        )

        endpoint = (
            f"{self.base_url}/rest/api/3/issue/{issue_key}"
        )

        params = {
            "fields":
                "summary,description,comment,attachment"
        }

        response = self.session.get(
            endpoint,
            params=params,
            timeout=30
        )

        if response.status_code != 200:

            raise JiraConnectionError(
                f"Unable to fetch ticket. "
                f"Status={response.status_code}"
            )

        issue = response.json()

        return self._build_ticket(issue)

    # --------------------------------------------------

    def _build_ticket(
        self,
        issue: dict
    ) -> Ticket:

        fields = issue["fields"]

        description = self._parse_description(
            fields.get("description")
        )

        comments = self._parse_comments(
            fields.get("comment", {})
        )

        attachments = self._collect_attachments(
            fields.get("attachment", [])
        )

        return Ticket(
            ticket_id=issue["key"],
            summary=fields.get("summary", ""),
            description=description,
            comments=comments,
            attachments=attachments
        )

    # --------------------------------------------------

    def _parse_description(
        self,
        description
    ) -> str:

        if not description:
            return ""

        return self.parser.parse(
            description
        )

    # --------------------------------------------------

    def _parse_comments(
        self,
        comment_block
    ) -> List[str]:

        comments = []

        values = comment_block.get(
            "comments",
            []
        )

        for comment in values:

            body = comment.get("body")

            text = self.parser.parse(body)

            if text.strip():

                comments.append(text)

        return comments

    # --------------------------------------------------

    def _collect_attachments(
        self,
        attachments
    ) -> List[str]:

        urls = []

        for attachment in attachments:

            mime = attachment.get(
                "mimeType",
                ""
            )

            if mime.startswith("image/"):

                urls.append(
                    attachment["content"]
                )

        return urls




    # --------------------------------------------------

    def download_attachments(
        self,
        ticket: Ticket,
        download_dir: str = Settings.DOWNLOAD_FOLDER
    ) -> List[Path]:
        """
        Download all image attachments for a ticket.

        Returns:
            List[Path]: Downloaded image file paths.
        """

        download_path = Path(download_dir)
        download_path.mkdir(
            parents=True,
            exist_ok=True
        )

        downloaded_files: List[Path] = []

        for index, url in enumerate(ticket.attachments, start=1):

            try:

                logger.info(
                    "Downloading attachment %s",
                    url
                )

                response = self.session.get(
                    url,
                    stream=True,
                    timeout=60
                )

                response.raise_for_status()

                content_type = response.headers.get(
                    "Content-Type",
                    ""
                )

                if not content_type.startswith("image/"):

                    logger.warning(
                        "Skipping non-image attachment: %s",
                        url
                    )

                    continue

                extension = mimetypes.guess_extension(
                    content_type
                )

                if extension is None:
                    extension = ".png"

                filename = (
                    f"{ticket.ticket_id}_{index}{extension}"
                )

                destination = (
                    download_path / filename
                )

                with open(destination, "wb") as file:

                    shutil.copyfileobj(
                        response.raw,
                        file
                    )

                downloaded_files.append(destination)

                logger.info(
                    "Saved %s",
                    destination
                )

            except Exception as ex:

                logger.exception(ex)

        return downloaded_files

    # --------------------------------------------------

    def add_comment(
        self,
        issue_key: str,
        comment: str
    ) -> None:
        """
        Add generated summary back to Jira.
        """

        endpoint = (
            f"{self.base_url}/rest/api/3/issue/"
            f"{issue_key}/comment"
        )

        payload = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": comment
                            }
                        ]
                    }
                ]
            }
        }

        response = self.session.post(
            endpoint,
            json=payload,
            timeout=30
        )

        if response.status_code not in (200, 201):

            raise JiraConnectionError(
                "Unable to add Jira comment."
            )

        logger.info(
            "Summary added to Jira ticket %s",
            issue_key
        )

    # --------------------------------------------------

    def verify_connection(self) -> bool:
        """
        Verify Jira credentials.
        """

        endpoint = (
            f"{self.base_url}/rest/api/3/myself"
        )

        response = self.session.get(
            endpoint,
            timeout=20
        )

        return response.status_code == 200

    # --------------------------------------------------

    def close(self):

        self.session.close()

        logger.info(
            "Jira session closed."
        )