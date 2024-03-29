import os
from openai import OpenAI
from joblib import Memory
from tenacity import retry, stop_after_attempt, wait_random_exponential
from dotenv import load_dotenv

load_dotenv()
memory = Memory("cachegpt")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-3.5-turbo"


@retry(wait=wait_random_exponential(min=10, max=30),
       stop=stop_after_attempt(25))
def generate(messages, model):
    print("calling GPT... model=" + model)
    return client.chat.completions.create(model=model, messages=messages)


@memory.cache
def ask(messages, model):
    response = generate(messages, model)
    return response.choices[0].message.content


def ex(content, model):
    messages = [
        {
            "role": "system",
            "content": "You are a constraint solver. You are given sentences and return whether they are consistent. You should return False or True, followed by an explanation. If there is a simple statement, just return True."
        },
        {
            "role": "user",
            "content": content
        }
    ]
    response = ask(messages, model)
    return response


def gen(content, typ, model=MODEL):
    messages = [
        {
            "role": "system",
            "content": f"You are a storyteller. You are given a story so far and asked to create a {typ}. Please return one sentence."
        },
        {
            "role": "user",
            "content": content
        }
    ]
    response = ask(messages, model)
    return response

def isInteresting(content, model=MODEL):
    messages = [
        {
            "role": "system",
            "content": f"You are a critical reader. You are given a story so far and asked whether it is interesting. You should return False or True, followed by an explanation. If there is a simple statement, just return True."
        },
        {
            "role": "user",
            "content": content
        }
    ]
    response = ask(messages, model)
    return response


def constraint(content):
    r = ex(content, MODEL)
    print(r)
    return r.lower().startswith('true')


def constraintInteresting(content):
    r = isInteresting(content, MODEL)
    print(r)
    return r.lower().startswith('true')
