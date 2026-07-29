from dataclasses import dataclass
from typing import List


@dataclass
class VisionResult:

    observations: List[str]

    errors: List[str]

    graph_findings: List[str]

    ocr_text: str