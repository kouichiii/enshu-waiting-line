import os
import base64
import re
import requests
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=" + api_key
HEADERS = {
    "Content-Type": "application/json"
}

def analyze_image(file: bytes, device_id: str):
    # 画像データを base64 にエンコード
    image_base64 = base64.b64encode(file).decode("utf-8")

    # デバイスごとのプロンプト
    if device_id == "1":
        prompt = "このバスの車内画像から混雑度を1〜5で判定し、また男性と女性の比率を 'male:%,female:%' という形式で出力してください。"
    elif device_id == "2":
        prompt = "この画像に写っている待機列の人数を数え、また男性と女性の比率を 'male:%,female:%' という形式で出力してください。"
    else:
        return None, None

    # REST API 用の JSON ボディ
    body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_base64
                        }
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=body)
        response.raise_for_status()
        data = response.json()

        print("🔍 Gemini API raw response:")
        from pprint import pprint
        pprint(data)

        # Gemini の応答テキスト
        text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        print("Gemini Text Output:", text)

        # 男女比と数値の抽出
        gender_match = re.search(r"male:\s*\d+%?,\s*female:\s*\d+%?", text)
        number_match = re.search(r"\d+", text)

        if device_id == "1" and number_match and gender_match:
            congestion_level = int(number_match.group())
            gender_ratio = gender_match.group()
            return congestion_level, gender_ratio

        if device_id == "2" and number_match and gender_match:
            num_people = int(number_match.group())
            gender_ratio = gender_match.group()
            return num_people, gender_ratio

        return None, None

    except Exception as e:
        print("Error calling Gemini REST API:", e)
        return None, None
