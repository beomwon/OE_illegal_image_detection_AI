import requests, uuid, time, json
from konlpy.tag import Okt
import settings

def ocr(image_file:str) -> json:
    api_url = settings.NAVER_OCR_API_URL
    secret_key = settings.NAVER_OCR_API_KEY

    request_json = {
        'images': [{'format': 'jpg', 'name': 'demo'}],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }

    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    files = [('file', open(image_file,'rb'))]
    headers = {'X-OCR-SECRET': secret_key}
    response = requests.request("POST", api_url, headers=headers, data = payload, files = files).json()
    return response

def count_illegal_word(target_type:str, target) -> int:
    text = ''
    if target_type == 'json':
        for v in target['images'][0]['fields']:
            text += v['inferText'] + ' '
    elif target_type == 'text':
        text = target
    
    return sum(map(text.count, settings.ILLEGAL_WORD_SET))

    # OKT 사용 로직
    # okt = Okt()
    # for v in okt.pos(text): # URL
    #     if v[0] in settings.ILLEGAL_WORD_SET:
    #         count += 1
            # print(v[0], '검출')

    # for v in okt.pos(text): # URL
    #     if v[0] in settings.ILLEGAL_WORD_SET or v[1] == 'URL':
    #         count += 1
    #         # print(v[0], '검출')

    # return count

def isIllegal(type:str, target:str) -> bool:
    if type == 'image':
        return count_illegal_word('json', ocr(target)) > settings.ILLEGAL_WORD_COUNT_THRESHOLD
    elif type == 'text':
        return count_illegal_word('text', target) > settings.ILLEGAL_WORD_COUNT_THRESHOLD

if __name__ == '__main__':
    pass
