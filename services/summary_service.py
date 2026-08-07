"""
summary_service.py

Generates the final Jira ticket summary using OpenAI.
"""

from __future__ import annotations

import json

from openai import OpenAIError

from clients.openai_client import OpenAIClient
from config.prompts import Prompts
from config.settings import Settings
from models.summary import Summary
from models.ticket import Ticket
from models.vision_results import VisionResult
from utils.exceptions import SummaryGenerationError
from utils.logger import logger


class SummaryService:

    def __init__(self):

        self.client = OpenAIClient.get_client()

    # --------------------------------------------------

    def generate(
        self,
        ticket: Ticket,
        vision: VisionResult
    ) -> Summary:

        logger.info(
            "Generating summary for %s",
            ticket.ticket_id
        )

        prompt = self._build_prompt(
            ticket,
            vision
        )

        try:

            response = self.client.responses.create(

                model=Settings.OPENAI_MODEL,

                input=prompt

            )

            return self._parse(
                response.output_text
            )

        except OpenAIError as ex:

            logger.exception(ex)

            raise SummaryGenerationError(
                "Summary generation failed."
            ) from ex

        # --------------------------------------------------

    def _build_prompt(
        self,
        ticket: Ticket,
        vision: VisionResult
    ) -> str:

        comments = (
            "\n".join(ticket.comments)
            if ticket.comments
            else "No comments available."
        )

        observations = "\n".join(
            vision.observations
        )

        errors = "\n".join(
            vision.errors
        )

        graphs = "\n".join(
            vision.graph_findings
        )

        return Prompts.SUMMARY_PROMPT.format(

            description = (
                ticket.description
                if ticket.description
                else "No description provided."
            ),

            comments=comments,

            observations=observations,

            errors=errors,

            graphs=graphs,

            ocr=vision.ocr_text

        )

        # --------------------------------------------------

    def _parse(
        self,
        response_text: str
    ) -> Summary:

        try:

            data = json.loads(
                response_text
            )

            return Summary(

                executive_summary=data.get(
                    "executive_summary",
                    ""
                ),

                key_findings=data.get(
                    "key_findings",
                    ""
                )

            )

        except Exception as ex:

            logger.exception(ex)

            raise SummaryGenerationError(
                "Invalid JSON received."
            ) from ex

        
