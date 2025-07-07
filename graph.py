from graph_schema import State
from nodes import assign_worker, synthesizer, make_orchestrator, make_worker
from langgraph.graph import StateGraph, START, END
from model_init import get_models


def graph(groq_api_key):

    structured_output_model, model = get_models(groq_api_key)

    orchestrator = make_orchestrator(structured_output_model)
    worker = make_worker(model)

    graph_builder = StateGraph(State)

    graph_builder.add_node("orchestrator", orchestrator)
    graph_builder.add_node("worker", worker)
    graph_builder.add_node("synthesizer", synthesizer)

    graph_builder.add_edge(START, "orchestrator")
    graph_builder.add_conditional_edges("orchestrator", assign_worker, ["worker"])
    graph_builder.add_edge("worker", "synthesizer")
    graph_builder.add_edge("synthesizer", END)

    final_graph = graph_builder.compile()

    return final_graph
