from graph_schema import State, WorkerState
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.constants import Send


def make_orchestrator(structured_output_model):
    def orchestrator(state: State):
        """Orchestrator that generates a plan for the report"""
        report_sections = structured_output_model.invoke(
            [
                SystemMessage(content="Generate a plan for the report."),
                HumanMessage(content=f"Here is the report topic: {state['topic']}"),
            ]
        )
        return {"sections": report_sections.sections}

    return orchestrator


def make_worker(model):
    def worker(state: WorkerState):
        """Worker writes a section of the report"""
        section = model.invoke(
            [
                SystemMessage(
                    content="Write a report section following the provided name and description. "
                    "Include no preamble for each section. Use markdown formatting."
                ),
                HumanMessage(
                    content=f"Here is the section name: {state['section'].name} and description: {state['section'].description}"
                ),
            ]
        )
        return {"completed_sections": [section.content]}

    return worker


def assign_worker(state: State):
    """Assign a worker to each section in the plan"""

    return [Send("worker", {"section": s}) for s in state["sections"]]


def synthesizer(state: State):
    """Synthesize full report from sections"""
    completed_sections = state["completed_sections"]
    completed_report_sections = "\n\n---\n\n".join(completed_sections)

    return {"final_report": completed_report_sections}
