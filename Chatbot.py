from openai import OpenAI, AzureOpenAI
import streamlit as st
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file if it exists
load_dotenv(override=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]

if "env_vars" not in st.session_state:
    # Get actual values from environment variables
    azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
    azure_api_key = os.environ.get("AZURE_OPENAI_API_KEY", "")
    azure_api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "")
    azure_deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "")
    openai_api_key = os.environ.get("OPENAI_API_KEY", "")
    
    st.session_state.env_vars = {
        "AZURE_OPENAI_ENDPOINT": azure_endpoint,
        "AZURE_OPENAI_API_KEY": azure_api_key,
        "AZURE_OPENAI_API_VERSION": azure_api_version,
        "AZURE_OPENAI_DEPLOYMENT_NAME": azure_deployment,
        "OPENAI_API_KEY": openai_api_key
    }
    
    # Debug what we loaded
    for key, value in st.session_state.env_vars.items():
        if value:
            masked = value[:4] + "..." + value[-4:] if len(value) > 8 else "***"
            logger.info(f"Loaded {key}: {masked}")
        else:
            logger.info(f"{key} not found in environment")

# Helper function to validate Azure endpoint
def validate_azure_endpoint(endpoint):
    if not endpoint:
        return False
    if not endpoint.startswith("https://"):
        return False
    if not endpoint.endswith(".openai.azure.com/"):
        # Add trailing slash if missing
        if endpoint.endswith(".openai.azure.com"):
            return endpoint + "/"
    return endpoint

with st.sidebar:
    st.title("API Configuration")
    api_type = st.radio("API Type", ["OpenAI", "Azure OpenAI"])
    
    if api_type == "OpenAI":
        # Get the stored value from session state
        saved_openai_key = st.session_state.env_vars.get("OPENAI_API_KEY", "")
        openai_api_key = st.text_input(
            "OpenAI API Key", 
            key="chatbot_api_key", 
            type="password",
            value=saved_openai_key,
            placeholder="sk-..."
        )
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    else:
        # Get the stored values from session state
        saved_azure_key = st.session_state.env_vars.get("AZURE_OPENAI_API_KEY", "")
        saved_azure_endpoint = st.session_state.env_vars.get("AZURE_OPENAI_ENDPOINT", "")
        saved_azure_deployment = st.session_state.env_vars.get("AZURE_OPENAI_DEPLOYMENT_NAME", "")
        saved_azure_api_version = st.session_state.env_vars.get("AZURE_OPENAI_API_VERSION", "")
        
        openai_api_key = st.text_input(
            "Azure OpenAI API Key", 
            key="azure_api_key", 
            type="password",
            value=saved_azure_key,
            placeholder="your-azure-openai-api-key"
        )
        
        azure_endpoint = st.text_input(
            "Azure OpenAI Endpoint", 
            key="azure_endpoint",
            value=saved_azure_endpoint,
            placeholder="https://your-azure-openai-endpoint.openai.azure.com/"
        )
        
        azure_deployment = st.text_input(
            "Azure Deployment Name", 
            key="azure_deployment", 
            value=saved_azure_deployment,
            placeholder="gpt-4o",
            help="This is your deployment name, e.g., gpt-4o"
        )
        
        azure_api_version = st.text_input(
            "Azure API Version", 
            key="azure_api_version", 
            value=saved_azure_api_version,
            placeholder="2024-08-01-preview"
        )
        
        "[Get Azure OpenAI access](https://azure.microsoft.com/en-us/products/cognitive-services/openai-service)"
    
    # Debug button to check environment variables
    if st.button("Debug Environment"):
        st.write("Session state variables:")
        for key, value in st.session_state.env_vars.items():
            if value:
                masked = value[:4] + "..." + value[-4:] if len(value) > 8 else "***"
                st.write(f"{key}: {masked}")
            else:
                st.write(f"{key}: Not set")
    
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI or Azure OpenAI")

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if api_type == "OpenAI" and not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    elif api_type == "Azure OpenAI":
        if not openai_api_key:
            st.info("Please add your Azure OpenAI API key to continue.")
            st.stop()
        if not azure_endpoint:
            st.info("Please add your Azure OpenAI endpoint to continue.")
            st.stop()
        if not azure_deployment:
            st.info("Please add your Azure OpenAI deployment name to continue.")
            st.stop()
        
        # Validate and fix Azure endpoint
        azure_endpoint = validate_azure_endpoint(azure_endpoint)
        if not azure_endpoint:
            st.error("Invalid Azure endpoint format. Should be: https://YOUR_RESOURCE_NAME.openai.azure.com/")
            st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    try:
        if api_type == "OpenAI":
            client = OpenAI(api_key=openai_api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo", 
                messages=st.session_state.messages
            )
        else:
            # Debug info
            # st.info(f"Connecting to Azure endpoint: {azure_endpoint}")
            
            client = AzureOpenAI(
                api_key=openai_api_key,
                api_version=azure_api_version,
                azure_endpoint=azure_endpoint
            )
            
            try:
                response = client.chat.completions.create(
                    model=azure_deployment,
                    messages=st.session_state.messages
                )
            except Exception as e:
                # Try with deployment_name instead of model
                st.warning(f"Retrying with deployment_name parameter: {str(e)}")
                response = client.chat.completions.create(
                    deployment_name=azure_deployment,
                    messages=st.session_state.messages
                )
            
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
        
    except Exception as e:
        st.error(f"Error occurred: {str(e)}")
        # More detailed error info for debugging
        st.error("If you're using Azure OpenAI, verify your endpoint, API key, and deployment name.")
        st.error("Check your network connection and make sure the Azure resource is accessible.")
        logger.exception("API call failed")
