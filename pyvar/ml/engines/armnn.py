# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
:platform: Unix/Yocto
:synopsis: Class to handle Arm NN inference engine.

.. moduleauthor:: Diego Dorta <diego.d@variscite.com>
"""

import os
import sys

import numpy as np

try:
    import pyarmnn as ann
except ImportError:
    sys.exit("No ArmNN Runtime module found!")

from pyvar.ml.config import CLASSIFICATION
from pyvar.ml.config import DETECTION
from pyvar.ml.utils.timer import Timer

class ArmNNInterpreter:
    """
    :ivar interpreter: Arm NN interpreter;
    :ivar input_details: input details from model;
    :ivar output_details: output details from inference;
    :ivar result: results from inference;
    :ivar inference_time: inference time;
    :ivar model_file_path: path to the machine learning model;
    :ivar input_width: size of model input width;
    :ivar input_height: size of model input height;
    :ivar category: model category (classification or detection);
    :ivar accelerated: runs inference on NPU or CPU.
    """
    def __init__(self, model_file_path=None, accelerated=True, category=None):
        """
        Constructor method for the Arm NN class.
        """
        if not os.path.isfile(model_file_path):
            raise ValueError("Must pass a labels file")
        if not model_file_path.endswith(".tflite"):
            raise TypeError(f"Expects {model_file_path} to be a text file")
        self.model_file_path = model_file_path
        self.accelerated = accelerated
        self.category = category
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.inference_time = None
        self.input_width = None
        self.input_height = None
        self.result = None

        parser = ann.ITfLiteParser()
        network = parser.CreateNetworkFromBinaryFile(model_file_path)

        graph_id = parser.GetSubgraphCount() - 1

        input_names = parser.GetSubgraphInputTensorNames(graph_id)

        self.input_binding_info = parser.GetNetworkInputBindingInfo(
                                                   graph_id, input_names[0])
        self.input_width = self.input_binding_info[1].GetShape()[1]
        self.input_height = self.input_binding_info[1].GetShape()[2]

        options = ann.CreationOptions()
        self.runtime = ann.IRuntime(options)

        preferredBackends = [ann.BackendId('CpuAcc'),
                             ann.BackendId('CpuRef')]

        if accelerated is True:
            preferredBackends = [ann.BackendId('VsiNpu'),
                                 ann.BackendId('CpuAcc'),
                                 ann.BackendId('CpuRef')]

        opt_network, messages = ann.Optimize(
            network, preferredBackends,
            self.runtime.GetDeviceSpec(), ann.OptimizerOptions())

        net_id, _ = self.runtime.LoadNetwork(opt_network)

        output_names = parser.GetSubgraphOutputTensorNames(graph_id)

        self.output_binding_info = parser.GetNetworkOutputBindingInfo(
                                                    0, output_names[0])
        if self.category is not None:
            if self.category is CLASSIFICATION:
                self.output_tensors = ann.make_output_tensors(
                                               [self.output_binding_info])
            elif self.category is DETECTION:
                 output_list = []
                 for out in output_names:
                     output_list.append(
                            parser.GetNetworkOutputBindingInfo(graph_id, out))
                     self.output_tensors = ann.make_output_tensors(output_list)

    def set_input(self, image):
        """
        Set the image/frame into the input tensor to be inferenced.
        """
        self.input_tensors = ann.make_input_tensors(
                                      [self.input_binding_info], [image])

    def get_output(self, index, squeeze=False):
        """
        Get the result after running the inference.

        Args:
            index (int): index of the result
            squeeze (bool): result is squeezed or not.

        Returns:
            if **squeeze**, return **squeezed**
            if **not**, return **not squeeze**
        """
        if squeeze:
            return np.squeeze(
                      ann.workload_tensors_to_ndarray(
                                   self.output_tensors)[index][0])
        return ann.workload_tensors_to_ndarray(self.output_tensors)[index][0]

    def get_result(self, category=None):
        """
        Get the result from the output details.

        Args:
            category (str): model category (classification or detection);

        Returns:
            if **success**, return **True**
            if **not**, return **False**
        """
        if self.category is not None:
            if self.category is CLASSIFICATION:
                output = self.get_output(0)
                top_k = np.argsort(output)[-5:][::-1]
                self.result = []
                for i in top_k:
                    score = float(output[i] / 255.0)
                    self.result.append((i, score))
                return True
            elif self.category is DETECTION:
                positions = self.get_output(0, True)
                classes = self.get_output(1, True)
                scores = self.get_output(2, True)
                self.result = []
                for idx, score in enumerate(scores):
                    if score > 0.5:
                        self.result.append({'pos': positions[idx],
                                            '_id': classes[idx]})
                return True

    def run_inference(self):
        """
        Runs inference on the image/frame set in the set_input() method.
        """
        timer = Timer()
        self.runtime.EnqueueWorkload(
            0, self.input_tensors, self.output_tensors) # ignores the warm-up time.
        with timer.timeit():
            self.runtime.EnqueueWorkload(0, self.input_tensors, self.output_tensors)
        self.inference_time = timer.time
