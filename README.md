# 🎈 Streamlit + LLM Examples App

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)

Starter examples for building LLM apps with Streamlit.

## Overview of the App

This app showcases a growing collection of LLM minimum working examples.

Current examples include:

- Chatbot (supports both OpenAI and Azure OpenAI)
- File Q&A
- Chat with Internet search
- LangChain Quickstart
- LangChain PromptTemplate
- Chat with user feedback

## Demo App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://llm-examples.streamlit.app/)

### Get an OpenAI API key

You can get your own OpenAI API key by following the following instructions:

1. Go to https://platform.openai.com/account/api-keys.
2. Click on the `+ Create new secret key` button.
3. Next, enter an identifier name (optional) and click on the `Create secret key` button.

### Set up Azure OpenAI access

To use Azure OpenAI instead:

1. Create an Azure OpenAI resource in the [Azure portal](https://portal.azure.com)
2. Deploy a model in the Azure OpenAI Studio
3. Get your endpoint URL and API key from the Azure portal
4. Use the deployment name when configuring the app

### Enter the API keys in Streamlit Community Cloud

To set the API keys as environment variables in Streamlit apps, do the following:

1. At the lower right corner, click on `< Manage app` then click on the vertical "..." followed by clicking on `Settings`.
2. This brings the **App settings**, next click on the `Secrets` tab and paste the API keys into the text box as follows:

```sh
OPENAI_API_KEY='xxxxxxxxxx'
AZURE_OPENAI_API_KEY='xxxxxxxxxx'
AZURE_OPENAI_ENDPOINT='https://your-endpoint-url'
AZURE_OPENAI_DEPLOYMENT_NAME='your-deployment-name'
```

### Set up environment variables

You can set up your API keys and configuration in two ways:

1. **Using the Streamlit UI**: Enter your API keys and configurations directly in the sidebar.
2. **Using a .env file**: Create a .env file in the root directory with the following variables:
```
OPENAI_API_KEY='xxxxxxxxxx'
AZURE_OPENAI_API_KEY='xxxxxxxxxx'
AZURE_OPENAI_ENDPOINT='https://your-endpoint-url'
AZURE_OPENAI_DEPLOYMENT_NAME='your-deployment-name'
```

## Run it locally

```sh
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run Chatbot.py
```
