#センサのラズパイ送信処理 (テスト用)

import requests

url = "http://172.16.1.33:8000/api/upload" #URLは確認必須
files = {
    "image": open("sample2.jpg", "rb") #sample用の画像
}
data = {
    "device_id": "2",
    "temperature": "25.4",
    "humidity": "65.0"
}

response = requests.post(url, files=files, data=data) #指定したURLにこのデータをHTTPでPOST

print("Status Code:", response.status_code)
print("Response Text:", response.text)  # ← JSONでない場合の内容がここに出る

print(response.json())
