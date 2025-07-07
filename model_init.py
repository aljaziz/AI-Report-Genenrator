from langchain_groq import ChatGroq
from graph_schema import Sections


def get_models(groq_api_key):
    # os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    model = ChatGroq(model="gemma2-9b-it", api_key=groq_api_key)
    structured_output_model = model.with_structured_output(Sections)
    return structured_output_model, model
