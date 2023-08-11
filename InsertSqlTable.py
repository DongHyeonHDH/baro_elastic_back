import pandas as pd
import mysql.connector
from pocket import pocket
from datetime import datetime
import string
import random

# MySQL 연결 정보 설정
info = pocket()
config = {
    'host': info.mysql_host,       # 호스트   
    'port': info.mysql_port, 
    'user': info.mysql_user,   # 사용자 이름
    'password': info.mysql_password,   # 비밀번호
    'database': 'baro_test_image'    # 사용할 데이터베이스 이름
}
# def convert_to_24_hour_format(input_time):
#     # 12-hour time format을 24-hour time format으로 변환
#     try:
#         converted_time = datetime.strptime(input_time, '%Y-%m-%d %I:%M:%S %p').strftime('%Y-%m-%d %H:%M:%S')
#         return converted_time
#     except ValueError:
#         # 시간 데이터가 초를 포함하지 않는 경우
#         converted_time = datetime.strptime(input_time, '%Y-%m-%d %I:%M ').strftime('%Y-%m-%d %H:%M:%S')
#         return converted_time  

def make_image_id(Imagedic):
    # 이미지 키 생성
    pid = ""
    while (True) :
        letters_set = string.ascii_letters
        num = random.randrange(1, 10) # 1부터 9 사이의 난수 생성
        random_list = random.sample(letters_set, num)
        random_str = f"I{''.join(random_list)}"

        try :
            Imagedic.get(image_id=random_str)
        except :
            pid = random_str
            Imagedic[pid] = 'ok'
            print(pid)
            break

    return pid

# MySQL 연결
conn = mysql.connector.connect(**config)

# 커서 생성
cursor = conn.cursor()

csv_file_path = 'C:\\Users\\knuprime-150\\OneDrive\\Documents\\grim\\ptsearch.csv'

positive = True
negative = False
adult = False
imagedic = {}
try:
    # CSV 파일 읽기
    df = pd.read_csv(csv_file_path, encoding='latin-1')

    # 데이터베이스에 데이터 삽입
    for _, row in df.iterrows():
        clip_skip_value = int(row['clip_skip']) if not pd.isna(row['clip_skip']) else 0
        denoising_strength_value = int(row['denoising_strength']) if not pd.isna(row['denoising_strength']) else 0        
        converted_time = row['timestamp']        
        if '\'' in row['prompt']:
            continue
        image_id = make_image_id(imagedic)
        try:
            query = f'''
                INSERT INTO IMAGE (image_id, user, image_file, seed, steps, sampler, cfg_scale, model_hash,
                  clip_skip, denoising_strength, image_time, adult) 
                VALUES ('{image_id}', '{row['user_id']}','{row['file_link']}',
                '{row['seed']}', '{row['steps']}', '{row['sampler']}', {row['cfg_scale']}, '{row['model_hash']}', {clip_skip_value}, {denoising_strength_value}, '{row['timestamp']}', {adult})'''
            
            positive_query= f'''
                INSERT INTO IMAGE_PROMPT (image_id, prompt, is_positive, prompt_time) 
                VALUES ('{image_id}', '{row['prompt']}', {positive} ,'{row['timestamp']}') 
            '''
            
            negative_query = f'''
                INSERT INTO IMAGE_PROMPT (image_id, prompt, is_positive, prompt_time) 
                VALUES ('{image_id}', '{row['negative_prompt']}',{negative} ,'{row['timestamp']}') 
            '''
                        
            try:
                cursor.execute(query)
                cursor.execute(positive_query)
                cursor.execute(negative_query)
                print('query ok')
            except:
                print('query가 되지 않네요')
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









