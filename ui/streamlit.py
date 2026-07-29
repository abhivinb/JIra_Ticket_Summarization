import streamlit as st

from pipeline.summarization_pipeline import SummarizationPipeline
from utils.logger import logger

st.set_page_config(

    page_title="Jira Ticket Summarizer",

    page_icon="🤖",

    layout="wide"

)

st.title("🤖 Jira Ticket Summarizer")

st.write(
    "Generate AI summaries for Jira tickets."
)

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

    st.subheader(
        "Recommendations"
    )

    st.write(
        summary.recommendations
    )

    pipeline.shutdown()