# Getting started

## Installing dependencies

Run the script bin/init to install all dependencies.


## Configuring the Gemini API

Create a file .streamlit/secrets.toml and add the configuration for using Gemini. 

Example if you use the Vertex AI API:

```toml
[gemini]
vertexai = true
project = <project_name>
location = "global"
model = "gemini-2.0-flash-001"
```

Example if you use the Gemini API:

```toml
[gemini]
vertexai = false
api_key = <gemini_api_key>
model = "gemini-2.0-flash-001"
```


## Starting the application

Run bin/serve to start the app.
