import tensorflow as tf
import time
sunflower_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/592px-Red_sunflower.jpg"
sunflower_path = tf.keras.utils.get_file('Red_sunflower', origin=sunflower_url)

img = tf.keras.preprocessing.image.load_img(
    sunflower_path, target_size=(300, 300)
)
img_array = tf.keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0) # Create a batch


model = tf.keras.models.load_model('CustomModel/tx.h5')
for l in model.variables:
    if(l.name=="conv2d_3/kernel:0"):
        filters=l
    if(l.name=="conv2d_3/bias:0"):
        bias=l
    if(l.name=="dense_3/kernel:0"):
        x=l
    if(l.name=="dense_3/bias:0"):
        y=l
   
c=tf.constant(([0.00392156862745098]))

img_array=tf.math.multiply(
    img_array, c, name=None
)
start_time = time.time()
xx1=tf.keras.backend.conv2d(img_array, filters,strides= (1, 1),padding='same',dilation_rate= (1, 1),data_format='channels_last')

xx2=tf.keras.backend.bias_add(xx1, bias)
xx2=tf.keras.backend.relu(
    xx2, alpha=0.0, max_value=None, threshold=0
)
xx3=tf.keras.backend.pool2d(xx2, pool_size=(2, 2), strides=(2, 2), padding='valid',data_format='channels_last')
print("--- %s seconds ---" % (time.time() - start_time))
xx4=tf.keras.backend.batch_flatten(xx3)

xx5=tf.keras.backend.dot(xx4,x)
xx6=tf.keras.backend.bias_add(xx5, y)
print("--- %s seconds ---" % (time.time() - start_time))
print(xx6)

stringh=tf.strings.as_string(
    xx3, precision=-1, scientific=False, shortest=False, width=-1, fill='',
    name=None
)
print(stringh)
cc=tf.strings.to_number(
    stringh, out_type=tf.dtypes.float32, name=None
)
print(cc)
