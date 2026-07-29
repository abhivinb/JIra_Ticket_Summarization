from dataclasses import dataclass, field
from typing import List


@dataclass
class Ticket:

    ticket_id: str

    summary: str

    description: str

    comments: List[str] = field(default_factory=list)

    attachments: List[str] = field(default_factory=list)