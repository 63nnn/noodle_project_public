import json  # to load API_KEY
import requests


with open("API/private.json") as file:
    jj = json.load(file)

API_KEY = jj["GPT_API_KEY"]
conversation_history = [
    {"role": "system", "content": "你是一個有禮貌的大呷麵本家的虛擬導覽員"}
]
url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}


def chat_with_model(question):
    """json format"""

    # 將使用者的訊息加入對話列表
    conversation_history.append({"role": "user", "content": question})
    data = {
        "model": "ft:gpt-3.5-turbo-0613:tunghai-university::9I19JCpK",
        "messages": conversation_history,
        "max_tokens": 2048,
        "temperature": 0.5,
        "top_p": 0.2,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }
    err_msg = True  # if no error occur, it will be false later
    # Handle HTTP error
    try:
        response = requests.post(url, headers=headers, json=data)
        # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:  # Handles 4xx/5xx responses
        errCode = response.status_code
        errMessage = f"HTTP error occurred: {http_err}"
    except requests.exceptions.ConnectionError as conn_err:  # Handles network problems
        errCode = None
        errMessage = f"Connection error occurred: {conn_err}"
    except requests.exceptions.Timeout as timeout_err:  # Handles timeouts
        errCode = None
        errMessage = f"Timeout error occurred: {timeout_err}"
    except (
        requests.exceptions.RequestException
    ) as req_err:  # Catches all other request-related errors
        errCode = None
        errMessage = f"Request error occurred: {req_err}"
    else:
        response_json = response.json()

        if "choices" in response_json:
            answer = response_json["choices"][0]["message"]["content"]
            # 將模型的回答添加到對話歷史
            conversation_history.append({"role": "assistant", "content": answer})
            err_msg = False
        else:
            if "error" in response_json:
                errCode = response_json["error"]["code"]
                errMessage = response_json["error"]["message"]
    if err_msg:  # True == error occur
        answer = "對不起，我無法生成回答，請重新再詢問一遍。"
        err_msg = {
            "model": "GPT-3.5 Turbo",
            "errCode": errCode,
            "errMessage": errMessage,
        }

    return answer, err_msg
