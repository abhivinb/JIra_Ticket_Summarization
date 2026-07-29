"""
services/vision_service.py

Vision analysis service using OpenAI Responses API.
"""

from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import List

from openai import OpenAIError

from clients.openai_client import OpenAIClient
from config.prompts import Prompts
from config.settings import Settings
from models.ticket import Ticket
from models.vision_results import VisionResult
from utils.exceptions import VisionAnalysisError
from utils.logger import logger
from utils.helper import clean_json


class VisionService:

    def __init__(self) -> None:

        self.client = OpenAIClient.get_client()

    # --------------------------------------------------

    @staticmethod
    def _encode_image(image_path: Path) -> str:

        with image_path.open("rb") as image:

            return base64.b64encode(
                image.read()
            ).decode("utf-8")

    # --------------------------------------------------

    @staticmethod
    def _build_prompt(ticket: Ticket) -> str:

        comments = (
                    "\n".join(ticket.comments)
                    if ticket.comments
                    else "No comments available."
                )

        return Prompts.VISION_PROMPT.format(
            description=ticket.description,
            comments=comments
        )

    # --------------------------------------------------

    def analyze(
        self,
        ticket: Ticket,
        image_paths: List[Path]
    ) -> VisionResult:

        logger.info(
            "Starting vision analysis for %s",
            ticket.ticket_id
        )

        prompt = self._build_prompt(ticket)

        content = [
            {
                "type": "input_text",
                "text": prompt
            }
        ]

        for image in image_paths:

            encoded = self._encode_image(image)

            content.append(
                {
                    "type": "input_image",
                    "image_url":
                        f"data:image/png;base64,{encoded}"
                }
            )

        try:

            response = self.client.responses.create(

                model=Settings.OPENAI_MODEL,

                input=[
                    {
                        "role": "user",
                        "content": content
                    }
                ]

            )

            result = response.output_text

            logger.info(
                "Vision response received."
            )

            return self._parse_response(result)

        except OpenAIError as ex:

            logger.exception(ex)

            raise VisionAnalysisError(
                "Vision analysis failed."
            ) from ex

    def _parse_response(
        self,
        response_text: str
    ) -> VisionResult:

        try:

            response_text = clean_json(response_text)
            data = json.loads(response_text)
            
            return VisionResult(

                observations=data.get(
                    "observations",
                    []
                ),

                errors=data.get(
                    "errors",
                    []
                ),

                graph_findings=data.get(
                    "graph_findings",
                    []
                ),

                ocr_text=data.get(
                    "ocr_text",
                    ""
                )

            )

        except Exception as ex:

            logger.exception(ex)

            raise VisionAnalysisError(
                "Invalid JSON returned by OpenAI."
            ) from ex