# 叫號系統部署指南

本專案為簡易自訂叫號系統，可在個人筆電/電腦上直接以終端機執行，也可透過多種部署。 
可用於現場活動、櫃檯等情境。

---

##  基本單機部署（單機版）

適用：只需在一台電腦（Windows/Mac/Linux）操作、投影或現場用

1. **安裝 Python 3.8+ 及 pip**
   - [Python官網下載](https://www.python.org/downloads/)

2. **安裝所需套件**
   ```bash
   pip install streamlit pandas

3. **下載/複製本專案檔案到電腦資料夾**
4. **啟動系統**
   ```bash
   streamlit run queque_system.py

5. **瀏覽器自動開啟** http://localhost:8501 使用
   若未自動開啟，可手動輸入網址
   
---

## 多設備共用（區網版）

適用：一台電腦主控，多台手機/平板/電腦同時查看與操作

1. **先完成基本單機部署**
2. **啟動**
 ```bash
streamlit run call_system.py --server.address=0.0.0.0
```

3. **用主機的區網IP為同一區網的其他設備開啟**

   主控端投影、其他設備可即時同步看到叫號畫面
   
---

## 內部專屬部署（組織伺服器/私有雲）
適用：組織、學校、公司內部伺服器，須限定特定人員或安全管控

1. **參考「基本單機部署」步驟，將程式部署於伺服器上**

2. **啟動**
   ``` bash
   streamlit run call_system.py --server.address=0.0.0.0

   
3. **如有防火牆，請開放 8501 埠口**
4. **建議加 Nginx 或 Apache 做 Proxy，可設定 https 憑證，或限制 IP 存取**
5. **其他內網設備、公司 VPN 使用者可透過伺服器IP存取**

---

## 雲端免費部署
1. **請先Fork本專案**
2. **於自己的 Fork 進行部署**

- 以 Streamlit Cloud、Railway、Render、Vercel 等平台部署時，請選「你的 Fork」作為來源，流程與原始 repo 相同。
- 選擇主程式（如 `queque_system.py`）與 `requirements.txt`，自動一鍵部署。
- **如要分享給他人，請直接分享你自己的雲端網址。**

3. **可自行設定權限**

- 你可以設定你的 fork 為私人（private）或公開（public）。
- 可於 Fork 上進行客製化修改，本原始 repo 不會被影響。

---

## 常見問題
### 密碼驗證/管理員模式
可自行於 Streamlit 程式中加上簡單密碼機制或驗證碼欄位。

### 安全性
雲端部署時，請勿上傳敏感名單，建議僅公開號碼而非姓名等個人資訊。

### 大量/多人同時操作
免費雲端平台有同時使用數量限制，商用或大規模使用場景建議自架。

### 上傳名單
目前僅可CSV上傳名單，未來有機會再調整

---

歡迎 fork 本 repo，若有部署新平台心得或修正建議也歡迎 PR 分享！

##  一鍵部署（Fork 後再點擊下方 Badge 即可！）

[![Deploy to Streamlit Cloud](https://static.streamlit.io/badges/streamlit_cloud_badge_white.svg)](https://streamlit.io/cloud)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)
[![Hugging Face Spaces](https://img.shields.io/badge/Spaces-Deploy-blue?logo=HuggingFace)](https://huggingface.co/new-space?template=streamlit)

>  **先 Fork 本 repo，再點擊上方任一平台部署**




