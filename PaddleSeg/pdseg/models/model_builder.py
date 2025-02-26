# coding: utf8
# copyright (c) 2019 PaddlePaddle Authors. All Rights Reserve.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import importlib
import struct

import paddle.fluid as fluid
import solver
from loss import multi_softmax_with_loss
from paddle.fluid.proto.framework_pb2 import VarType
from utils.config import cfg


class ModelPhase(object):
    """
    Standard name for model phase in PaddleSeg

    The following standard keys are defined:
    * `TRAIN`: training mode.
    * `EVAL`: testing/evaluation mode.
    * `PREDICT`: prediction/inference mode.
    * `VISUAL` : visualization mode
    """

    TRAIN = 'train'
    EVAL = 'eval'
    PREDICT = 'predict'
    VISUAL = 'visual'

    @staticmethod
    def is_train(phase):
        return phase == ModelPhase.TRAIN

    @staticmethod
    def is_predict(phase):
        return phase == ModelPhase.PREDICT

    @staticmethod
    def is_eval(phase):
        return phase == ModelPhase.EVAL

    @staticmethod
    def is_visual(phase):
        return phase == ModelPhase.VISUAL

    @staticmethod
    def is_valid_phase(phase):
        """ Check valid phase """
        if ModelPhase.is_train(phase) or ModelPhase.is_predict(phase) \
                or ModelPhase.is_eval(phase) or ModelPhase.is_visual(phase):
            return True

        return False


def map_model_name(model_name):
    name_dict = {
        "unet": "unet.unet",
        "deeplabv3p": "deeplab.deeplabv3p",
        "icnet": "icnet.icnet",
        "pspnet": "pspnet.pspnet",
    }
    if model_name in name_dict.keys():
        return name_dict[model_name]
    else:
        raise Exception(
            "unknow model name, only support unet, deeplabv3p, icnet")


def get_func(func_name):
    """Helper to return a function object by name. func_name must identify a
    function in this module or the path to a function relative to the base
    'modeling' module.
    """
    if func_name == '':
        return None
    try:
        parts = func_name.split('.')
        # Refers to a function in this module
        if len(parts) == 1:
            return globals()[parts[0]]
        # Otherwise, assume we're referencing a module under modeling
        module_name = 'models.' + '.'.join(parts[:-1])
        module = importlib.import_module(module_name)
        return getattr(module, parts[-1])
    except Exception:
        print('Failed to find function: {}'.format(func_name))
    return module


def softmax(logit):
    logit = fluid.layers.transpose(logit, [0, 2, 3, 1])
    logit = fluid.layers.softmax(logit)
    logit = fluid.layers.transpose(logit, [0, 3, 1, 2])
    return logit


def build_model(main_prog, start_prog, phase=ModelPhase.TRAIN):
    if not ModelPhase.is_valid_phase(phase):
        raise ValueError("ModelPhase {} is not valid!".format(phase))
    if ModelPhase.is_train(phase):
        width = cfg.TRAIN_CROP_SIZE[0]
        height = cfg.TRAIN_CROP_SIZE[1]
    else:
        width = cfg.EVAL_CROP_SIZE[0]
        height = cfg.EVAL_CROP_SIZE[1]

    image_shape = [cfg.DATASET.DATA_DIM, height, width]
    grt_shape = [1, height, width]
    class_num = cfg.DATASET.NUM_CLASSES

    with fluid.program_guard(main_prog, start_prog):
        with fluid.unique_name.guard():
            image = fluid.layers.data(
                name='image', shape=image_shape, dtype='float32')
            label = fluid.layers.data(
                name='label', shape=grt_shape, dtype='int32')
            mask = fluid.layers.data(
                name='mask', shape=grt_shape, dtype='int32')

            # use PyReader when doing traning and evaluation
            if ModelPhase.is_train(phase) or ModelPhase.is_eval(phase):
                py_reader = fluid.io.PyReader(
                    feed_list=[image, label, mask],
                    capacity=cfg.DATALOADER.BUF_SIZE,
                    iterable=False,
                    use_double_buffer=True)
            if cfg.MODEL.FP16:
                image = fluid.layers.cast(image, "float16")
            model_name = map_model_name(cfg.MODEL.MODEL_NAME)
            model_func = get_func("modeling." + model_name)
            logits = model_func(image, class_num)

            if ModelPhase.is_train(phase) or ModelPhase.is_eval(phase):
                avg_loss = multi_softmax_with_loss(logits, label, mask,
                                                   class_num)

            #get pred result in original size
            if isinstance(logits, tuple):
                logit = logits[0]
            else:
                logit = logits

            if logit.shape[2:] != label.shape[2:]:
                logit = fluid.layers.resize_bilinear(logit, label.shape[2:])

            # return image input and logit output for inference graph prune
            if ModelPhase.is_predict(phase):
                logit = softmax(logit)
                return image, logit

            out = fluid.layers.transpose(x=logit, perm=[0, 2, 3, 1])
            if cfg.MODEL.FP16:
                out = fluid.layers.cast(out, 'float32')
            pred = fluid.layers.argmax(out, axis=3)
            pred = fluid.layers.unsqueeze(pred, axes=[3])

            if ModelPhase.is_visual(phase):
                logit = softmax(logit)
                return pred, logit

            if ModelPhase.is_eval(phase):
                return py_reader, avg_loss, pred, label, mask

            if ModelPhase.is_train(phase):
                optimizer = solver.Solver(main_prog, start_prog)
                decayed_lr = optimizer.optimise(avg_loss)
                return py_reader, avg_loss, decayed_lr, pred, label, mask


def to_int(string, dest="I"):
    return struct.unpack(dest, string)[0]


def parse_shape_from_file(filename):
    with open(filename, "rb") as file:
        version = file.read(4)
        lod_level = to_int(file.read(8), dest="Q")
        for i in range(lod_level):
            _size = to_int(file.read(8), dest="Q")
            _ = file.read(_size)
        version = file.read(4)
        tensor_desc_size = to_int(file.read(4))
        tensor_desc = VarType.TensorDesc()
        tensor_desc.ParseFromString(file.read(tensor_desc_size))
    return tuple(tensor_desc.dims)
