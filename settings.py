import json
from tensorflow import keras

with open('secrets.json', 'r') as f:
    secret = json.load(f)

# main
SCHEDULE_MINUTE = secret['SCHEDULE_MINUTE']
MAIN_SERVER_DATABASE_ADDRESS = secret['MAIN_SERVER_DATABASE_ADDRESS']
MAIN_SERVER_DATABASE_ID = secret['MAIN_SERVER_DATABASE_ID']
MAIN_SERVER_DATABASE_PW = secret['MAIN_SERVER_DATABASE_PW']
MAIN_SERVER_DATABASE_NAME = secret['MAIN_SERVER_DATABASE_NAME']

DATABASE_IMAGE_TABLES = secret['DATABASE_IMAGE_TABLES']
DATABASE_TEXT_TABLES = secret['DATABASE_TEXT_TABLES']

UPDATE_DATABASE_API_URL_TEST = secret['UPDATE_DATABASE_API_URL_TEST']
UPDATE_DATABASE_API_URL_REAL = secret['UPDATE_DATABASE_API_URL_REAL']

# check_illegal_sentence_in_image
ILLEGAL_WORD_FILE_PATH = secret['ILLEGAL_WORD_FILE_PATH']
NAVER_OCR_API_URL = secret['NAVER_OCR_API_URL']
NAVER_OCR_API_KEY = secret['NAVER_OCR_API_KEY']

ILLEGAL_WORD_COUNT_THRESHOLD = 0
ILLEGAL_WORD_SET = open(ILLEGAL_WORD_FILE_PATH,'r',encoding='UTF-8').read().split()

# check_illegal_image
ILLEGAL_CLASSIFY_THRESHOLD = 0.7

base = eval(secret['MODEL_BASE'])
ILLEGAL_IMAGE_DETECTION_MODEL = eval(secret['MODEL_LAYER'])

base.trainable = False
ILLEGAL_IMAGE_DETECTION_MODEL.compile('adam', 'binary_crossentropy', metrics='accuracy')
ILLEGAL_IMAGE_DETECTION_MODEL.load_weights('illegal_image_detection.h5')
