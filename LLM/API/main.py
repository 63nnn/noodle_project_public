from fastapi import FastAPI
import time  # calculate latency
import FileLog  # made by logging fileHandler
from functools import wraps  # fastAPI need this to use decorator
import dataGemini, dataChatGPT, dataTaiwanllm
import data2FGemini, data2FChatGPT, data2FTaiwanllm


# logger
API_log = FileLog.FileLog(
    "./API/logs/API_server.log.csv", "API_server", encoding="utf-8"
)
API_log.setLoggerLevel("Info")


# FastAPI
app = FastAPI()


# decorator for estimate time
def time_latency(func):
    @wraps(func)  # FastAPI need this decorator
    def wrapper(*arg, **kwarg):
        time0 = time.time()
        tmp = func(*arg, **kwarg)
        latency = round(time.time() - time0, 2)
        API_log.info({"system": {"message": "latency", "latency": latency}})
        print(f">>> latency: {latency} s")
        return tmp

    # wrapper.__name__ = func.__name__  # to fix flask bug about endpoint
    return wrapper


# ori
@app.get("/dajianoodle/guide/llm/1f/gemini/{question}")
@time_latency
def gemini(question: str):

    answer = "Not yet. We are out of monkey"
    answer, err_msg = dataGemini.chat_with_model(question)
    if not err_msg:  # err_msg false
        API_log.info(
            {"chat": {"model": "Gemini", "question": question, "answer": answer}}
        )
    else:
        API_log.error({"error": err_msg})

    return {"response": {"answer": answer}}


@app.get("/dajianoodle/guide/llm/1f/gpt/{question}")
@time_latency
def chatgpt(question: str):

    answer = "Not yet. We are out of monkey"
    answer, err_msg = dataChatGPT.chat_with_model(question)
    if not err_msg:  # err_msg false
        API_log.info(
            {"chat": {"model": "GPT-3.5 Turbo", "question": question, "answer": answer}}
        )
    else:
        API_log.error({"error": err_msg})

    return {"response": {"answer": answer}}


@app.get("/dajianoodle/guide/llm/1f/twllm/{question}")
@time_latency
def twllm(question: str):

    answer = "Not yet. We are out of monkey"
    answer, err_msg = dataTaiwanllm.chat_with_model(question)
    if not err_msg:  # err_msg false
        API_log.info(
            {"chat": {"model": "TaiwanLLM", "question": question, "answer": answer}}
        )
    else:
        API_log.error({"error": err_msg})

    return {"response": {"answer": answer}}


# 2F
@app.get("/dajianoodle/guide/llm/2f/gemini/{question}")
@time_latency
def gemini_2f(question: str):

    answer = "Not yet. We are out of monkey"
    answer, err_msg = data2FGemini.chat_with_model(question)
    if not err_msg:  # err_msg false
        API_log.info(
            {"chat": {"model": "Gemini", "question": question, "answer": answer}}
        )
    else:
        API_log.error({"error": err_msg})

    return {"response": {"answer": answer}}


@app.get("/dajianoodle/guide/llm/2f/gpt/{question}")
@time_latency
def chatgpt_2f(question: str):

    answer = "Not yet. We are out of monkey"
    answer, err_msg = None, True
    if not err_msg:  # err_msg false
        API_log.info(
            {"chat": {"model": "GPT-3.5 Turbo", "question": question, "answer": answer}}
        )
    else:
        API_log.error({"error": err_msg})

    return {"response": {"answer": answer}}


@app.get("/dajianoodle/guide/llm/2f/twllm/{question}")
@time_latency
def twllm_2f(question: str):

    answer = "Not yet. We are out of monkey"
    answer, err_msg = data2FTaiwanllm.chat_with_model(question)
    if not err_msg:  # err_msg false
        API_log.info(
            {"chat": {"model": "TaiwanLLM", "question": question, "answer": answer}}
        )
    else:
        API_log.error({"error": err_msg})

    return {"response": {"answer": answer}}


@app.get("/callback/{pwd}/{sth}")
@time_latency
def callback(pwd: str, sth: str):
    if pwd == "3773":
        print(sth)
        API_log.info({"system": {"message": sth}})
        return {"response": f"{sth}"}


@app.get("/reboot/{sth}")
def reboot(sth):
    if sth == "3223536":
        import os, sys

        API_log.critical({"system": {"message": "API server is rebooting."}})
        os.execl(sys.executable, sys.executable, *sys.argv)
    return {"response": "rebooting"}


@app.get("/")
def root():
    return "Nothing Here"


if __name__ == "__main__":
    import uvicorn
    import json

    with open("./API/private.json") as file:
        jfile = json.load(file)

    API_log.info({"system": {"message": "API server is running."}})
    uvicorn.run("main:app", host=jfile["host"]["ip"], port=jfile["host"]["port"])
