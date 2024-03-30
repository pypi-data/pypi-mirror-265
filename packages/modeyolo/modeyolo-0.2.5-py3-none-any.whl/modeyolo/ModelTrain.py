from ultralytics import YOLO
from modeyolo.DatasetModifier import InitModifier
import os
import yaml

class trainYOLO:
    
    def __init__(self, target_directory: str = 'modified_dataset', src_directory: str = 'dataset', mode: str = 'all', data_path: str = './modified_dataset/data.yaml', epochs: int = 1, imgsz: int = 224,operation:int=-1) -> None:
        models_names = [
            'yolov3u.pt',
            'yolov5nu.pt',
            'yolov5su.pt',
            'yolov5mu.pt',
            'yolov5lu.pt',
            'yolov5xu.pt',
            'yolov5n6u.pt',
            'yolov5s6u.pt',
            'yolov5m6u.pt',
            'yolov5l6u.pt',
            'yolov5x6u.pt',
            'yolov6n.pt',
            'yolov6s.pt',
            'yolov6m.pt',
            'yolov6l.pt',
            'yolov6l6.pt',
            'yolov8n.pt',
            'yolov8s.pt',
            'yolov8m.pt',
            'yolov8l.pt',
            'yolov8x.pt',
            'yolov9s.pt',
            'yolov9m.pt',
            'yolov9c.pt',
            'yolov9e.pt'
        ]
        if operation not in range(0,len(models_names)):
            print('Enter the model name that you want to train\nYou can take refer to out documentation page for more information  about the model')
            for idx,name in enumerate(models_names):
                print(f'press {idx} for {name} model')
            operation=int(input('enter the index : '))
        try:
            self.model_name=models_names[operation]
        except Exception as e:
            print(f"operation is not possible due to this error : {e}")
            exit()
        self.data_path=data_path
        self.epochs=epochs
        self.imgzs=imgsz
        self.model=YOLO(self.model_name)
        
        try: 
            if(not os.path.exists(self.data_path)):
                datasetreform=InitModifier(target_directory=target_directory,src_directory=src_directory,mode=mode)
                datasetreform.reform_dataset()
            else:
                with open(os.path.join(target_directory, 'data.yaml'), 'r') as f:
                    temp = yaml.safe_load(f)
                    if (os.path.exists(os.path.join(target_directory, 'train')) and os.path.isdir(os.path.join(target_directory, 'train'))):
                        temp['train'] = os.path.abspath(
                            os.path.join(target_directory, 'train', 'images'))
                    if (os.path.exists(os.path.join(target_directory, 'test')) and os.path.isdir(os.path.join(target_directory, 'test'))):
                        temp['test'] = os.path.abspath(
                            os.path.join(target_directory, 'test', 'images'))
                    if (os.path.exists(os.path.join(target_directory, 'val')) and os.path.isdir(os.path.join(target_directory, 'val'))):
                        temp['val'] = os.path.abspath(
                            os.path.join(target_directory, 'val', 'images'))
                with open(os.path.join(target_directory, 'data.yaml'), 'w') as yaml_file:
                    yaml.safe_dump(temp, yaml_file)
                print("file updated!!!")
        except Exception as e:
            print(f"their is a error to create the dataset : {e}")
            exit()
        
    def train(self)->None:
        results=self.model.train(data=self.data_path,epochs=self.epochs,imgsz=self.imgzs)
        print(results)
    
    def val(self)->None:
        try:
            self.model.val()
        except Exception as e:
            print(f"there is a error while trying to execute this code  : {e}")
            
        
