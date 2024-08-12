import os

# 폴더 경로 설정
folder_path = r"C:\Users\User\OneDrive\바탕 화면\realrealrealreal-main\realrealrealreal-main"

# 변경할 파일명 리스트
new_names = [10, 30, 70, 90]

# 파일명 변경 작업 수행
for i, new_name in enumerate(new_names):
    if i ==0:
        old_name = 'GALNS_BL - 복사본'
    else:
        old_name = 'GALNS_BL - 복사본' + f' ({i+1})'
    
    old_path = os.path.join(folder_path, old_name)
    new_path = os.path.join(folder_path, f'GALNS_BL{new_name}')
    
    # 폴더가 존재할 때만 이름 변경
    if os.path.exists(old_path):
        os.rename(old_path, new_path)

# 파일명 변경 작업 수행
for i, new_name in enumerate(new_names):
    if i ==0:
        old_name = 'GALNS_FLP - 복사본'
    else:
        old_name = 'GALNS_FLP - 복사본' + f' ({i+1})'
    
    old_path = os.path.join(folder_path, old_name)
    new_path = os.path.join(folder_path, f'GALNS_FLP{new_name}')
    
    # 폴더가 존재할 때만 이름 변경
    if os.path.exists(old_path):
        os.rename(old_path, new_path)


# 파일명 변경 작업 수행
for i, new_name in enumerate(new_names):
    if i ==0:
        old_name = 'GALNS_FC - 복사본'
    else:
        old_name = 'GALNS_FC - 복사본' + f' ({i+1})'
    
    old_path = os.path.join(folder_path, old_name)
    new_path = os.path.join(folder_path, f'GALNS_FC{new_name}')
    
    # 폴더가 존재할 때만 이름 변경
    if os.path.exists(old_path):
        os.rename(old_path, new_path)