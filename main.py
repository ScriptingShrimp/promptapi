# toolAnInvention
# toolAnInstrument

import requests
# import uvicorn
import os
from typing import Union
from openai import OpenAI


modelTemperature=0.01
modelBaseURL="http://localhost:1234/v1"
modelAPIKey="lm-studio"
lmstudioModel="lmstudio-community/Meta-Llama-3-70B-Instruct-GGUF"



# PROMPTS
# user
originalQuestion = "what weather is in Prague, Czech Republic?"
# system
## assistant 
assistantGeneral = "I am an offline assistant that can help you with various tasks. How can I help you today? I don't know any current prices, weather or any other real-time data." 
## hints
assistantHints = "Your goal is to analyze unanswered question and determine if there is is enough hints to answer the question. If there is enough hints, you simply answer with the hints in the bulletpoints. If there is not enough hints, add some suggestions and answer with the hints in the bulletpoints."
## evaluation
evaluationQuestion = "Your goal is to analyze question and answer to determine if the answer was specific, factual and relevant to the question. If the question is answered, you simply answer 'answered'. If the question is not answered, you answer 'not answered'."
## online access 
noOnlineInformation1 = "Its not possible for me to answer this question, since I am not able to access current data from the internet."
noOnlineInformation2 = "I have no data related to today since my knowledge ends in specific date."
# check the tools
areThereTools = "Consider if the question could be answered from list of tools. If yes select only one tool that is suitable for described task. Answer only with the name of the tool or this sentence 'The tool does not exist'.\n\nExample: What weather is now in Prague, Czech republic? \nAnswer: getWeatherInState.py\n\nExample: What is the capital of Germany?\nAnswer: tool does not exist"
## pyhton code
describeFunctionFile = "Based on provided input, describe what the function does."
# {"role": "system", "content": "From list of tools, select only one tool that is suitable for described task. Answer only with the name of the tool or this sentence 'The tool does not exist'.\n\nExample: What weather is now in Prague, Czech republic? \n"},
# {"role": "user", "content": "What is current population of earth? \n\n*getWeatherForCity.py \n*getPopulationForCity.py \n*getWeatherForCounty.py \n*getPopulationForCountry.py"},
# {"role": "system", "content": "From list of tools, select only one tool that is suitable for described task. Answer only with the name of the tool or this sentence 'The tool does not exist'.\n\nExample: What weather is now in Prague, Czech republic? \n"},
# {"role": "user", "content": "what is current price of bitcoin??"},
# final
toolPrompt = "You are helpful assistant. Now you can answer the questions with the use of the tools. The tool was able to answer the user question precisely. Tool has been called and the result is: \n"



def generalChat():
    client = OpenAI(base_url=modelBaseURL, api_key=modelAPIKey)
    completion = client.chat.completions.create(
        model=lmstudioModel,
        messages=[
            {"role": "system", "content": assistantGeneral},
            {"role": "user", "content": originalQuestion},
        ],
        temperature=modelTemperature,
    )
    return str(completion.choices[0].message.content)

def evaulateResponse(question: str, answer: str):
    client = OpenAI(base_url=modelBaseURL, api_key=modelAPIKey)
    completion = client.chat.completions.create(
        model=lmstudioModel,
        messages=[
            {"role": "system", "content": evaluationQuestion},
            {"role": "user", "content": "QUESTION:\n\n" + question + "\n\nANSWER:\n\n" + answer},
        ],
        temperature=modelTemperature,
    )
    return str(completion.choices[0].message.content)    

def listTools():
    listDir = os.listdir("./tools")
    return str(listDir)

def stringifyTool(path="./tools/getWeather.py"):
    toolString = str(open(path).read())
    return toolString

functionContent = stringifyTool()


def giveHintsToSolveTheProblem(hints: str):
    client = OpenAI(base_url=modelBaseURL, api_key=modelAPIKey)
    completion = client.chat.completions.create(
        model=lmstudioModel,
        messages=[
            {"role": "system", "content": assistantHints},
            {"role": "user", "content": hints},
        ],
        temperature=modelTemperature,
    )
    return str(completion.choices[0].message.content)

def solveTheTaskByCheckingTools(problemStatement: str):
    lt=listTools()
    client = OpenAI(base_url=modelBaseURL, api_key=modelAPIKey)
    completion = client.chat.completions.create(
        model=lmstudioModel,
        messages=[
            {"role": "system", "content": areThereTools},
            {"role": "user", "content": "THE PROBLEM:\n\n" + problemStatement + "LIST OF TOOLS:\n\n" + lt},
        ],
        temperature=modelTemperature,
    )
    return str(completion.choices[0].message.content)

def callTheTool(toolPath: str):
    exec(open("tools/" + str(toolPath)).read())

def finalAnswer(toolResult: str):
    client = OpenAI(base_url=modelBaseURL, api_key=modelAPIKey)
    completion = client.chat.completions.create(
        model=lmstudioModel,
        messages=[
            {"role": "system", "content": toolPrompt + toolResult},
            {"role": "user", "content": originalQuestion},
        ],
        temperature=modelTemperature,
    )
    return str(completion.choices[0].message.content)

def chain():
    gC: str = generalChat()
    eR: str = evaulateResponse(question=originalQuestion, answer=gC)

    if eR.lower().__contains__("not"):
        dF = giveHintsToSolveTheProblem(hints=gC)
        sT: str = solveTheTaskByCheckingTools(problemStatement=gC)
        if sT.lower().__contains__("the tool does not exist"):
            return sT
        else:
            cT = callTheTool(toolPath=sT)
            return cT
    else:
        return eR
    



print(chain())


## tools
#             {"role": "system", "content": "From list of tools, select only one tool that is suitable for described task. Answer only with the name of the tool or this sentence 'The tool does not exist'.\n\nExample: What weather is now in Prague, Czech republic? \n"},
