"""
OpenAI Client Singleton

This module creates and returns a single OpenAI client
instance that will be reused across the application.
"""

from openai import OpenAI
from config.settings import Settings


class OpenAIClient:

    _client = None

    @classmethod
    def get_client(cls):

        if cls._client is None:

            cls._client = OpenAI(
                api_key=Settings.OPENAI_API_KEY
            )

        return cls._client