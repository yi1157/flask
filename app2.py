# 主頁:welcome to my website
# 次頁:此頁用來作金額轉換, 下拉選單, 請輸入要轉換多少美金


# from flask import Flask, render_template 

# app = Flask(__name__) 

# @app.route("/") 
# def home():
# 	return render_template("index.html")

# @app.route("/amount") # 次頁
# def money():
# 	return render_template("money.html")

# if __name__ == '__main__':
# 	app.run("127.0.0.1", port=100, debug=True)



from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# API 來源 (美金為基準)
API_URL = 'https://v6.exchangerate-api.com/v6/902ea5ad90fe41e8477ebef3/latest/USD'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/amount", methods=["GET", "POST"])
def money():
    result = None
    target = None
    usd = None
    error = None

    # 先呼叫 API 拿匯率資料
    try:  #捕捉錯誤(讓使用看不到紅色錯誤,程式繼續運行,可寫邏輯讓錯誤只顯示在後台)
        response = requests.get(API_URL)
        data = response.json()
        rates = data["conversion_rates"]   # 這裡包含所有幣別的匯率
    except Exception as e:
        rates = {}
        error = f"匯率 API 錯誤: {e}"

    if request.method == "POST" and rates:  #POST 提交表單
        try:
            usd = float(request.form.get("usd", "0").strip())
            target = request.form.get("currency")  #GET 獲取資料  .get("currency")：去抓取表單裡面名稱叫 currency 的欄位值
            if target not in rates:
                error = "請選擇正確的貨幣"
            else:
                result = usd * rates[target] #匯率  target = 使用者選擇的貨幣
        except ValueError:
            error = "請輸入數字"

    return render_template(
        "money.html",
        rates=rates,
        result=result,
        target=target,
        usd=usd,
        error=error
    )

if __name__ == "__main__":
    app.run("127.0.0.1", port=100, debug=True)