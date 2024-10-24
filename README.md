# 觀光工廠元宇宙結合生成式AI導覽員

## 檔案結構

### LLM

#### API

* API server 本體

#### training

* datasets: 設計後的資料集
* LLM_eval: 測試模型性能與圖表輸出
* format convert: 以datasets為來源將資料集轉為各模型需要的格式
* gpt fine tuning: fine tuning gpt 的腳本

### dcBot

* discord Bot
* 大部分功能是debug用(重啟server指令、發送server log訊息...)

## 專題內容

---

### 主體

#### 資料集來源

* 員工錄音, 訪問對象: 董事長
* 現場參觀
* ChatGPT讀取檔案後生成 -> 人工修正 -> 結構化設計問題 -> 個性化回應

#### 生成式AI導覽員

* 架構

> * API sever
> * TWLLM + LoRA
> * Gemini Pro + Few Shot Prompting

* API server

> * log檔案紀錄
> * 回應格式

---

### 分析

#### 開發環境、工具

> * vacs
> * PC
> * postman
> * wandb
> * text-generation-webui
> * discord Bot

#### 資料集設計

* 董事長介紹錄音 -> 生成逐字稿並且修改使語句通順
* ChatGPT讀取檔案後生成 -> 人工修正 -> 結構化設計問題 -> 個性化回應

> * type1: ChatGPT在讀取逐字稿後生成，依照正確性人工修改
> * type2: 結構化人工生成，參考type1發問方式
> * type3: 基於type2調整個性、口吻更人性化、提升回答精準程度，明確分辨在製程個階段的麵條，自我回歸生成、next-token-prediction

#### 大型語言模型評估

* A round vs B round

> * A round: 與原始問答相差無幾
> * B round: 基於原始問答進行改動，測試模型的范化能力

* 機器評估指標

> * BLEU
> * ROUGE
> * Sentence Transformation
>
> * 機器評估比較
>>
>>* type2 LoRA Rank(8 -> 128 -> 256), epochs(50, 100)
>>* type2 vs type3
>>* type3 epochs(100 -> 200 -> 300)
>>* type3 100 epochs, Batch sizes(32 -> 64 -> 128)
>>* type3 128 Batch sizes, epochs(100, 200, 300)

* 人工評估指標

> * 延遲測算
> * 問卷評分
>
>> * 連貫性
>> * 資訊量
>> * 流暢性
>> * 相關性
>> * 整體評價

* Flask vs FastAPI

> FastAPI: def vs async def vs async def await
>> async def await > def >>> async def
