import os
from dotenv import load_dotenv
import datetime
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Import classes related to the agent setup
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import ReActAgent, FunctionCallingAgentWorker, AgentRunner

# Import classes for chat messages and tools
from llama_index.core.llms import ChatMessage
from llama_index.core.tools import BaseTool, FunctionTool, QueryEngineTool, ToolMetadata

# Import classes for data indexing and storage
from llama_index.core import VectorStoreIndex, StorageContext, SimpleDirectoryReader, load_index_from_storage
from llama_index.core.objects import ObjectIndex




# Load environment variables
load_dotenv()
# Retrieve API keys from environment variables. Keep separate file .env in the same directory as this file and add teh keys there. 
openai_api_key = os.getenv("OPENAI_API_KEY")


# Define the bar chart creation tool
def create_bar_chart(data, title="Bar Chart", x_label="X-axis", y_label="Y-axis", color="skyblue"):
    """
    Generates and saves a bar chart based on the provided data. The data can be a dictionary,
    a list of tuples, or a simple list of values.

    Parameters:
    - data (dict, list of tuples, or list of values): The data to plot.
      - If a dictionary, expects {x_label: y_value}.
      - If a list of tuples, expects [(x_label, y_value), ...].
      - If a list of values, each value is plotted with a default x_label.
    - title (str): The title of the chart.
    - x_label (str): The label for the x-axis.
    - y_label (str): The label for the y-axis.
    - color (str): The color of the bars in the chart.
    """
    # Handle a simple list of values by assigning default x_labels
    if isinstance(data, list) and all(isinstance(item, (int, float)) for item in data):
        data = {f"Item {i+1}": val for i, val in enumerate(data)}
    # Handle a list of tuples
    elif isinstance(data, list) and all(isinstance(item, tuple) for item in data):
        data = {item[0]: item[1] for item in data}
    elif not isinstance(data, dict):
        raise ValueError("Data must be a dictionary, a list of tuples, or a list of numeric values.")

    fig, ax = plt.subplots()
    ax.bar(data.keys(), data.values(), color=color)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the figure
    directory = "temp_img"
    if not os.path.exists(directory):
        os.makedirs(directory)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{directory}/{title.replace(' ', '_')}_{current_time}.png"
    plt.savefig(filename)
    plt.close(fig)
    print(f"Saved chart as {filename}")



def create_line_chart(data, title="Line Chart", x_label="X-axis", y_label="Y-axis", color="skyblue"):
    """
    Generates and saves a line chart based on the provided data. The data can be a dictionary,
    a list of tuples, or a simple list of values.

    Parameters:
    - data (dict, list of tuples, or list of values): The data to plot.
      - If a dictionary, expects {x_label: y_value}.
      - If a list of tuples, expects [(x_label, y_value), ...].
      - If a list of values, each value is plotted with a default x_label.
    - title (str): The title of the chart.
    - x_label (str): The label for the x-axis.
    - y_label (str): The label for the y-axis.
    - color (str): The color of the line in the chart.
    """
    # Handle a simple list of values by assigning default x_labels
    if isinstance(data, list) and all(isinstance(item, (int, float)) for item in data):
        data = {f"Item {i+1}": val for i, val in enumerate(data)}
    # Handle a list of tuples
    elif isinstance(data, list) and all(isinstance(item, tuple) for item in data):
        data = {item[0]: item[1] for item in data}
    elif not isinstance(data, dict):
        raise ValueError("Data must be a dictionary, a list of tuples, or a list of numeric values.")

    fig, ax = plt.subplots()
    
    ax.plot(list(data.keys()), list(data.values()), color=color, marker='o')  # Added a marker for better visibility
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the figure
    directory = "temp_img"
    if not os.path.exists(directory):
        os.makedirs(directory)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{directory}/{title.replace(' ', '_')}_{current_time}.png"
    plt.savefig(filename)
    plt.close(fig)
    print(f"Saved chart as {filename}")



# Define the bar chart creation tool
bar_chart_tool = FunctionTool.from_defaults(
    fn=create_bar_chart,  
    name="bar_chart_creator",
    description="Generates a dynamic bar chart based on provided data and parameters."
)


# Define the bar chart creation tool
line_chart_tool = FunctionTool.from_defaults(
    fn=create_line_chart,  
    name="line_chart_creator",
    description="Generates a dynamic line chart based on provided data and parameters."
)


try:
    storage_context = StorageContext.from_defaults(
        persist_dir="./test_files/textdata"
    )
    text_index = load_index_from_storage(storage_context)

    storage_context = StorageContext.from_defaults(
        persist_dir="./test_files/chartdata"
    )
    chart_index = load_index_from_storage(storage_context)

    index_loaded = True
except:
    index_loaded = False

if not index_loaded:
    # load data
    text_docs = SimpleDirectoryReader(
        input_files=["./test_files/inflation2024_report.pdf"]
    ).load_data()
    chart_docs = SimpleDirectoryReader(
        input_files=["./test_files/inflation2024_data_chart.pdf"]
    ).load_data()

    # build index
    text_index = VectorStoreIndex.from_documents(text_docs)
    chart_index = VectorStoreIndex.from_documents(chart_docs)

    # persist index
    text_index.storage_context.persist(persist_dir="./test_files/textdata")
    chart_index.storage_context.persist(persist_dir="./test_files/textdata")

text_engine = text_index.as_query_engine(similarity_top_k=3)
chart_engine = chart_index.as_query_engine(similarity_top_k=3)

query_engine_tools = [
    QueryEngineTool(
        query_engine=text_engine,
        metadata=ToolMetadata(
            name="textdata",
            description=(
                "Provides information about text in the document. "
                "Use a detailed plain text question as input to the tool."
            ),
        ),
    ),
    QueryEngineTool(
        query_engine=chart_engine,
        metadata=ToolMetadata(
            name="chartdata",
            description=(
                "Provides information about chart data in the document."
                "Use a detailed plain text question as input to the tool."
            ),
        ),
    ),
    bar_chart_tool,
    line_chart_tool,
]

obj_index = ObjectIndex.from_objects(
    query_engine_tools,
    index_cls=VectorStoreIndex,
)

llm = OpenAI(model="gpt-3.5-turbo")
agent_worker = FunctionCallingAgentWorker.from_tools(
    tool_retriever=obj_index.as_retriever(similarity_top_k=5),
    llm=llm,
    verbose=True,
    allow_parallel_tool_calls=True,
)
agent = AgentRunner(agent_worker)


def process_inquiry_and_show_latest_image(question):
    """
    Processes a given inquiry using an agent's chat function that might generate an image,
    prints the response, and displays the path to the newest image created in the 'temp_img'
    directory if available, along with the image itself.

    Parameters:
    - question (str): The inquiry that might lead to image creation.
    """
    inquiry_time = datetime.datetime.now()
    response = agent.chat(question)
    
    print(f"{response}")

    # Check the 'temp_img' directory for the newest file created after the inquiry
    directory = 'temp_img'
    latest_file = None
    latest_time = inquiry_time  # Start comparison from the inquiry time

    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                file_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_time > latest_time:  # Compare creation time
                    latest_time = file_time
                    latest_file = file_path

    # Print the path to the latest image if available and display the image
    if latest_file:
        return latest_file  # Return the file path to be used in Streamlit
    return None  # Return None if no file was created


# def main(): 
#     while True:
#         question = input("Ask your question (type 'exit' to quit): ")
#         if question.lower() == 'exit':
#             print("Goodbye!")
#             break
#         response = process_inquiry_and_show_latest_image(question)
#         print("Response:", response)

# if __name__ == "__main__":
#     main()



# # Example inquiry to generate a bar chart
# question = "Generate a line chart in black color for the inflation data."
# process_inquiry_and_show_latest_image(question)