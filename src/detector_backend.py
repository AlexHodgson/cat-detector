import os
import cv2

import torch
import torchvision
import torchvision.transforms as T

class Device:

    def __init__(self):

        # Choose where to run the net
        #Default to GPU if avaliable
        if torch.cuda.is_available():
            self.device = torch.device("cuda:0")
        else:
            self.device = torch.device("cpu")

        print("Using Device: " , self.device)


    def set_device(self, hardware_acceleration: bool):
        '''
        Changes where the calculations are being run between cpu and gpu

        hardware_acceleration: bool
        If the program will look for a gpu to do acceleration on
        '''
        
        if hardware_acceleration and torch.cuda.is_available():
            self.device = torch.device("cuda:0")
        else:
            self.device = torch.device("cpu")

        model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
        model.to(self.device)
        model.eval()

        print("Using Device: " , self.device)

device = Device()
# Prepare neural network
model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
model.to(device.device)
model.eval()

# Names corresponding to labels from net
COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
] 


def get_prediction(img, threshold):
    '''
    Pass an image to the network to get prediction of objects in it
    Could also provide bounding boxes
    '''

    # FIXME This is a very dumb way to put the neural net on the selected device, figure out why updating device outside the function isn't working
    model.to(device.device)
    model.eval()

    pred = model(img) # Pass the images to the model
    pred_class = [COCO_INSTANCE_CATEGORY_NAMES[i] for i in list(pred[0]['labels'].cpu().numpy())] # Get the Prediction Score
    pred_boxes = [[(i[0], i[1]), (i[2], i[3])] for i in list(pred[0]['boxes'].detach().cpu().numpy())] # Bounding boxes
    pred_score = list(pred[0]['scores'].detach().cpu().numpy())
    preds = [pred_score.index(x) for x in pred_score if x > threshold]

    if preds:
        pred_t = preds[-1] # Get list of index with score greater than threshold.
        pred_boxes = pred_boxes[:pred_t+1]
        pred_class = pred_class[:pred_t+1]
    return pred_boxes, pred_class

def find_cats(root_dir: str, files: list, threshold: float = 0.6):
    '''
    Sends images to a neural network to check if they contain cats

    root_dir: str
    Base directory to search

    files: list[str]
    List of files to scan for cats

    threshold: float
    The confidence threshold for the detection of a cat
    Must be between 0 and 1
    Default = 0.6

    hardware_acceleration: bool
    If the program will look for a gpu to do calculations on
    Default = True
    '''

    print("Using Device: " , device.device)

    if threshold < 0 or threshold > 1:
        raise ValueError("Threshold must be between 0 and 1")


    BATCH_SIZE = 5 # How many images to send to gpu at once
    batch = [] # Stores images in this batch
    batch_names = [] # Names of images stored in batch
    cat_pics = [] # List of images with cats in them

    for f in files:

        # Open images, resize, add to batch on GPU
        try:
            img = cv2.imread(os.path.join(root_dir,f))
            img = cv2.resize(img, (256,256))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            transform = T.Compose([T.ToTensor()])
            img = transform(img).to(device.device)

            batch.append(img)
            batch_names.append(f)

        except Exception as e:
            print(str(e))
            pass

        # Send batch to neural network
        if len(batch) == BATCH_SIZE or f == files[-1]:

            classes = []
            
            for img in batch:
                classes.append(get_prediction([img], threshold)[1])

            # Save names of files with cats
            for i in range(len(classes)):
                if 'cat' in classes[i]:
                    cat_pics.append(batch_names[i])

            # Reset batch
            batch = []
            batch_names=[]

    return cat_pics

