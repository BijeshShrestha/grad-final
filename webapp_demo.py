from CQA import *

import streamlit as st
from streamlit import pyplot as plt
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import FunctionCallingAgentWorker, AgentRunner
from PIL import Image
import base64

def display_pdf(file_path):
    # Opening file from file path
    st.markdown("### PDF Preview")
    with open(file_path, "rb") as file:
        base64_pdf = base64.b64encode(file.read()).decode("utf-8")

    # Embedding PDF in HTML
    pdf_display = f"""<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="100%" type="application/pdf"
                        style="height:100vh;"
                    >
                    </iframe>"""

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)


# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
# Streamlit user interface setup
st.set_page_config(layout="wide", page_title="Chart Question Answering", page_icon="📊")

st.markdown("""
<style>
iframe {
    width: 110% !important;
    height: 8000px !important;
    border: none;
}
</style>
""", unsafe_allow_html=True)

st.title('Chart Question Answering')

# Here, switch the order of col1 and col2 to reverse the panes
col2, col1 = st.columns(2)  # Adjusted the order here
with col1.expander("Prospectus - Click to expand the PDF", expanded=False):
    display_pdf("./docs_deliverables/Prospectus_VIS_Group_Project_AI_Charts.pdf")

with col1.expander("Test report used in the tool", expanded=True):
    st.image(Image.open("./img/inflationreport.png").resize((int(.8 * Image.open("./img/tool_function_overview.png").width), int(1.8 * Image.open("./img/tool_function_overview.png").height))))

col1.markdown("###     CQA Tool Framework")
with col1.expander("Overiew of CQA Tool Framework"):
    st.image(Image.open("./img/tool_function_overview.png"))
    st.image(Image.open("./img/draft_pipeline.png"))

col1.markdown("###     CQA Tool Instructions")
col1.markdown("1️⃣ Upload a PDF file")
col1.markdown("2️⃣ Ask a question about the content of the PDF file")    
col1.markdown("3️⃣ The tool will generate a response to your question")


with col1.expander(":warning:  Finding and Limitations "):
    st.markdown("1️⃣ OpenAI Credits: Experimenting consumed substantial resources, especially when using GPT-4-turbo.")
    st.markdown("2️⃣ Hallucination occurred after several conversations, indicating that it can only sustain a conversation for three to four interactions.")
    st.markdown("3️⃣ GPT-3.5 facilitated a faster workflow, but it yielded poorer results.")
    st.markdown("4️⃣ The process of parsing chart and text data from a PDF could be improved. Currently, we use the Inkscape library, which is incompatible with Windows operating systems")
    st.markdown("5️⃣ Occasionally, the agent erroneously invokes the incorrect function.")
    st.markdown("6️⃣ There is a noticeable delay between the prompt and the response from the language model. Design limitations")
col2.markdown("### Chat, inquire, and modify the chart")

# # Initialize variables to store PDF data
# if 'text_data' not in st.session_state or 'chart_data' not in st.session_state:
#     st.session_state['text_data'], st.session_state['chart_data'] = [], []

# Ensure conversation and response history are part of session state
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []
if 'response_history' not in st.session_state:
    st.session_state['response_history'] = []

# Display the conversation history dynamically
def display_conversation_history():
    if 'conversation' not in st.session_state:
        st.session_state['conversation'] = []
    if 'response_history' not in st.session_state:
        st.session_state['response_history'] = []

    for i in range(len(st.session_state['conversation'])):
        col2.write(f"User: {st.session_state['conversation'][i]}")
        if i < len(st.session_state['response_history']):
            col2.write(f"{st.session_state['response_history'][i]}")

        # Additionally check for image responses and display them
        if i < len(st.session_state['response_history']) and isinstance(st.session_state['response_history'][i], str) and st.session_state['response_history'][i].endswith('.png'):
            st.image(st.session_state['response_history'][i], caption="Generated Chart")


# Display the conversation history and any images first
display_conversation_history()

def send_message():
    user_message = st.session_state['current_message']
    if user_message:
        # Append message to conversation
        st.session_state['conversation'].append(user_message)

        # Generate a response using the agent, which might include generating an image
        latest_image_path = process_inquiry_and_show_latest_image(user_message)
        if latest_image_path:
            # If an image is generated, use the image path as the response to display
            st.session_state['response_history'].append(latest_image_path)
            st.image(latest_image_path, caption="Latest Generated Chart")

        # Otherwise, generate a text response using the agent
        else:
            response = agent.chat(user_message)
            st.session_state['response_history'].append(response)

        # Clear the current message to reset the text input box
        st.session_state['current_message'] = ""

        # # Optionally rerun to update the UI
        # st.rerun()

if 'current_message' not in st.session_state:
    st.session_state['current_message'] = ""


# Input and send buttons are defined after displaying the images
message_input = col2.text_input("Enter your message here", key='current_message')
send_button = col2.button("Send", on_click=send_message)

if send_button:
    st.rerun()