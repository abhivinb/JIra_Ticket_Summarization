"""
Application Entry Point

Run using:

streamlit run app.py
"""

import streamlit as st

from pipeline.summarization_pipeline import SummarizationPipeline
from utils.logger import logger


def main():

    st.set_page_config(

        page_title="Jira Ticket Summarizer",

        page_icon="🤖",

        layout="wide"

    )

    st.title("🤖 Jira Ticket Summarizer")

    st.markdown(
        "Generate AI-powered summaries for Jira tickets."
    )

    ticket_id = st.text_input(

        "Enter Jira Ticket ID",

        placeholder="ABC-123"

    )

    if st.button("Generate Summary"):

        if not ticket_id.strip():

            st.warning(
                "Please enter a Jira Ticket ID."
            )

            return

        pipeline = None

        try:

            pipeline = SummarizationPipeline()

            with st.spinner(
                "Analyzing ticket..."
            ):

                summary = pipeline.run(
                    ticket_id=ticket_id
                )

            st.success(
                "Summary generated successfully."
            )

            st.subheader(
                "Executive Summary"
            )

            st.write(
                summary.executive_summary
            )

            st.subheader(
                "Key Findings"
            )

            st.write(
                summary.key_findings
            )

            st.subheader(
                "Recommendations"
            )

            st.write(
                summary.recommendations
            )

        except Exception as ex:

            logger.exception(ex)

            st.error(str(ex))

        finally:

            if pipeline is not None:

                pipeline.shutdown()


if __name__ == "__main__":

    main()
