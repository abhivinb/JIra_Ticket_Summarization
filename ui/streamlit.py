import sys

import streamlit as st

from config.settings import Settings
from pipeline.summarization_pipeline import SummarizationPipeline
from utils.logger import logger


def log_startup():

    logger.info("Application Started")

    logger.info(
        "Python Version: %s",
        sys.version.split()[0]
    )

    logger.info(
        "Environment: %s",
        Settings.ENVIRONMENT
    )

    logger.info(
        "Mock Mode: %s",
        Settings.USE_MOCK_DATA
    )

    logger.info(
        "OpenAI Model: %s",
        Settings.OPENAI_MODEL
    )

st.set_page_config(

    page_title="Jira Ticket Summarizer",

    page_icon="🤖",

    layout="wide"

)

st.title("🤖 Jira Ticket Summarizer")

st.write(
    "Generate AI summaries for Jira tickets."
)

try:

    Settings.validate()

    log_startup()

except ValueError as ex:

    logger.error(
        "Application startup validation failed: %s",
        ex
    )

    st.error(
        "Application configuration is incomplete. Please check the required environment variables."
    )

    st.info(str(ex))

    st.stop()

ticket_id = st.text_input(

    "Enter Jira Ticket ID",

    placeholder="ABC-123"

)

generate = st.button(
    "Generate Summary"
)

if generate:

    if not ticket_id.strip():

        st.warning(
            "Please enter a ticket ID."
        )

        st.stop()

    pipeline = SummarizationPipeline()

    with st.spinner(

        "Generating summary..."

    ):

        try:

            summary = pipeline.run(
                ticket_id
            )

        except Exception as ex:

            logger.exception(ex)

            st.error(str(ex))

            st.stop()

    st.success(
        "Summary Generated Successfully."
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

    pipeline.shutdown()
