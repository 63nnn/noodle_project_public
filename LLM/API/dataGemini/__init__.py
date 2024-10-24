import requests
import json

with open("API/private.json") as file:
    jj = json.load(file)


url = jj["GEMINI_URL"]
headers = {"Content-Type": "application/json"}


conversation_history = []
# Get the conversation history
with open("API/dataGemini/conversationHistory.jsonl", "r", encoding="utf-8") as file:
    for line in file:
        if line[-2] == ",":  # strip ","
            line = line[:-2]
        tmp = json.loads(line)
        conversation_history.append(tmp)


# Few-shot Prompting
def generate_data(conversation_history):
    return {
        # 訓練資料
        "contents": [{"parts": conversation_history}],
        # 生成設定
        "generationConfig": {
            "temperature": 0.3,
            "topK": 3,
            "topP": 0.4,
            "maxOutputTokens": 2048,
            "stopSequences": [],
        },
        # 安全設定
        "safetySettings": [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_LOW_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_LOW_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_LOW_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_LOW_AND_ABOVE",
            },
        ],
    }


def chat_with_model(question):
    # 將使用者的訊息加入對話列表
    conversation_history.append({"text": f"user: {question}"})
    data = generate_data(conversation_history)
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

        # 產生回應
        if "candidates" in response_json:  # 回答成功有 candidates
            answer = response_json["candidates"][0]["content"]["parts"][0]["text"]
            # 將模型的回答添加到對話歷史
            conversation_history.append({"text": f"model: {answer}"})
            err_msg = False
        else:
            if "error" in response_json:
                # err_msg = f'errCode: {response_json["error"]["code"]}, errMessage: {response_json["error"]["message"]}'
                errCode = response_json["error"]["code"]
                errMessage = response_json["error"]["message"]

    if err_msg:  # True == error occur
        answer = "對不起，我無法生成回答，請重新再詢問一遍。"
        err_msg = {"model": "Gemini", "errCode": errCode, "errMessage": errMessage}

    return answer, err_msg
