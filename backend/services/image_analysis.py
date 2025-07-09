import os
import base64
import re
import requests
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key=" + api_key
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

def predict_congestion_and_comfort(
    congestion_level: int,
    num_queue_people: int,
    gender_ratio_bus : str,
    gender_ratio_queue : str,
    temperature: float,
    humidity: float
):
    prompt = (
        f"以下の条件に基づいて、バスの車内の予測快適度（1〜5）と予測混雑度（1〜5）を推定してください。\n"
        f"なお、快適度は1であると不快、5であると快適であり、混雑度は1であるとすいている、5であると混雑している, として判断してください。\n"
        f"・現在の混雑度: {congestion_level}\n"
        f"・列に並んでいる人数: {num_queue_people}\n"
        f"・バスに乗車している男女比: {gender_ratio_bus}\n"
        f"・列に並んでいる男女比: {gender_ratio_queue}\n"
        f"・温度: {temperature}℃\n"
        f"・湿度: {humidity}%\n\n"
        f"出力形式は次のようにしてください。またそれ以外は出力しないでください。:\n"
        f"快適度: <数値>, 予測混雑度: <数値>"
    )

    body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=body)
        response.raise_for_status()
        data = response.json()

        print("🔍 Gemini 推定API raw response:")
        from pprint import pprint
        pprint(data)

        # Gemini の応答テキスト取得
        text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        print("Gemini 推定出力:", text)

        # 快適度と混雑度の抽出
        comfort_match = re.search(r"快適度[:：]?\s*(\d+)", text)
        congestion_match = re.search(r"混雑度[:：]?\s*(\d+)", text)

        comfort_level = int(comfort_match.group(1)) if comfort_match else None
        predicted_congestion = int(congestion_match.group(1)) if congestion_match else None

        return comfort_level, predicted_congestion

    except Exception as e:
        print("Error in Gemini 推定API:", e)
        return None, None