import tensorflow as tf
import settings

def isIllegal(path:str) -> bool:
    bin = tf.io.read_file(path)
    image = tf.image.decode_jpeg(bin)
    image = tf.image.resize(image, [224, 224])
    return settings.ILLEGAL_IMAGE_DETECTION_MODEL.predict(image[None])[0][0] > settings.ILLEGAL_CLASSIFY_THRESHOLD

if __name__ == '__main__':
    pass