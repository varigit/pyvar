# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
:platform: Unix/Yocto
:synopsis: Python Engine Class

.. moduleauthor:: Diego Dorta <diego.d@variscite.com>
"""
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
    def __init__(self, model_file_path=None, accelerated=True):
        self.model_file_path = model_file_path
        self.accelerated = accelerated
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.inference_time = None
        self.input_width = None
        self.input_height = None

        if model_file_path is not None:
            parser = ann.ITfLiteParser()
            network = parser.CreateNetworkFromBinaryFile(model_file_path)

            graph_id = parser.GetSubgraphCount() - 1
            
            input_names = parser.GetSubgraphInputTensorNames(graph_id)
            
            self.input_binding_info = parser.GetNetworkInputBindingInfo(graph_id, input_names[0])
            self.input_width = self.input_binding_info[1].GetShape()[1]
            self.input_height = self.input_binding_info[1].GetShape()[2]

            options = ann.CreationOptions()
            self.runtime = ann.IRuntime(options)

            preferredBackends = [ann.BackendId('CpuAcc'), ann.BackendId('CpuRef')]
            
            if accelerated is True:
                preferredBackends = [ann.BackendId('VsiNpu'), ann.BackendId('CpuAcc'), ann.BackendId('CpuRef')]
            
            opt_network, messages = ann.Optimize(
                network, preferredBackends, self.runtime.GetDeviceSpec(), ann.OptimizerOptions())

            net_id, _ = self.runtime.LoadNetwork(opt_network)

            output_names = parser.GetSubgraphOutputTensorNames(graph_id)
            
            self.output_binding_info = parser.GetNetworkOutputBindingInfo(0, output_names[0])
            self.output_tensors = ann.make_output_tensors([self.output_binding_info])
                   
    def set_input(self, image):
        self.input_tensors = ann.make_input_tensors([self.input_binding_info], [image])

    def get_output(self, squeeze=False):
        if squeeze:
            return np.squeeze(ann.workload_tensors_to_ndarray(self.output_tensors))

        return ann.workload_tensors_to_ndarray(self.output_tensors)[0][0]

    def get_result(self, category=None, labels=None): # change this function, remove labels, and use overlay
        if category is not None:
            if category is CLASSIFICATION:
                output = self.get_output()
                results = np.argsort(output)[::-1]
                for i in range(min(len(results), 5)):
                    print(f"[{i}] Object name = {labels[results[i]]}")

    def run_inference(self):
        timer = Timer()
        self.runtime.EnqueueWorkload(0, self.input_tensors, self.output_tensors) # ignores the warm-up time.
        with timer.timeit():
            self.runtime.EnqueueWorkload(0, self.input_tensors, self.output_tensors)
        self.inference_time = timer.time
