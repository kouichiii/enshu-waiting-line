import os
import google.generativeai as genai
from dotenv import load_dotenv
import base64


# 環境変数を読み込む
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash")

def analyze_image(file: bytes, device_id: str):
    # base64に変換
    image_base64 = base64.b64encode(file).decode("utf-8")

    # プロンプト（device_idに応じて変化）
    if device_id == "1":
        prompt = "このバスの車内画像から混雑度を1〜5で判定し、また男性と女性の比率を 'male:%,female:%' という形式で出力してください。"
    elif device_id == "2":
        prompt = "この画像に写っている待機列の人数を数え、また男性と女性の比率を 'male:%,female:%' という形式で出力してください。"
    else:
        return None, None

    # 画像 + テキストによるプロンプト実行
    response = model.generate_content([
        prompt,
        {
            "inline_data": {
                "mime_type": "image/jpeg",
                "data": image_base64
            }
        }
    ])

    # 期待される出力形式：
    # 混雑度: 3、男女比: male:60,female:40
    text = response.text.strip()

    # 結果をパース（安全のため簡易処理）
    import re
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
