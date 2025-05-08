
# LLM idea generator

A simple application that generates and refines ideas on a given topic, by having one LLM generate the ideas and another LLM score and critique the ideas. You can then run multiple iterations to improve the idea.

You need access to the Gemini api to use the tool. Both Vertex AI API and Gemini API are supported.

[App screenshot](images/llm_idea_generator.png)

## How to use

Write the topic you want to generate an idea on to the textbox **What to generate ideas on?**. Press **Go!** to start the process. When the responses have arrived, press **Go!** again to refine the idea further. Continue for as long as you like.

## Setup

### Installing dependencies

Run the following command to install all dependencies:

```bash
bin/init
```

### Configuring the Gemini API

Create a file .streamlit/secrets.toml and add the configuration for using Gemini. 

Example if you use the Vertex AI API:

```toml
[gemini]
vertexai = true
project = "<gcp_project_name>"
location = "global"
model = "gemini-2.0-flash-001"
```

Example if you use the Gemini API:

```toml
[gemini]
vertexai = false
api_key = "<gemini_api_key>"
model = "gemini-2.0-flash-001"
```


### Starting the application

If using the Vertex AI API, first authenticate using gcloud. This is not needed if using Gemini API:

```bash
gcloud auth application-default login
```

Run the following command to start the app:

```bash
bin/serve
```

