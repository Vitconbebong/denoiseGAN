import time

import tensorflow as tf
import numpy as np

from utils import *
from model import *

from skimage import measure



def test(image):
    tf.reset_default_graph()

    global_step = tf.Variable(0, dtype=tf.int32, trainable=False, name='global_step')

    gen_in = tf.placeholder(shape=[None, BATCH_SHAPE[1], BATCH_SHAPE[2], BATCH_SHAPE[3]], dtype=tf.float32, name='generated_image')
    real_in = tf.placeholder(shape=[None, BATCH_SHAPE[1], BATCH_SHAPE[2], BATCH_SHAPE[3]], dtype=tf.float32, name='groundtruth_image')

    Gz = generator(gen_in)



    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)

        saver = initialize(sess)
        initial_step = global_step.eval()

        start_time = time.time()
        n_batches = 200
        total_iteration = n_batches * N_EPOCHS

        image = sess.run(tf.map_fn(lambda img: tf.image.per_image_standardization(img), image))
        image = sess.run(Gz, feed_dict={gen_in: image})
        image = np.resize(image[0][56:, :, :], [144, 256, 3])
        imsave('output', image)
        return image

def denoise(image_path):
    # Đọc hình ảnh từ file
    image = scipy.misc.imread(image_path, mode='RGB').astype('float32')
    
    # Thay đổi kích thước hình ảnh về (256, 256) bằng padding
    npad = ((56, 56), (0, 0), (0, 0))  # Padding cho chiều cao
    image = np.pad(image, pad_width=npad, mode='constant', constant_values=0)
    
    # Cắt hình ảnh về kích thước (256, 256)
    image = image[56:56 + 256, 0:256, :]  # Lấy phần trung tâm (256, 256)
    
    # Mở rộng chiều để có định dạng (1, 256, 256, 3)
    image = np.expand_dims(image, axis=0)
    
    print(image[0].shape)  # Kiểm tra kích thước hình ảnh
    output = test(image)    # Gọi hàm test với hình ảnh đã thay đổi kích thước
    return output




if __name__=='__main__':
    image = scipy.misc.imread(sys.argv[-1], mode='RGB').astype('float32')
    npad = ((56, 56), (0, 0), (0, 0))
    image = np.pad(image, pad_width=npad, mode='constant', constant_values=0)
    image = np.expand_dims(image, axis=0)
    print(image[0].shape)
    test(image)
