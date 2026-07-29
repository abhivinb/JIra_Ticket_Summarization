"""
pipeline/summarization_pipeline.py

Main orchestration pipeline.
"""

from models.summary import Summary
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
        ticket_id: str,
        post_to_jira: bool = True
    ) -> Summary:

        logger.info(
            "=" * 60
        )

        logger.info(
            "Pipeline Started : %s",
            ticket_id
        )

        ticket = get_dummy_ticket()  #dummy data

        #actual data
        # ticket = self.jira.get_issue(
        #     ticket_id
        # )

        logger.info(
            "Ticket fetched successfully."
        )

        images = ticket.attachments #dummy data

        #actual data
        # images = self.jira.download_attachments(   
        #     ticket
        # )

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

        comment = self._build_comment(
            summary
        )

        # if post_to_jira:
        #     self.jira.add_comment(

        #         issue_key=ticket.ticket_id,

        #         comment=comment

        #     )

        logger.info(
            "Comment posted."
        )

        logger.info(
            "Pipeline Finished."
        )

        return summary    

        # --------------------------------------------------

    @staticmethod
    def _build_comment(
        summary: Summary
    ) -> str:

        return f"""
        🤖 AI Generated Summary

        Executive Summary
        ------------------------

        {summary.executive_summary}

        Key Findings
        ------------------------

        {summary.key_findings}

        Recommendations
        ------------------------

        {summary.recommendations}
        """
        # --------------------------------------------------

    def shutdown(self):

        self.jira.close()