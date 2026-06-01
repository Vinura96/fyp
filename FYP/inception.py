import tensorflow as tf
import time

model = tf.keras.models.load_model('incep.h5')
sunflower_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/592px-Red_sunflower.jpg"
sunflower_path = tf.keras.utils.get_file('Red_sunflower', origin=sunflower_url)

img = tf.keras.preprocessing.image.load_img(
    sunflower_path, target_size=(300, 300)
)
img_array = tf.keras.preprocessing.image.img_to_array(img)

img_array = tf.expand_dims(img_array, 0) # Create a batch


start_time = time.time()
predictions = model.predict(img_array)
print("--- %s seconds ---" % (time.time() - start_time))
score = tf.nn.softmax(predictions[0])
