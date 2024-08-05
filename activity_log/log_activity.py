import json
import os
from datetime import datetime

# JSON 파일 경로 설정
json_file = 'activity_log/json_record/activity_log.json'

def log_activity_to_json():
    # 오늘 날짜 형식 설정
    today = datetime.now().strftime("%Y-%m-%d")

    # JSON 파일에서 기존 데이터를 불러오거나 새로 생성
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = {}

    ########### 기록 수정 영역 
    # 당일 활동 데이터가 이미 있는지 확인하고 새로운 데이터 추가
    if today in data:
        # 당일 새로운 기록을 추가할 경우
        entry_number = len(data[today]) + 1
        data[today][f'entry_{entry_number}'] = {
            "record": "새로운 기록 추가",
            "notes": "새로운 메모 추가"
        }
    else:
        # 당일 첫 번째 활동 데이터
        data[today] = {
            "entry_1": {
                "record": "Daily_Check",
                "notes": "활동기록 코드 만들기"
            }
        }

    # JSON 파일에 데이터 저장
    os.makedirs(os.path.dirname(json_file), exist_ok=True)
    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"{today} 활동이 JSON 파일에 기록되었습니다.")

def update_markdown_from_json():
    # Markdown 파일 이름 설정 (현재 연도-월)
    month_file = datetime.now().strftime("%Y-%m") + '.md'

    # JSON 파일에서 데이터를 읽어오기
    if not os.path.exists(json_file):
        print("JSON 파일이 없습니다. 먼저 JSON 파일을 생성해주세요.")
        return

    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 새로운 달의 Markdown 파일에 기록
    with open(month_file, 'w', encoding='utf-8') as file:
        # Markdown 파일에 헤더와 표 헤더 작성
        file.write(f"# {datetime.now().strftime('%Y-%m')} 활동 기록\n\n")
        file.write("| 날짜       | Record                        | 비고             |\n")
        file.write("|------------|-------------------------------|------------------|\n")

        # JSON 데이터를 기반으로 각 행 작성
        for date, activities in sorted(data.items()):
            for entry, activity in activities.items():
                record = activity['record']
                notes = activity['notes']
                
                # Markdown 표 형식으로 기록
                file.write(f"| {date} | {record} | {notes} |\n")

    print(f"{month_file} 파일이 업데이트되었습니다.")

if __name__ == "__main__":
    log_activity_to_json()
    update_markdown_from_json()