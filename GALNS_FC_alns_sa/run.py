import os
import subprocess

# 지정된 폴더 경로
folder_path = r"C:\Users\User\OneDrive\바탕 화면\realrealrealreal-main\realrealrealreal-main"

# 폴더 내의 모든 하위 폴더를 검색하여 multi_modal.py 파일 실행
for root, dirs, files in os.walk(folder_path):
    if 'multi_modal.py' in files:
        script_path = os.path.join(root, 'multi_modal.py')
        try:
            # 터미널에서 Python 파일 실행 (Windows)
            subprocess.run(['start', 'cmd', '/c', 'python', script_path], shell=True)
            print(f"Successfully opened terminal and ran: {script_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error running {script_path}: {e}")
        except FileNotFoundError as e:
            print(f"Terminal application not found. Ensure you have a terminal application that supports")