"""
Application Settings

Loads all environment variables.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:

    # -----------------------------
    # OpenAI
    # -----------------------------

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    OPENAI_MODEL = os.getenv(
        "OPENAI_MODEL",
        "gpt-4.1"
    )

    # -----------------------------
    # Jira
    # -----------------------------

    JIRA_BASE_URL = os.getenv(
        "JIRA_BASE_URL",
        ""
    )

    JIRA_EMAIL = os.getenv(
        "JIRA_EMAIL",
        ""
    )

    JIRA_API_TOKEN = os.getenv(
        "JIRA_API_TOKEN",
        ""
    )

    # -----------------------------
    # Downloads
    # -----------------------------

    DOWNLOAD_FOLDER = os.getenv(
        "DOWNLOAD_FOLDER",
        "downloads"
    )

    # -----------------------------
    # Validation
    # -----------------------------

    @classmethod
    def validate(cls):

        missing = []

        if not cls.OPENAI_API_KEY:
            missing.append("OPENAI_API_KEY")

        if not cls.JIRA_BASE_URL:
            missing.append("JIRA_BASE_URL")

        if not cls.JIRA_EMAIL:
            missing.append("JIRA_EMAIL")

        if not cls.JIRA_API_TOKEN:
            missing.append("JIRA_API_TOKEN")

        if missing:

            raise ValueError(

                "Missing Environment Variables:\n"

                + "\n".join(missing)

            )
        