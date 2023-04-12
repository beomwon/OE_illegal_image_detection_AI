from PIL import Image
from io import BytesIO

import requests, pymysql, time, schedule
from multiprocessing import Process, Queue

import settings
import check_illegal_image
import check_illegal_sentence

TEST = True

conn = pymysql.connect(
    host=settings.MAIN_SERVER_DATABASE_ADDRESS, 
    user=settings.MAIN_SERVER_DATABASE_ID, 
    password=settings.MAIN_SERVER_DATABASE_PW, 
    db=settings.MAIN_SERVER_DATABASE_NAME, 
    charset='utf8', 
    cursorclass=pymysql.cursors.DictCursor)
cur = conn.cursor()

def command(state):
    sql = state
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

def extension2jpg(url:str) -> str:
    response = requests.get(url)
    im = Image.open(BytesIO(response.content))

    im = im.convert('RGB')
    im.save(f'temp.jpg','jpeg')

    return f'temp.jpg'

def get_ban_image_list(images:dict) -> list:
    table_and_indexs = []
    for table_and_index, target in images.items():
        path = extension2jpg(target)
        if check_illegal_image.isIllegal(path) or check_illegal_sentence.isIllegal('image', path): table_and_indexs.append(table_and_index)
    
    return table_and_indexs

def get_ban_text_list(texts:dict) -> list:
    table_and_indexs = []
    for table_and_index, target in texts.items():
        if check_illegal_sentence.isIllegal('text', target): table_and_indexs.append(table_and_index)

    return table_and_indexs

def make_dataset_to_be_detected() -> tuple:
    images, texts, from_minutes_ago = {}, {}, settings.FROM_MINUTES_AGO
    database_image_tables = settings.DATABASE_IMAGE_TABLES[0:1]
    database_text_tables = settings.DATABASE_TEXT_TABLES
    
    for v in database_image_tables:
        query = 'SELECT * FROM {} WHERE {} >= DATE_SUB(NOW(), INTERVAL {} MINUTE)'.format(v['table_name'], v['time'], from_minutes_ago)
        images.update({'{}_{}'.format(v['table_name'], table[v['table_index']]): table[v['target']] for table in command(query)})
    
    for v in database_text_tables:
        query = 'SELECT * FROM {} WHERE {} >= DATE_SUB(NOW(), INTERVAL {} MINUTE)'.format(v['table_name'], v['time'], from_minutes_ago)
        texts.update({'{}_{}'.format(v['table_name'], table[v['table_index']]): table[v['target']] for table in command(query)})
    
    return images, texts

def update_database() -> None:
    images, texts = make_dataset_to_be_detected()
    ban_post_list = get_ban_image_list(images) + get_ban_text_list(texts)

    payload = {'list':{'jungmo_photo':[], 'jungmo_post_image':[], 'jungmo_review_images':[], 'my_feed_image':[]}}
    for v in ban_post_list:
        table, index = v.split('_')
        payload['list'][table].append(int(index))
    
    if TEST:
        print(payload)
        requests.post(settings.UPDATE_DATABASE_API_URL_TEST, data=payload)
    else:
        requests.post(settings.UPDATE_DATABASE_API_URL_REAL, data=payload)

if __name__ == '__main__':
    if TEST:
        # test_line
        update_database()
    else:
        schedule.every(10).minutes.do(update_database)
        while True:
            schedule.run_pending()
            time.sleep(1)
    
    
