"""
ADF (Atlassian Document Format) Parser

Converts Jira Cloud rich-text JSON into plain readable text.

Supported nodes

✓ doc
✓ paragraph
✓ text
✓ bulletList
✓ orderedList
✓ listItem
✓ heading
✓ hardBreak
✓ codeBlock
✓ blockquote
✓ panel
✓ table
"""

from typing import Any


class ADFParser:

    def parse(self, adf: Any) -> str:

        if not adf:
            return ""

        if isinstance(adf, str):
            return adf

        result = []

        self._walk(adf, result)

        return "\n".join(
            line.strip()
            for line in result
            if line.strip()
        )

    def _walk(self, node, output):

        if isinstance(node, list):

            for item in node:
                self._walk(item, output)

            return

        if not isinstance(node, dict):
            return

        node_type = node.get("type")

        if node_type == "text":

            output.append(node.get("text", ""))

        elif node_type == "paragraph":

            self._walk(node.get("content", []), output)
            output.append("")

        elif node_type == "heading":

            output.append("\n")

            self._walk(node.get("content", []), output)

            output.append("\n")

        elif node_type == "bulletList":

            self._walk(node.get("content", []), output)

        elif node_type == "orderedList":

            self._walk(node.get("content", []), output)

        elif node_type == "listItem":

            output.append("• ")

            self._walk(node.get("content", []), output)

        elif node_type == "codeBlock":

            output.append("\n```")

            self._walk(node.get("content", []), output)

            output.append("```\n")

        elif node_type == "blockquote":

            output.append("> ")

            self._walk(node.get("content", []), output)

        elif node_type == "panel":

            self._walk(node.get("content", []), output)

        elif node_type == "table":

            self._walk(node.get("content", []), output)

        elif node_type == "tableRow":

            self._walk(node.get("content", []), output)

            output.append("")

        elif node_type == "tableCell":

            self._walk(node.get("content", []), output)

            output.append(" | ")

        elif node_type == "hardBreak":

            output.append("\n")

        else:

            self._walk(node.get("content", []), output)