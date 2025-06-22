import os
import shutil
from pathlib import Path
from datetime import datetime

def organize_photos(folder_path):
    """사진 파일들을 시간순으로 정리하고 이름 변경"""
    # 지원하는 이미지 확장자
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.ico'}
    
    # 폴더 경로를 Path 객체로 변환
    base_folder = Path(folder_path)
    
    if not base_folder.exists():
        print(f"Error: There's no folder at'{folder_path}'.")
        return
    
    print(f"Converting pictures name in '{folder_path}'...")
    
    # 하위 폴더를 포함하여 모든 사진 파일 찾기
    photo_files = []
    
    for file_path in base_folder.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            # 파일의 마지막 수정/생성 시간 가져오기
            try:
                creation_time = file_path.stat().st_birthtime
            except AttributeError:
                creation_time = file_path.stat().st_mtime
            
            photo_files.append((file_path, creation_time))
    
    if not photo_files:
        print("Cannot find any photo files in the folder.")
        return
    
    # 시간순으로 정렬
    photo_files.sort(key=lambda x: x[1])
    
    print(f"found {len(photo_files)} photo files.")
    
    # 파일 이름 변경 및 이동
    processed_count = 0
    
    for index, (file_path, _) in enumerate(photo_files, 1):
        # 새 파일명 생성 (숫자 + 원본 확장자)
        new_filename = f"{index}{file_path.suffix}"
        new_file_path = base_folder / new_filename
        
        try:
            # 동일한 이름의 파일이 이미 존재하는 경우 처리
            counter = 1
            original_new_filename = new_filename
            while new_file_path.exists() and new_file_path != file_path:
                name_part = original_new_filename.rsplit('.', 1)[0]
                ext_part = original_new_filename.rsplit('.', 1)[1]
                new_filename = f"{name_part}_{counter}.{ext_part}"
                new_file_path = base_folder / new_filename
                counter += 1
            
            # 파일이 이미 올바른 위치에 있는 경우
            if file_path == new_file_path:
                print(f"Pass: {file_path.name} (Already in correct location/name)")
                processed_count += 1
                continue
            
            # 파일 이동 및 이름 변경
            shutil.move(str(file_path), str(new_file_path))
            print(f"Converted: {file_path.name} → {new_filename}")
            processed_count += 1
            
        except Exception as e:
            print(f"Error - {file_path.name}: {str(e)}")
    
    print(f"\nDone! {processed_count} of files are converted.")
    
    # 빈 폴더 정리
    cleanup_empty_folders(base_folder)

def cleanup_empty_folders(base_folder):
    """빈 폴더들을 제거"""
    print("\nCleaning empty folders...")
    
    removed_count = 0
    # 하위 폴더부터 역순으로 확인
    for folder_path in sorted(base_folder.rglob("*"), key=lambda p: len(p.parts), reverse=True):
        if folder_path.is_dir() and folder_path != base_folder:
            try:
                # 폴더가 비어있으면 제거
                if not any(folder_path.iterdir()):
                    folder_path.rmdir()
                    print(f"Cleaning empty folder: {folder_path.relative_to(base_folder)}")
                    removed_count += 1
            except Exception as e:
                print(f"Cannot delete empty folder of {folder_path.name}: {str(e)}")
    
    if removed_count > 0:
        print(f"{removed_count} of folders are deleted.")
    else:
        print("There's no empty folder to clean.")

if __name__ == "__main__":
    folder_path = input("Input photo folder: ").strip()
    
    # 경로에 따옴표가 있다면 제거
    folder_path = folder_path.strip('"').strip("'")
    
    if folder_path:
        organize_photos(folder_path)
    else:
        print("Please input proper folder path.")
        
    input("\nInput any keys to exit...")