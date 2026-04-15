# Track2Event

Track2Event 是一個將影片中的追蹤結果轉換為「行為事件」的分析系統。

本專案流程包含：

* 目標偵測與追蹤（YOLOv8 + ByteTrack）
* 軌跡（trajectory）資料整理
* 運動特徵計算（速度、位移、持續時間）
* 規則式停留事件（stationary）判定
* 輸出結構化事件資料（JSON）

---

## 系統流程

```text
影片
→ 目標追蹤
→ 軌跡資料
→ 運動特徵
→ 行為事件（停留）
```

---

## 使用方式

1. 將 YOLOv8 模型放入 `models/`
   （本專案使用：https://huggingface.co/Ultralytics/YOLOv8）

2. 將影片放入 `data/`

3. 執行：

```bash
python main.py
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

## 說明

* 停留事件是基於速度、位移與持續時間的規則式判定
* 事件品質會受到追蹤演算法穩定度影響
* 在遮擋、ID 切換或漏檢情況下可能出現誤差
