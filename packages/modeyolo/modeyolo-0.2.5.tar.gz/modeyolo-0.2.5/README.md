# ModeYOLO Python Package

## Introduction
ModeYOLO is a versatile Python package designed for efficient color space transformations, dataset modification, and YOLO model training. It seamlessly integrates into your workflow, providing solutions for diverse machine learning applications in computer vision.


## Dependencies
ModeYOLO depends on the following libraries:
- Ultralytics (`ultralytics`)
- PyTorch (`torch`)
- os (`os`)
- opencv-python (`cv2`)

### Folder Structure
Before using the package, ensure that your source dataset follows the following folder structure:

```plaintext
dataset/
|-- train/
|   |-- images/
|   |-- labels/
|-- test/
|   |-- images/
|   |-- labels/
|-- val/
|   |-- images/
|   |-- labels/
|-- data.yaml
```

## ColorOperation Module (`ColorOperation.py`)

### Class: `colorcng`

#### Color Spaces: 
Currently we accepting this `['RGB', 'BGR', 'GRAY', 'CrCb', 'LAB', 'HSV']` Color Spaces. Each element in the list corresponds to a specific color space. Here's an explanation of each color space:

1. **RGB (Red, Green, Blue):** The standard color model used in most digital cameras and displays, where each pixel is represented by three values indicating the intensity of red, green, and blue.

2. **BGR (Blue, Green, Red):** Similar to RGB but with the order of color channels reversed. OpenCV, a popular computer vision library, uses BGR as its default color order.

3. **GRAY (Grayscale):** A single-channel color space where each pixel is represented by a single intensity value, typically ranging from black to white.

4. **CrCb:** A component of the YCbCr color space often used in image and video compression. It separates chrominance (color information) from luminance (brightness information).

5. **LAB:** The LAB color space represents colors independently of device-specific characteristics. It consists of three components: L* (luminance), a* (green to red), and b* (blue to yellow).

6. **HSV (Hue, Saturation, Value):** A color space that separates color information into three components: hue (the type of color), saturation (the intensity or vividness of the color), and value (brightness). 

#### Constructor
```python
def __init__(self, path: str, mode: str = 'all') -> None:
    """
    Initializes the colorcng object.

    Parameters:
    - path: str, path to the target directory.
    - mode: str, mode of operation ('all', 'rgb', 'bgr', 'gray', 'hsv', 'crcb', 'lab').
    """
```

#### Methods
1. `cng_rgb`
    ```python
    def cng_rgb(self, opt: str, img: np.ndarray, idx: int | str = 0) -> None:
        """
        Converts the image to RGB color space.

        Parameters:
        - opt: str, operation type ('train', 'test', 'val').
        - img: np.ndarray, input image.
        - idx: int | str, index for the output file name.
        """
    ```

2. `cng_bgr`
    ```python
    def cng_bgr(self, opt: str, img: np.ndarray, idx: int | str = 0) -> None:
        """
        Saves the image in BGR color space.

        Parameters:
        - opt: str, operation type ('train', 'test', 'val').
        - img: np.ndarray, input image.
        - idx: int | str, index for the output file name.
        """
    ```

3. `cng_gray`
    ```python
    def cng_gray(self, opt: str, img: np.ndarray, idx: int | str = 0) -> None:
        """
        Converts the image to grayscale.

        Parameters:
        - opt: str, operation type ('train', 'test', 'val').
        - img: np.ndarray, input image.
        - idx: int | str, index for the output file name.
        """
    ```

4. `cng_hsv`
    ```python
    def cng_hsv(self, opt: str, img: np.ndarray, idx: int | str = 0) -> None:
        """
        Converts the image to HSV color space.

        Parameters:
        - opt: str, operation type ('train', 'test', 'val').
        - img: np.ndarray, input image.
        - idx: int | str, index for the output file name.
        """
    ```

5. `cng_crcb`
    ```python
    def cng_crcb(self, opt: str, img: np.ndarray, idx: int | str = 0) -> None:
        """
        Converts the image to YCrCb color space.

        Parameters:
        - opt: str, operation type ('train', 'test', 'val').
        - img: np.ndarray, input image.
        - idx: int | str, index for the output file name.
        """
    ```

6. `cng_lab`
    ```python
    def cng_lab(self, opt: str, img: np.ndarray, idx: int | str = 0) -> None:
        """
        Converts the image to LAB color space.

        Parameters:
        - opt: str, operation type ('train', 'test', 'val').
        - img: np.ndarray, input image.
        - idx: int | str, index for the output file name.
        """
    ```

7. `execute`
    ```python
    def execute(self, opt: str, file: str, idx: int | str = 0) -> None:
        """
        Executes the specified color space transformation.

        Parameters:
        - opt: str, operation type ('train', 'test', 'val').
        - file: str, path to the input image.
        - idx: int | str, index for the output file name.
        """
    ```

## Dataset Modifier Module (`DatasetModifier.py`)

### Class: `InitModifier`

#### Constructor
```python
def __init__(self, target_directory: str = 'modified_dataset', src_directory: str = 'dataset', mode: str = 'all') -> None:
    """
    Initializes the InitModifier object.

    Parameters:
    - target_directory: str, path to the target directory.
    - src_directory: str, path to the source dataset directory.
    - mode: str, mode of operation ('all', 'rgb', 'bgr', 'gray', 'hsv', 'crcb', 'lab').
    """
```

#### Methods
1. `start_train`
    ```python
    def start_train(self) -> None:
        """
        Creates the modified training dataset.
        """
    ```

2. `start_test`
    ```python
    def start_test(self) -> None:
        """
        Creates the modified testing dataset.
        """
    ```

3. `start_val`
    ```python
    def start_val(self) -> None:
        """
        Creates the modified validation dataset.
        """
    ```

4. `reform_dataset`
    ```python
    def reform_dataset(self) -> None:
        """
        Reformats the entire dataset.
        """
    ```

### Example Usage

```python
# Import the InitModifier class
from ModeYOLO.DatasetModifier import InitModifier

# Create an InitModifier object
init_op = InitModifier(target_directory='modified_dataset', src_directory='dataset', mode='all')

# Create the modified dataset
init_op.reform_dataset()
```


## ModelTrain Module (`ModelTrain.py`)
### Class: `trainYOLO`
This submodule facilitates YOLO model training with various pre-trained models. Users can choose from a selection of YOLO models, specify training parameters, and seamlessly integrate it into their workflows.


### Pre-trained Models
The `trainYOLO` submodule supports training with various pre-trained YOLO models. Choose a model by entering the corresponding index when prompted. Here are the available models:

1. `yolov3u.pt`: YOLOv3 with upsampling
2. `yolov5nu.pt`: YOLOv5 with narrow channels
3. `yolov5su.pt`: YOLOv5 with small model
4. `yolov5mu.pt`: YOLOv5 with medium model
5. `yolov5lu.pt`: YOLOv5 with large model
6. `yolov5xu.pt`: YOLOv5 with extra-large model
7. `yolov5n6u.pt`: YOLOv5 with narrow channels and 6x size
8. `yolov5s6u.pt`: YOLOv5 with small model and 6x size
9. `yolov5m6u.pt`: YOLOv5 with medium model and 6x size
10. `yolov5l6u.pt`: YOLOv5 with large model and 6x size
11. `yolov5x6u.pt`: YOLOv5 with extra-large model and 6x size
12. `yolov6n.pt`: YOLOv6 with narrow channels
13. `yolov6s.pt`: YOLOv6 with small model
14. `yolov6m.pt`: YOLOv6 with medium model
15. `yolov6l.pt`: YOLOv6 with large model
16. `yolov6l6.pt`: YOLOv6 with large model and 6x size
17. `yolov8n.pt`: YOLOv8 with narrow channels
18. `yolov8s.pt`: YOLOv8 with small model
19. `yolov8m.pt`: YOLOv8 with medium model
20. `yolov8l.pt`: YOLOv8 with large model
21. `yolov8x.pt`: YOLOv8 with extra-large model
22. `yolov9s.pt`: YOLOv9 with small model
23. `yolov9m.pt`: YOLOv9 with medium model
24. `yolov9c.pt`: YOLOv9 with complex model
25. `yolov9e.pt`: YOLOv9 with extra-large model

Choose a model based on your specific requirements and follow the on-screen instructions during training for optimal results.


### Example Usage
```python
# Import the trainYOLO class
from ModeYOLO.ModelTrain import trainYOLO

# Create a trainYOLO object
yolo_trainer = trainYOLO(target_directory='modified_dataset', src_directory='dataset', mode='all', data_path='./modified_dataset/data.yaml', epochs=1, imgsz=224)

# Train the YOLO model
yolo_trainer.train()

# Validate the trained model
yolo_trainer.val()
```

**Note:** Follow the on-screen instructions to choose a YOLO model for training.

## License
This project is licensed under the MIT License - see the [LICENSE]('https://github.com/colddsam/ModeYOLO/blob/main/LICENSE') file for details.

## Acknowledgments
- Mention any contributors or external libraries that inspired or helped with the development of ModeYOLO.

- Feel free to adjust the content as needed and let me know if you have further requirements!

- This example assumes that the source dataset is structured according to the specified folder structure. Adjust the paths and parameters accordingly based on your dataset structure.