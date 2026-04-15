# Track2Event

Track2Event 是一個將影片中的目標追蹤結果轉換為「行為事件」的分析工具。

系統將低層的感知結果（tracking）轉換為可解讀的結構化事件（event），作為後續分析或語言模型應用的基礎。

---

## 系統流程

```text
影片
→ 目標偵測與追蹤
→ 軌跡資料（trajectory）
→ 運動特徵（speed / distance / duration）
→ 行為事件（停留）
```

---

## 功能

* 目標偵測與追蹤（YOLOv8 + ByteTrack）
* 軌跡資料整理（per-track aggregation）
* 運動特徵計算（速度、位移、持續時間）
* 規則式停留事件（stationary）判定
* 輸出結構化 JSON 結果

---

## 使用方式

### 方法一：使用預設設定

```bash
python main.py
```

---

### 方法二：使用 CLI 指定參數

```bash
python cli.py --video data/video.mp4 --model models/yolov8x.pt
```

---

## 輸出結果

* `tracks.json`
  原始追蹤資料（每個 track 的 bbox 與 frame）

* `analyze_result.json`
  每個 track 的運動特徵（速度、位移、duration、label）

* `stationary_events.json`
  判定為「停留」的事件資料

---

## 系統設計

* 採用 **rule-based event detection**（非訓練模型）
* 將 tracking 結果抽象為 trajectory，再進行行為判定
* pipeline 設計支援：

  * CLI 使用
  * Python function 呼叫（tool-ready）
  * 後續整合 LLM / agent 系統

---

## 限制

* 事件品質受追蹤穩定度影響（ID switch、遮擋、漏檢）
* 非人物件若未過濾，可能影響結果（依模型設定而定）
* 判定規則基於 threshold，需依場景調整

---

## 模型

本專案使用 YOLOv8：

https://huggingface.co/Ultralytics/YOLOv8

請自行下載並放置於 `models/` 目錄。
