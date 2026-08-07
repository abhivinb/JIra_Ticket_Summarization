class Prompts:

    VISION_PROMPT = """
You are an experienced Software Support ADAS Engineer.

Analyse the Jira ticket.

Description:
{description}

Comments:
{comments}

Analyse every attached screenshot carefully.

Tasks

1. Read every visible text.

2. Detect error messages.

3. Detect warnings.

4. Analyse graphs.

5. Detect trends.

6. Detect UI problems.

7. Detect stack traces.

8. Mention important observations.

Return JSON.

{{
 "observations":[],
 "errors":[],
 "graph_findings":[],
 "ocr_text":""
}}

Return ONLY JSON.
"""

    SUMMARY_PROMPT = """
You are an experienced Software Support ADAS Engineer.

You are provided with:

Description
----------------
{description}

Comments
----------------
{comments}

Vision Observations
----------------
{observations}

Detected Errors
----------------
{errors}

Graph Analysis
----------------
{graphs}

OCR Text
----------------
{ocr}

Generate a JSON response only.

{{
    "executive_summary": "...",
    "key_findings": "..."
}}

Do not return markdown.

Do not return explanations.

Return only JSON.
"""
