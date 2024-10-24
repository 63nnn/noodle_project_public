from flask import Flask, jsonify
import time  # calculate latency
import FileLog  # made by logging fileHandler
import dataGemini, dataChatGPT, dataTaiwanllm
import data2FGemini, data2FChatGPT, data2FTaiwanllm


# logger
API_log = FileLog.FileLog(f"./API/logs/API_server.log.csv", encoding="utf-8")
API_log.setLoggerLevel("Info")


# Flask
app = Flask(__name__)


# decorator for estimate time
def time_latency(func):
    def wrapper(*arg, **kwarg):
        time0 = time.time()
        tmp = func(*arg, **kwarg)
        latency = round(time.time() - time0, 2)
        API_log.info({"latency": latency})
        print(f">>> latency: {latency} s")
        return tmp

    wrapper.__name__ = func.__name__  # to fix flask bug about endpoint
    return wrapper


# ori
@app.route("/dajianoodle/guide/llm/1f/gemini/<question>")
@time_latency
def gemini(question):

    answer = "Not yet. We are out of monkey"
    answer, err_msg = dataGemini.chat_with_model(question)
    if not err_msg:  # err_msg false
        API_log.info({"model": "Gemini", "question": question, "answer": answer})
    else:
        API_log.error(err_msg)

    return jsonify({"answer": answer})


@app.route("/dajianoodle/guide/llm/1f/gpt/<question>")
@time_latency
def chatgpt(question):

    answer = "Not yet. We are out of monkey"
    answer, err_msg = dataChatGPT.chat_with_model(question)
    if not err_msg:  # err_msg false
        API_log.info({"model": "GPT-3.5 Turbo", "question": question, "answer": answer})
    else:
        API_log.error(err_msg)

    return jsonify({"answer": answer})


@app.route("/dajianoodle/guide/llm/1f/twllm/<question>")
@time_latency
def twllm(question):

    answer = "Not yet. We are out of monkey"
    answer, err_msg = dataTaiwanllm.chat_with_model(question)
    if not err_msg:  # err_msg false
        API_log.info({"model": "TaiwanLLM", "question": question, "answer": answer})
    else:
        API_log.error(err_msg)

    return jsonify({"answer": answer})


# 2F
@app.route("/dajianoodle/guide/llm/2f/gemini/<question>")
@time_latency
def gemini_2f(question):

    answer = "Not yet. We are out of monkey"
    answer, err_msg = None, True
    if not err_msg:  # err_msg false
        API_log.info({"model": "Gemini", "question": question, "answer": answer})
    else:
        API_log.error(err_msg)

    return jsonify({"answer": answer})


@app.route("/dajianoodle/guide/llm/2f/gpt/<question>")
@time_latency
def chatgpt_2f(question):

    answer = "Not yet. We are out of monkey"
    answer, err_msg = None, True
    if not err_msg:  # err_msg false
        API_log.info({"model": "GPT-3.5 Turbo", "question": question, "answer": answer})
    else:
        API_log.error(err_msg)

    return jsonify({"answer": answer})


@app.route("/dajianoodle/guide/llm/2f/twllm/<question>")
@time_latency
def twllm_2f(question):

    answer = "Not yet. We are out of monkey"
    answer, err_msg = data2FTaiwanllm.chat_with_model(question)
    if not err_msg:  # err_msg false
        API_log.info({"model": "TaiwanLLM", "question": question, "answer": answer})
    else:
        API_log.error(err_msg)

    return jsonify({"answer": answer})


@app.route("/callback/<sth>")
def callback(sth):
    print(sth)
    API_log.info({"call": sth})
    return jsonify({"response": sth})


@app.route("/reboot/<sth>")
def reboot(sth):
    import os, sys

    if sth == "3223536":
        API_log.critical({"message": "API server is rebooting."})
        # 使用 os.execl 重新啟動程式，替換當前進程
        os.execl(sys.executable, sys.executable, *sys.argv)
    return jsonify({"response": "rebooting"})


@app.route("/")
def index():
    return "<h1>Nothing Here</h1>"


if __name__ == "__main__":
    app.debug = True
    # app.run(host="0.0.0.0", port=58840)
    app.run(host="127.0.0.1", port=3000)
