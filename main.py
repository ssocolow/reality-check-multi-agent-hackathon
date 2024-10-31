import os
from getpass import getpass
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from camel.configs import ChatGPTConfig
from camel.agents import ChatAgent

import requests


#### here's the user's interest for information comparation
user_interest="11111"
#### here's the website user need to provide for analysis
website_url = "https://docs.camel-ai.org/index.html"


def get_website_content(url: str) -> str:
    """
    Retrieve the content of a website using the Firecraw API.

    Parameters:
    url (str): The URL of the website to retrieve content from.

    Returns:
    str: The content of the website.
    """
    api_url = "https://api.firecraw.com/v1/scrape"
    headers = {
        "Authorization": "",
        "Content-Type": "application/json"
    }
    payload = {
        "url": url,
        "render": True
    }

    response = requests.post(api_url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("content", "No content found")
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

# Example usage:
try:
    content = get_website_content(website_url)
    print("Website content:", content)
except Exception as e:
    print("An error occurred:", e)







class ModelAgent:
    def __init__(self, model_plat, model_type):
        # Initialize the model with the specified name and API key.
        self.model = ModelFactory.create(
            model_platform=model_plat,
            model_type=model_type,
            model_config_dict=ChatGPTConfig().as_dict(), # [Optional] the config for model
    )
    
    def generate_response(self, input_data):
        sys_msg = 'You are an expert at coming up with hackathon ideas for multi-agent systems'
        agent = ChatAgent(
            system_message=sys_msg,
            model=self.model,
            message_window_size=1000, # [Optional] the length for chat memory
            )
        response = agent.step(input_data)
        # Generates a response using the model based on the provided input data.
        return response.msgs[0].content




# Define the AnalysisAgent class for comparing and refining responses
class AnalysisAgent:
    def __init__(self, model_name, api_key):
        # Initialize the analysis model with its API key.
        self.model = CamelModel(model_name=model_name, api_key=api_key)
    
    def analyze_responses(self, responses):
        # This method compares the responses from different models and highlights differences.
        analysis_input = {
            "response_a": responses[0],
            "response_b": responses[1],
            "response_c": responses[2]
        }
        
        # Generate an initial analysis using the model
        refined_output = self.model.generate(analysis_input)

        # Compare the responses and identify differences manually
        differences = self.compare_responses(responses)
        
        # Combine the refined output with the identified differences and warnings
        final_report = refined_output + "\n\nDifferences Noted:\n" + differences
        
        return final_report
    
    def compare_responses(self, responses):
        # Identify and compare the key points in the responses to find discrepancies.
        response_a, response_b, response_c = responses
        differences = []

        # Compare each section of the responses (for simplicity, let's assume they are strings)
        if response_a != response_b:
            differences.append(
                "Difference between Model A and Model B: These sections do not match. "
                "Please verify the accuracy of this information."
            )
        
        if response_a != response_c:
            differences.append(
                "Difference between Model A and Model C: These sections do not match. "
                "Please verify the accuracy of this information."
            )
        
        if response_b != response_c:
            differences.append(
                "Difference between Model B and Model C: These sections do not match. "
                "Please verify the accuracy of this information."
            )
        
        # Combine all differences into a single string
        if differences:
            return "\n".join(differences)
        else:
            return "No significant differences were detected between the models' responses."

# Initialize ModelAgent instances for each AI model
web_content=content

rebuild_prompt=f"""
You are a proofreader, and you help to extract all the information from the 'Content' based on 'user intertest'.\n###\n"""+f"user interest: {user_interest}\n###\n"+f"Conetnt: {web_content}"
model_a_agent = ModelAgent(ModelPlatformType.OPENAI, ModelType.GPT_4O_MINI)
model_b_agent = ModelAgent(ModelPlatformType.OPENAI, ModelType.GPT_4O)
model_c_agent = ModelAgent(ModelPlatformType.OPENAI, ModelType.GPT_3_5_TURBO)

web_a=model_a_agent.generate_response(rebuild_prompt)
web_b=model_b_agent.generate_response(rebuild_prompt)
web_c=model_c_agent.generate_response(rebuild_prompt)


model1 = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI,
    model_type=ModelType.GPT_4O,
    model_config_dict=ChatGPTConfig().as_dict(), # [Optional] the config for model
    )

model2 = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI,
    model_type=ModelType.GPT_4O,
    model_config_dict=ChatGPTConfig().as_dict(), # [Optional] the config for model
    )

model3 = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI,
    model_type=ModelType.GPT_4O,
    model_config_dict=ChatGPTConfig().as_dict(), # [Optional] the config for model
    )
sys_msg = 'You are an expert at coming up with hackathon ideas for multi-agent systems'
usr_msg=f""""You are an expert AI tasked with analyzing and comparing three different responses " 
"provided by separate AI models. Your goal is to identify any discrepancies, differences, " 
"or inconsistencies between these responses. For each difference you find, provide a brief " 
"explanation of what is different and suggest why the difference might exist. Additionally, " 
"highlight any sections that might contain errors or require further verification. " 
"Here are the responses:\n\n" "Response A: {web_a}\n\n" "Response B: {web_b}\n\n" "Response C: {web_c}\n\n" "Please analyze these responses and provide a detailed report, pointing out specific differences " "and flagging any potentially incorrect information." )"""

agent = ChatAgent(
    system_message=sys_msg,
    model=model1,
    message_window_size=1000, # [Optional] the length for chat memory
    )

response = agent.step(usr_msg)

# Check the response (just for illustrative purpose)
print(response.msgs[0].content)


# # Initialize the AnalysisAgent for comparing and refining responses
# analysis_agent = AnalysisAgent("model_analyzer", os.getenv("ANALYSIS_MODEL_API_KEY"))

# # Define the central function that coordinates the agents
# def multi_agent_pipeline(user_input_1, user_input_2):
#     # Prepare the input data for the model agents
#     input_data = {
#         "user_requirement": user_input_1,
#         "url": user_input_2
#     }
    
#     # Generate responses from each of the three model agents
#     response_a = model_a_agent.generate_response(input_data)  # Response from Model A
#     response_b = model_b_agent.generate_response(input_data)  # Response from Model B
#     response_c = model_c_agent.generate_response(input_data)  # Response from Model C
    
#     # Print the intermediate responses for debugging or review
#     print("Response A:", response_a)
#     print("Response B:", response_b)
#     print("Response C:", response_c)
    
#     # Use the analysis agent to analyze the differences and generate the final report
#     final_report = analysis_agent.analyze_responses([response_a, response_b, response_c])
    
#     # Return the final refined report generated by the analysis agent
#     return final_report

# # Define the inputs (example user requirement and URL)
# user_input_1 = "The user wants to know about the latest tech news."
# # user_input_2 = "https://example.com/latest-tech-news"
# web_content="***"





# # Execute the multi-agent pipeline and get the final report
# final_report = multi_agent_pipeline(user_input_1, user_input_2)

# # Print the final report, which integrates and refines the different responses.
# print("Final Report:", final_report)





















# # Prompt for the API key securely
# # openai_api_key = getpass('Enter your API key: ')
# os.environ["OPENAI_API_KEY"] = ''
# # 
# sys_msg = 'You are an expert at coming up with hackathon ideas for multi-agent systems'


# modelA = ModelFactory.create(
#     model_platform=ModelPlatformType.OPENAI,
#     model_type=ModelType.GPT_4O_MINI,
#     model_config_dict=ChatGPTConfig().as_dict(), # [Optional] the config for model
#     )

# modelB = ModelFactory.create(
#     model_platform=ModelPlatformType.OPENAI,
#     model_type=ModelType.GPT_4O,
#     model_config_dict=ChatGPTConfig().as_dict(), # [Optional] the config for model
#     )

# modelC = ModelFactory.create(
#     model_platform=ModelPlatformType.OPENAI,
#     model_type=ModelType.GPT_3_5_TURBO,
#     model_config_dict=ChatGPTConfig().as_dict(), # [Optional] the config for model
#     )

# model1 = ModelFactory.create(
#     model_platform=ModelPlatformType.OPENAI,
#     model_type=ModelType.GPT_4O,
#     model_config_dict=ChatGPTConfig().as_dict(), # [Optional] the config for model
#     )

# model2 = ModelFactory.create(
#     model_platform=ModelPlatformType.OPENAI,
#     model_type=ModelType.GPT_4O,
#     model_config_dict=ChatGPTConfig().as_dict(), # [Optional] the config for model
#     )

# model3 = ModelFactory.create(
#     model_platform=ModelPlatformType.OPENAI,
#     model_type=ModelType.GPT_4O,
#     model_config_dict=ChatGPTConfig().as_dict(), # [Optional] the config for model
#     )

# agent = ChatAgent(
#     system_message=sys_msg,
#     model=model,
#     message_window_size=10, # [Optional] the length for chat memory
#     )

# # Define a user message
# usr_msg = 'I am entering the CAMEL-AI hackathon, what are some good ideas around multi-agent systems?'

# # Sending the message to the agent
# response = agent.step(usr_msg)

# # Check the response (just for illustrative purpose)
# print(response.msgs[0].content)



# # model = ModelFactory.create(
# #     model_platform=ModelPlatformType.MISTRAL,
# #     model_type=ModelType.MISTRAL_LARGE,
# #     model_config_dict=MistralConfig().as_dict(), # [Optional] the config for model
# # )
