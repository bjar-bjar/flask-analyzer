from flask import Flask, request, jsonify
import traceback
import yfinance as yf
import os
from datetime import datetime

app = Flask(__name__)


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        ticker = data.get("ticker")
        buy_price = float(data.get("buy_price"))
        stop_price = float(data.get("stop_price"))
        buy_date_str = data.get("buy_date")
        buy_date = datetime.strptime(buy_date_str, "%Y-%m-%d")

        stock = yf.Ticker(ticker)
        hist = stock.history(period="30d")

        if hist.empty:
            return jsonify({"error": "해당 종목의 데이터를 가져올 수 없습니다."})

        hist_after_buy = hist[hist.index >= buy_date]

        if hist_after_buy.empty:
            return jsonify({"error": "매수일 이후의 주가 데이터가 없습니다."})

        closes = hist_after_buy["Close"].tolist()
        current_price = closes[-1]
        highest_price = max(closes)
        lowest_price = min(closes)

        result = {
            "종목코드": ticker,
            "현재가": round(current_price),
            "최고가": round(highest_price),
            "최저가": round(lowest_price),
            "손절도달": lowest_price <= stop_price,
            "현재수익률": round((current_price - buy_price) / buy_price * 100, 2),
            "최고수익률": round((highest_price - buy_price) / buy_price * 100, 2)
        }

        return jsonify(result)
    except Exception as e:
        print("🔥 서버 내부 오류 발생:")
        traceback.print_exc()
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)