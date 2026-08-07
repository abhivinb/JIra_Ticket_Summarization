"""
pipeline/summarization_pipeline.py

Main orchestration pipeline.
"""

from models.summary import Summary
from config.settings import Settings
from services.jira_service import JiraService
from services.vision_service import VisionService
from services.summary_service import SummaryService
from utils.logger import logger
from models.vision_results import VisionResult
from mock_data import get_dummy_ticket


class SummarizationPipeline:

    def __init__(self):

        self.jira = JiraService()

        self.vision = VisionService()

        self.summary = SummaryService()

        # --------------------------------------------------

    def run(
        self,
        ticket_id: str
    ) -> Summary:

        logger.info(
            "=" * 60
        )

        logger.info(
            "Pipeline Started : %s",
            ticket_id
        )

        if Settings.USE_MOCK_DATA:

            ticket = get_dummy_ticket()

        else:

            ticket = self.jira.get_issue(
                ticket_id
            )

        logger.info(
            "Ticket fetched successfully."
        )

        if Settings.USE_MOCK_DATA:

            images = ticket.attachments

        else:

            images = self.jira.download_attachments(
                ticket
            )

        logger.info(
            "%d images downloaded.",
            len(images)
        )

        if images:

            vision_result = self.vision.analyze(

                ticket=ticket,

                image_paths=images

            )

        else:
            vision_result = VisionResult(

                observations=[],
                errors=[],
                graph_findings=[],
                ocr_text=""

            )

        logger.info(
            "Vision analysis completed."
        )

        summary = self.summary.generate(

            ticket,

            vision_result

        )

        logger.info(
            "Summary generated."
        )

        logger.info(
            "Pipeline Finished."
        )

        return summary

        # --------------------------------------------------

    def shutdown(self):

        self.jira.close()
