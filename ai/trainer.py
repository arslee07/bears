from imageai.Detection.Custom import DetectionModelTrainer
import os
# os.environ['CUDA_VISIBLE_DEVICES'] = '0'
# os.environ["SM_FRAMEWORK"] = "tf.keras"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

trainer = DetectionModelTrainer()
trainer.setModelTypeAsYOLOv3()
trainer.setDataDirectory(data_directory="/home/arslee/Projects/bears/ai/bears")
# Скачайте модель https://github.com/OlafenwaMoses/ImageAI/releases/download/essential-v4/pretrained-yolov3.h5
# Перетащите в bears/ai/
trainer.setTrainConfig(object_names_array=["bear"],
                       batch_size=4,
                       num_experiments=200,
                       train_from_pretrained_model="/home/arslee/Projects/bears/ai/pretrained-yolov3.h5")
trainer.trainModel()
