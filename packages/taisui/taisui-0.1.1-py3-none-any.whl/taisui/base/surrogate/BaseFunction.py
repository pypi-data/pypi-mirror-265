# Copyright 2024 BIT AETAS
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import torch
import torch.nn as nn
def heaviside(x: torch.Tensor):
    '''
    :param x: the input tensor
    :return: the output tensor

    The heaviside function

    '''

    return (x >= 0).to(x)


class SurrogateFunctionBase(nn.Module):
    '''
    :param alpha: parameter to control smoothness of gradient
    :param spiking: output spikes. The default is ``True`` which means that using ``heaviside`` in forward
        propagation and using surrogate gradient in backward propagation. If ``False``, in forward propagation,
        using the primitive function of the surrogate gradient function used in backward propagation

    The base class of surrogate spiking function.

    '''
    def __init__(self, alpha, spiking=True):
        super().__init__()
        self.spiking = spiking
        self.alpha = alpha

    def set_spiking_mode(self, spiking: bool):
        self.spiking = spiking

    def extra_repr(self):
        return f'alpha={self.alpha}, spiking={self.spiking}'

    @staticmethod
    def spiking_function(x, alpha):
        raise NotImplementedError

    @staticmethod
    def primitive_function(x, alpha):
        raise NotImplementedError

    def forward(self, x: torch.Tensor):
        if self.spiking:
            return self.spiking_function(x, self.alpha)
        else:
            return self.primitive_function(x, self.alpha)