from modeyolo.ColorOperation import colorcng
from tqdm import tqdm
import os
import yaml


class InitModifier(colorcng):
    def __init__(self, target_directory: str = 'modified_dataset', src_directory: str = 'dataset', mode: str = 'all') -> None:
        self.mode = mode.lower()
        self.dest = os.path.join(target_directory)
        self.src = os.path.join(src_directory)
        super().__init__(path=os.path.join(target_directory), mode=mode)
        if (os.path.exists(self.dest) and os.path.isdir(self.dest)):
            print("target dataset already exist!!!")
            try:
                with open(os.path.join(self.dest, 'data.yaml'), 'r') as f:
                    temp = yaml.safe_load(f)
                    if (os.path.exists(os.path.join(self.dest, 'train')) and os.path.isdir(os.path.join(self.dest, 'train'))):
                        temp['train'] = os.path.abspath(
                            os.path.join(self.dest, 'train', 'images'))
                    if (os.path.exists(os.path.join(self.dest, 'test')) and os.path.isdir(os.path.join(self.dest, 'test'))):
                        temp['test'] = os.path.abspath(
                            os.path.join(self.dest, 'test', 'images'))
                    if (os.path.exists(os.path.join(self.dest, 'val')) and os.path.isdir(os.path.join(self.dest, 'val'))):
                        temp['val'] = os.path.abspath(
                            os.path.join(self.dest, 'val', 'images'))
                with open(os.path.join(self.dest, 'data.yaml'), 'w') as yaml_file:
                    yaml.safe_dump(temp, yaml_file)
                print("file updated!!!")
            except Exception as e:
                print(f"there a error occurs : {e}")
        elif (not (os.path.exists(self.src) and os.path.isdir(self.src))):
            print("source dataset not exist!!!")
            exit()
        else:
            os.makedirs(target_directory)
            with open(os.path.join(self.src, 'data.yaml'), 'r') as f:
                temp = yaml.safe_load(f)
                if (os.path.exists(os.path.join(self.src, 'train')) and os.path.isdir(os.path.join(self.src, 'train'))):
                    temp['train'] = os.path.abspath(
                        os.path.join(self.dest, 'train', 'images'))
                if (os.path.exists(os.path.join(self.src, 'test')) and os.path.isdir(os.path.join(self.src, 'test'))):
                    temp['test'] = os.path.abspath(
                        os.path.join(self.dest, 'test', 'images'))
                if (os.path.exists(os.path.join(self.src, 'val')) and os.path.isdir(os.path.join(self.src, 'val'))):
                    temp['val'] = os.path.abspath(
                        os.path.join(self.dest, 'val', 'images'))
            with open(os.path.join(self.dest, 'data.yaml'), 'w') as yaml_file:
                yaml.safe_dump(temp, yaml_file)
    def extenstion_extract(self,file):
        
        idx=-1
        for i in range(len(file)-1,-1,-1):
            if file[i]=='.':
                break
            idx-=1
        return file[:idx],file[idx:]
    
    def start_train(self):
        src_train = os.path.join(self.src, 'train')
        dest_train = os.path.join(self.dest, 'train')
        os.makedirs(dest_train)
        os.makedirs(os.path.join(dest_train, 'images'))
        os.makedirs(os.path.join(dest_train, 'labels'))
        if (not (os.path.exists(src_train) and os.path.isdir(src_train))):
            print("train dataset not exist!!!")
        else:
            print('training data modification started..')
            for img in tqdm(os.listdir(os.path.join(src_train, 'images')),ncols=100,desc='training : '):
                split_img = self.extenstion_extract(file=img)
                if (os.path.exists(os.path.join(src_train, 'labels', f'{split_img[0]}.txt'))):
                    self.execute(opt='train', file=os.path.join(
                        src_train, 'images', img), idx=split_img[0])
                    with open(os.path.join(src_train, 'labels', f"{split_img[0]}.txt"), 'r') as file:
                        temp = file.read()

                    if self.mode == 'all':
                        for label_mode in ['RGB', 'BGR', 'GRAY', 'CrCb', 'LAB', 'HSV']:
                            with open(os.path.join(dest_train, 'labels', f"{label_mode}_{split_img[0]}.txt"), 'w') as file:
                                file.write(temp)
                    else:
                        with open(os.path.join(dest_train, 'labels', f"{self.mode.upper()}_{split_img[0]}.txt"), 'w') as file:
                            file.write(temp)
            print('training data modification completed!!')

    def start_test(self):
        src_test = os.path.join(self.src, 'test')
        dest_test = os.path.join(self.dest, 'test')
        os.makedirs(dest_test)
        os.makedirs(os.path.join(dest_test, 'images'))
        os.makedirs(os.path.join(dest_test, 'labels'))
        if (not (os.path.exists(src_test) and os.path.isdir(src_test))):
            print("test dataset not exist!!!")
        else:
            print('testing data modification started..')
            for img in tqdm(os.listdir(os.path.join(src_test, 'images')),ncols=100,desc='testing : '):
                split_img = self.extenstion_extract(file=img)
                if (os.path.exists(os.path.join(src_test, 'labels', f'{split_img[0]}.txt'))):
                    self.execute(opt='test', file=os.path.join(
                        src_test, 'images', img), idx=split_img[0])
                    with open(os.path.join(src_test, 'labels', f"{split_img[0]}.txt"), 'r') as file:
                        temp = file.read()

                    if self.mode == 'all':
                        for label_mode in ['RGB', 'BGR', 'GRAY', 'CrCb', 'LAB', 'HSV']:
                            with open(os.path.join(dest_test, 'labels', f"{label_mode}_{split_img[0]}.txt"), 'w') as file:
                                file.write(temp)
                    else:
                        with open(os.path.join(dest_test, 'labels', f"{self.mode.upper()}_{split_img[0]}.txt"), 'w') as file:
                            file.write(temp)
            print('testing data modification completed!!')

    def start_val(self):
        src_val = os.path.join(self.src, 'val')
        dest_val = os.path.join(self.dest, 'val')
        os.makedirs(dest_val)
        os.makedirs(os.path.join(dest_val, 'images'))
        os.makedirs(os.path.join(dest_val, 'labels'))
        if (not (os.path.exists(src_val) and os.path.isdir(src_val))):
            print("val dataset not exist!!!")
        else:
            print('validation data modification started..')
            for img in tqdm(os.listdir(os.path.join(src_val, 'images')),ncols=100,desc='validation : '):
                split_img = self.extenstion_extract(file=img)
                if (os.path.exists(os.path.join(src_val, 'labels', f'{split_img[0]}.txt'))):
                    self.execute(opt='val', file=os.path.join(
                        src_val, 'images', img), idx=split_img[0])
                    with open(os.path.join(src_val, 'labels', f"{split_img[0]}.txt"), 'r') as file:
                        temp = file.read()

                    if self.mode == 'all':
                        for label_mode in ['RGB', 'BGR', 'GRAY', 'CrCb', 'LAB', 'HSV']:
                            with open(os.path.join(dest_val, 'labels', f"{label_mode}_{split_img[0]}.txt"), 'w') as file:
                                file.write(temp)
                    else:
                        with open(os.path.join(dest_val, 'labels', f"{self.mode.upper()}_{split_img[0]}.txt"), 'w') as file:
                            file.write(temp)
            print('validation data modification completed!!')
    def reform_dataset(self):
        self.start_train()
        self.start_test()
        self.start_val()
