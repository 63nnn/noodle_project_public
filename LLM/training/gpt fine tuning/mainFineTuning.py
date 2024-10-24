import FileLog

# logger
API_log = FileLog.FileLog(
    f"./training/gpt fine tuning/logsAPI_server.log.csv", encoding="utf-8"
)
API_log.setLoggerLevel("Info")
