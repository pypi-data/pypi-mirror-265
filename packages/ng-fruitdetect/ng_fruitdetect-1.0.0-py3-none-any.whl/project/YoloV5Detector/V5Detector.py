import torch
import numpy as np
from project.models.experimental import attempt_load
from project.utils.general import non_max_suppression, scale_coords
from project.utils.datasets import letterbox
from project.utils.torch_utils import select_device
from project.utils.plots import plot_one_box
import random

class Detector:
    def __init__(self, weights_path, gpu_id="cpu", colors=None):
        self.weights = weights_path
        self.device = gpu_id
        self.device = select_device(self.device)
        model = attempt_load(self.weights, map_location=self.device)
        model.to(self.device).eval()
        model.float()
        self.m = model
        self.names = model.module.names if hasattr(
            model, 'module') else model.names
        self.colors_random = [[random.randint(0, 255) for _ in range(3)] for _ in self.names]
        self.colors = colors
        if self.colors:
            for color in self.colors:
                self.colors_random[color] = self.colors[color]

    def preprocess(self, img, img_size):
        img0 = img.copy()
        img = letterbox(img, new_shape=img_size)[0]
        img = img[:, :, ::-1].transpose(2, 0, 1)
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(self.device)
        img = img.float()
        img /= 255.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        return img0, img

    def detect(self, im, cls, thresh, img_size=640):

        im0, img = self.preprocess(im, img_size)

        pred = self.m(img, augment=False)[0]
        pred = pred.float()
        pred = non_max_suppression(pred, thresh, 0.4)
        pred_boxes = []
        for det in pred:
            if det is not None and len(det):
                det[:, :4] = scale_coords(
                    img.shape[2:], det[:, :4], im0.shape).round()

                for *x, conf, cls_id in det:
                    label_name = self.names[int(cls_id)]
                    if not label_name in cls:
                        continue
                    x1, y1 = int(x[0].cpu().detach().numpy().tolist()), int(x[1].cpu().detach().numpy().tolist())
                    x2, y2 = int(x[2].cpu().detach().numpy().tolist()), int(x[3].cpu().detach().numpy().tolist())
                    cls_id = int(cls_id.cpu().detach().numpy().tolist())
                    conf = round((conf.cpu().detach().numpy().tolist()), 4)
                    pred_boxes.append(
                        (x1, y1, x2, y2, cls_id, label_name, conf))
        return im, pred_boxes

    def draw_box(self, im, pred_boxes):
        if not pred_boxes:
            print("can not draw box cause no objects!!")
        else:
            for pred_box in pred_boxes:
                plot_one_box(pred_box, im, label=pred_box[5]+" "+str(pred_box[6]), color=self.colors_random[int(pred_box[4])], line_thickness=3)
        return im

    def print_result(self, pred_boxes):
        if not pred_boxes:
            print("can not print result cause no objects!!")
        else:
            for i, box in enumerate(pred_boxes):
                # 计算目标框的中心点坐标
                center_x = (box[0] + box[2]) / 2
                center_y = (box[1] + box[3]) / 2
                # print(
                #     "{}st object is {}, class id is {}, center_x:{}, center_y:{}, width:{}, height:{}, conf:{}".format(
                #         i, box[5], box[4],
                #         center_x, center_y,
                #         (box[2] - box[0]),
                #         (box[3] - box[1]),
                #         box[6]))
                return center_x,center_y









