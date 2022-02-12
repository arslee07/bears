from imageai.Detection.Custom import CustomObjectDetection

detector = CustomObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("model.h5")
detector.setJsonPath("detection_config.json")
detector.loadModel()
detections = detector.detectObjectsFromImage(
    input_image="input.jpg", output_image_path="outuput.jpg"
)

for detection in detections:
    print(
        detection["name"],
        " : ",
        detection["percentage_probability"],
        " : ",
        detection["box_points"],
    )
