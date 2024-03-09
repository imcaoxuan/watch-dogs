import MNN
import MNN.cv as cv2
import MNN.numpy as np

config = {}
config['precision'] = 'normal'
config['backend'] = 'CPU'
config['numThread'] = 1
rt = MNN.nn.create_runtime_manager((config,))
net = MNN.nn.load_module_from_file('yolov8n.mnn', [], [], runtime_manager=rt)


def inference(original_image):

    # net = MNN.nn.load_module_from_file(model, ['images'], ['output0'], runtime_manager=rt)
    ih, iw, _ = original_image.shape
    length = max((ih, iw))
    scale = length / 640
    # image = np.pad(original_image, [[0, length - ih], [0, length - iw], [0, 0]], mode='constant')
    image = cv2.resize(original_image, (640, 640), 0., 0., cv2.INTER_LINEAR, -1, [0., 0., 0.], [1./255., 1./255., 1./255.])
    input_var = np.expand_dims(image, 0)
    input_var = MNN.expr.convert(input_var, MNN.expr.NC4HW4)
    output_var = net.forward(input_var)
    output_var = MNN.expr.convert(output_var, MNN.expr.NCHW)
    output_var = output_var.squeeze()
    # output_var shape: [84, 8400]; 84 means: [cx, cy, w, h, prob * 80]
    cx = output_var[0]
    cy = output_var[1]
    w = output_var[2]
    h = output_var[3]
    probs = output_var[4:]
    # [cx, cy, w, h] -> [y0, x0, y1, x1]
    x0 = cx - w * 0.5
    y0 = cy - h * 0.5
    x1 = cx + w * 0.5
    y1 = cy + h * 0.5
    boxes = np.stack([x0, y0, x1, y1], axis=1)
    # get max prob and idx
    scores = np.max(probs, 0)
    class_ids = np.argmax(probs, 0)
    result_ids = MNN.expr.nms(boxes, scores, 100, 0.45, 0.25)
    print(result_ids.shape)
    # nms result box, score, ids
    result_boxes = boxes[result_ids]
    result_scores = scores[result_ids]
    result_class_ids = class_ids[result_ids]
    for i in range(len(result_boxes)):
        x0, y0, x1, y1 = result_boxes[i].read_as_tuple()
        y0 = int(y0 * scale)
        y1 = int(y1 * scale)
        x0 = int(x0 * scale)
        x1 = int(x1 * scale)
        print(result_class_ids[i])
        cv2.rectangle(original_image, (x0, y0), (x1, y1), (0, 0, 255), 2)
    # cv2.imwrite('static/r.png', original_image)
    return original_image, result_boxes, result_scores, result_class_ids