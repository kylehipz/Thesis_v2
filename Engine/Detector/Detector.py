import numpy as np
import tensorflow as tf
import cv2

class LPDetector:
    """License Plate Detector
    This class allows the user to detect license plates in an image.
    This uses deep learning for more accurate and efficient detection.
    See example.py
    ...

    Attributes
    ----------
    graph_def : It is the definition of the inference graph loaded to memory.
    sess : Tensorflow runtime session. This is needed to run the prediction of our graph_def

    Methods
    ----------
    detect(image, threshold)
        Uses the tensorflow session and graph_def to detect license plates on images.
        Accuracy of detected license plates less than the threshold are discarded.
    """
    
    def __init__(self, graph_path):
        """
        Parameters
        ----------
        graph_path : str
            File path of the graph to be loaded (mobilenet ssd v1)
        """
        f = tf.gfile.FastGFile(graph_path, 'rb')
        self.graph_def = tf.GraphDef()
        self.graph_def.ParseFromString(f.read())
        self.sess = tf.Session()
        self.sess.graph.as_default()
        tf.import_graph_def(self.graph_def, name='')
        f.close()

    def detect(self, image, threshold):
        """Detects possible license plates in an image
        Parameters
        ----------
        image : numpy array
            The image being detected on
        threshold : float
            Threshold of accuracy
        Returns
        -------
        license_plates_detected : list of tuples
            The coordinates of the license plates detected
        """

        license_plates_detected = list() # initialize list of license plates detected

        # Opencv uses BGR format. Tensorflow uses RGB so we need to convert it to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height = image.shape[0]
        width = image.shape[1]


        # running the graph and getting the output tensors - count of license plates, confidence of each
        # and coordinates of the bounding boxes, also convert the input image to a tensor
        out = self.sess.run([self.sess.graph.get_tensor_by_name('num_detections:0'),
                        self.sess.graph.get_tensor_by_name('detection_scores:0'),
                        self.sess.graph.get_tensor_by_name('detection_boxes:0'),
                        self.sess.graph.get_tensor_by_name('detection_classes:0')],
                       feed_dict={'image_tensor:0': image.reshape(1, image.shape[0], image.shape[1], 3)})

        # iterate over all the detected_images and then append to the license plates detected
        # self.license_plate_count = int(out[0][0])

        for i in range(int(out[0][0])):
            confidence = out[1][0][i]
            if confidence > threshold:
                bounding_boxes = [float(box) for box in out[2][0][i]]
                top_left = (int(bounding_boxes[1] * width), int(bounding_boxes[0] * height))
                bottom_right = (int(bounding_boxes[3] * width), int(bounding_boxes[2] * height))
                license_plate = [top_left, bottom_right]
                license_plates_detected.append(license_plate)
        
        return license_plates_detected

