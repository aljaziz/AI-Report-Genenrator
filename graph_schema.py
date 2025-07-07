from typing_extensions import TypedDict
from typing import List, Annotated
from pydantic import BaseModel, Field
import operator


# Schema for structured output
class Section(BaseModel):
    name: str = Field(description="Name for this section of the report")
    description: str = Field(
        description="Brief Overview of the main topics and concepts of the section"
    )


class Sections(BaseModel):
    sections: List[Section] = Field(description="Sections of the report")


class State(TypedDict):
    topic: str
    sections: list[Section]
    completed_sections: Annotated[list, operator.add]
    final_report: str


class WorkerState(TypedDict):
    section: Section
    completed_sections: Annotated[list, operator.add]
