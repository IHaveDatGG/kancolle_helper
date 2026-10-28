# Kancolle Helper

A lightweight, portable Windows helper for **KanColle** (especially tailored for **POI** browser users). It uses image recognition and background clicks to automate repetitive battle flows, designed to stay out of your way so you can keep playing normally.
⚠️ **Note: Do not minimize the target game/browser window**, or capture and background clicks will stop working.

面向 **艦隊收藏（KanColle）** 玩家（特別是 **POI** 瀏覽器使用者）的輕量免安裝 Windows 輔助工具。透過 **圖像辨識** 與 **背景點擊** 幫你處理繁瑣的戰鬥流程，支援背景常駐，不干擾一般操作。
⚠️ **注意：請勿將遊戲／POI 視窗最小化**，否則畫面截圖與點擊會失效。

**Platform:** Windows only | **Version:** v0.1.3

---

## English

### What it does

- **Main app** (`start.bat`): The core automation loop. It watches the game window, matches templates (compass, formation, Next, return to port, advance/retreat, night battle, etc.), and clicks for you. You can tweak advance and night-battle behavior right from the UI.
- **Extended Mode / Experimental** (`start_extended.bat`): Scripted sorties for specific maps (e.g., 5-2 / 5-3) from port and back. Built as clean overrides on top of the main code without messing with core files.

All image templates live in `templates/`. Make sure to set the **window title** in the UI to match your client (defaults to `poi`).

### Portable release

No messy system-wide installations here. The project comes as a self-contained folder with portable Python included.

| Item | Description |
|------|-------------|
| **`python/`** | Bundled minimal portable Python. Dependencies are automatically installed on your first launch. |
| **Updates** | Every time you launch via `start.bat` , it checks for updates using a Git-based script (`src/update.py`). When a new version drops, just restart `start.bat`—no reinstall needed. |

### How to Use

1. Unzip the release folder anywhere you like.(Note: Avoid non-ASCII characters in the path, as they may cause errors).
2. From the **project root** (the folder containing `python/` and `templates/`), double-click `start.bat`.

That's it! It handles dependencies and updates automatically before launching the UI. *First launch might take a moment while packages download.*

### Capture mode (toolbar)

Two modes are available:
- **Single (Default)**: Lower CPU usage, but the window might flash a capture border on every screenshot.
- **Continuous**: If the flickering is bothering you, you can switch to this mode, but it will use a little more CPU resources.

### Disclaimer

**This tool automates inputs for a game client. Use at your own risk.** Please respect the game's terms of service and local regulations. The authors take zero responsibility for any account or data loss.

---

## 繁體中文

### 功能特色

- **主程式**（`start.bat`）：萬用的半自動化工具。透過截圖與模板辨識（羅盤、陣形、次、帰、進擊／撤退、夜戰等按鈕）進行背景點擊；UI 上可自由調整進擊與夜戰的處理方式。
- **Extended（實驗模式）**（`start_extended.bat`）：針對特定海域（如 5-2 / 5-3）的完整出擊腳本，採用分離覆寫設計，不改動主程式。

模板圖片都放在 `templates/` 裡。記得在 UI 將**視窗標題**設定成你的客戶端名稱（預設為 `poi`）。

### 可攜式、免安裝

採用**純資料夾打包**的形式，內建可攜式 Python，不用另外安裝在電腦上其他地方。

| 項目 | 說明 |
|------|------|
| **`python/`** | 內附精簡版可攜式 Python，首次啟動時會自動下載需要的相依套件。 |
| **自動更新** | 每次執行 `start.bat` 時，都會透過內建的 Git 更新腳本（`src/update.py`）檢查更新。有更新時只要重開 `start.bat` 就能直接變新版！

### 快速上手

1. 解壓縮到任意位置，注意路徑中有非英文數字時可能會導致錯誤。
2. 在 **專案根目錄**（含 `python/`、`templates/` 資料夾的那層）雙擊 **`start.bat`**。

`start.bat` 會自動安裝依賴並完成更新，再啟動主程式介面。首次執行若需下載套件，可能需等待一段時間。

### 截圖模式（工具列）

提供兩種截圖模式切換：
- **單次（預設）**：CPU 占用較低，但每次截圖時邊框可能會閃爍。
- **連續**：如果覺得閃爍很煩可以切這項，但 CPU 佔用會稍微高一點。

### 免責聲明

**本工具會自動模擬遊戲操作，使用風險請自行承擔**。請遵守遊戲官方的服務條款與相關規範，作者不對任何封號或損失負任何責任。
