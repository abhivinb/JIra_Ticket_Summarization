"""
pipeline/summarization_pipeline.py

Main orchestration pipeline.
"""

from models.summary import Summary
from services.jira_service import JiraService
from services.vision_service import VisionService
from services.summary_service import SummaryService
from utils.logger import logger


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

        ticket = self.jira.get_issue(
            ticket_id
        )

        logger.info(
            "Ticket fetched successfully."
        )

        images = self.jira.download_attachments(
            ticket
        )

        logger.info(
            "%d images downloaded.",
            len(images)
        )

        vision_result = self.vision.analyze(

            ticket=ticket,

            image_paths=images

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

        self.jira.add_comment(

            issue_key=ticket.ticket_id,

            comment=comment

        )

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