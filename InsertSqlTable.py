import pandas as pd
import mysql.connector
# MySQL 연결 정보 설정
config = {
    'host': '13.125.224.184',       # 호스트
    'port': '51046', # 포트번호 -> 이렇게 연결하는게 아니면 수정
    'user': 'hdh',   # 사용자 이름
    'password': '4202',   # 비밀번호
    'database': 'baro_grim_practice'    # 사용할 데이터베이스 이름
}

# MySQL 연결
conn = mysql.connector.connect(**config)

# 커서 생성
cursor = conn.cursor()

csv_file_path = 'C:\\Users\\knuprime-150\\OneDrive\\Documents\\grim\\civit.csv'

try:
    # CSV 파일 읽기
    df = pd.read_csv(csv_file_path, encoding='latin-1')

    # 데이터베이스에 데이터 삽입
    for _, row in df.iterrows():
        clip_skip_value = int(row['clip_skip']) if not pd.isna(row['clip_skip']) else 0
        denoising_strength_value = int(row['denoising_strength']) if not pd.isna(row['denoising_strength']) else 0
        if '\'' in row['prompt']:
            continue
        
        try:
            query = f"INSERT INTO IMAGE (user_id, name, file_link, prompt, negative_prompt, timestamp, steps,sampler, cfg_scale, seed, model_hash, clip_skip, denoising_strength) VALUES ('{row['user_id']}', '{row['name']}','{row['file_link']}', '{row['prompt']}', '{row['negative_prompt']}', '{row['timestamp']}', {row['steps']}, '{row['sampler']}', {row['cfg_scale']}, {row['seed']}, '{row['model_hash']}', {clip_skip_value}, {denoising_strength_value})"
            
            cursor.execute(query)
        except:
            continue

    # 변경 사항 커밋
    conn.commit()
    print("데이터가 성공적으로 삽입되었습니다.")
except mysql.connector.Error as err:
    print(f"데이터 삽입 오류: {err}")
finally:
    # 커넥션과 커서 닫기
    cursor.close()
    conn.close()
