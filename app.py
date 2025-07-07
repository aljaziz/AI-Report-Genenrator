from graph import graph
import streamlit as st


st.title("🔗 AI Report Generator")
groq_api_key = st.sidebar.text_input("Groq API Key", type="password")


def generate_response(input_text):
    generator = graph(groq_api_key)
    report = generator.invoke({"topic": input_text})
    st.info(report["final_report"])


with st.form("my_form"):
    text = st.text_area(
        "Enter your topic:",
    )
    submitted = st.form_submit_button("Submit")
    if not groq_api_key.startswith("gsk_"):
        st.warning("Please enter your Groq API key!", icon="⚠")
    if submitted and groq_api_key.startswith("gsk_"):
        generate_response(text)
        # if st.button("Download"):
        #     st.download_button(
        #         label="Download PDF", data=result, file_name="Report.pdf"
        #     )
