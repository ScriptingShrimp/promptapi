import uvicorn
import os
from typing import Union
from fastapi import FastAPI
from openai import OpenAI


app = FastAPI()
modelTemperature=0.1
modelBaseURL="http://localhost:1234/v1"
modelAPIKey="lm-studio"
lmstudioModel="lmstudio-community/Meta-Llama-3-70B-Instruct-GGUF"

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/ai")
def read_root():
    client = OpenAI(base_url=modelBaseURL, api_key=modelAPIKey)

    completion = client.chat.completions.create(
        model=lmstudioModel,
        messages=[
            {"role": "system", "content": "From list of tools, select only one tool that is suitable for described task. Answer only with the name of the tool or this sentence 'The tool does not exist'.\n\nExample: What weather is now in Prague, Czech republic? \n"},
            {"role": "user", "content": "What is current population of earth? \n\n*getWeatherForCity.py \n*getPopulationForCity.py \n*getWeatherForCounty.py \n*getPopulationForCountry.py"},
        ],
        temperature=modelTemperature,
        # function_call=
        # max_tokens: -1,
    )
    
    return (completion.choices[0].message.content)

@app.get("/weather/{city}")
def getWeatherForCity(city: str):
    return {"city": city, "weathssssser": "sunny"}

@app.get("/listTools")
def listTools():
    listDir = os.listdir("./tools")
    return listDir

@app.get("/isFunctionNeeded")
def isFunctionNeeded():
    client = OpenAI(base_url=modelBaseURL, api_key=modelAPIKey)
    completion = client.chat.completions.create(

        model=lmstudioModel,
        messages=[
            {"role": "system", "content": "take user input and consider if there is a need for function call. \n\nExample: What weather is now in Prague, Czech republic? \n Answer: yes"},
            {"role": "user", "content": "what is current weather in Prague?"},
            {"role": "system", "content": "From list of tools, select only one tool that is suitable for described task. Answer only with the name of the tool or this sentence 'The tool does not exist'.\n\nExample: What weather is now in Prague, Czech republic? \n"},
            {"role": "user", "content": "What is current population of earth? \n\n*getWeatherForCity.py \n*getPopulationForCity.py \n*getWeatherForCounty.py \n*getPopulationForCountry.py"},
        ],
        temperature=modelTemperature,
    )
    
    return (completion)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)