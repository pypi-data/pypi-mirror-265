"""
Standard - PyTorch modules (inheriting nn.Module) for standard blocks layering
(Sphynx Docstrings)
"""

__version__ = "0.1.0"


import torch
import torch.nn as nn

device = 'cuda' if torch.cuda.is_available() else 'cpu'


# ------------------------------------------- Multi-Layer Perceptrons (MLP) --------------------------------------------


# -------------------------------------------- Convolutional Blocks (CNN) ----------------------------------------------
class ConvBlock(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride, padding, activation, device=device):
        """Creates a Pytorch module comprising a Convolutional layer, followed by Batch-Normalization
        and an arbitrary activation function.

        :param in_channels  : Input tensor channels
        :type in_channels   : int
        :param out_channels : Output tensor channels
        :type out_channels  : int
        :param kernel_size  : Convolutional kernel (filter) dimensions
        :type kernel_size   : int or tuple
        :param stride       : Convolutional kernel (filter) striding step(s)
        :type stride        : int or tuple
        :param padding      : Input tensor padding quantity and/or mode
        :type padding       : int or tuple or str
        :param activation   : Output activation function (w. attributes), defaults to nn.ReLU()
        :param device       : Host device ('cpu' or 'cuda:X')
        :type device        : str
        """
        super(ConvBlock, self).__init__()
        self.layers = nn.ModuleDict()

        # 2D Convolutional Layer init
        self.layers['conv_2D'] = nn.Conv2d(in_channels=in_channels,
                                           out_channels=out_channels,
                                           kernel_size=kernel_size,
                                           stride=stride,
                                           padding=padding,
                                           bias=True).to(device)

        # 2D Batch-Normalization Layer init
        self.layers['batch_norm_2D'] = nn.BatchNorm2d(out_channels).to(device)

        # Non-Linear Activation init
        self.act_fun = activation.to(device)

        # Weights & Bias init
        for layer in self.layers.keys():
            try:
                nn.init.kaiming_normal_(self.layers[layer].weight, mode='fan_in')                                       # Kaiming-He (Normal) init

            except:
                pass                                                                                                    # Batch Layers could not be init!

            self.layers[layer].bias.data.fill_(0.)                                                                      # Biases initialization (0.)

    def forward(self, x):
        """Forward method

        :param x    : Input Tensor (batch_size, in_channels, height, width)
        :type x     : torch.Tensor
        :return     : Output Tensor (batch_size, out_channels, ..., ...)
        :rtype      : torch.Tensor
        """
        x = self.layers['conv_2D'](x)
        x = self.layers['batch_norm_2D'](x)
        x = self.act_fun(x)

        return x


class DWConv(nn.Module):
    def __init__(self, in_channels, kernel_size, stride, padding, activation=nn.ReLU(), device=device):
        """Creates a Pytorch module consisting of a Depth-wise (sub-grouped) Convolutional layer, followed by
        Batch-Normalization and an arbitrary activation. (see "Howard, A. et al. - "MobileNets: Efficient Convolutional
        Neural Networks for Mobile Vision Applications", https://arxiv.org/pdf/1704.04861.pdf)

        :param in_channels  : Input tensor channels
        :type in_channels   : int
        :param kernel_size  : Convolutional kernel (filter) dimensions
        :type kernel_size   : int or tuple
        :param stride       : Convolutional kernel (filter) striding step(s)
        :type stride        : int or tuple
        :param padding      : Input tensor padding quantity and/or mode
        :type padding       : int or tuple or str
        :param activation   : Output activation function (w. attributes), defaults to nn.ReLU()
        :param device       : Host device ('cpu' or 'cuda:X')
        :type device        : str
        """
        super(DWConv, self).__init__()
        self.layers = nn.ModuleDict()

        # 2D Convolutional Layer
        self.layers['dw_conv_2D'] = nn.Conv2d(in_channels=in_channels,
                                              out_channels=in_channels,
                                              kernel_size=kernel_size,
                                              stride=stride,
                                              padding=padding,
                                              groups=in_channels,                                                       # Re-concatenated groups output included
                                              bias=True).to(device)

        # 2D Batch Normalization
        self.layers['batch_norm_2D'] = nn.BatchNorm2d(in_channels).to(device)

        # Non-Linear Activation
        self.act_fun = activation.to(device)

        # Weights & Bias init
        for layer in self.layers.keys():
            try:
                nn.init.kaiming_normal_(self.layers[layer].weight, mode='fan_in')                                       # Kaiming-He (Normal) init
            except:
                pass                                                                                                    # Batch Layer could not be initialized!

            self.layers[layer].bias.data.fill_(0.)                                                                      # Biases initialization (0.)

    def forward(self, x):
        """Forward method

        :param x    : Input tensor (batch_size, in_channels, height, width)
        :type x     : torch.Tensor
        :returns    : Output tensor (batch_size, groups, ..., ...)
        :rtype      : torch.Tensor
        """
        x = self.layers['dw_conv_2D'](x)
        x = self.layers['batch_norm_2D'](x)
        x = self.act_fun(x)

        return x


class PWConv(nn.Module):
    def __init__(self, in_channels, out_channels, stride, padding, activation=nn.ReLU(), device=device):
        """Creates a Pytorch module consisting of a Point-wise (1D Kernel) Convolutional layer, followed by
        Batch-Normalization and an arbitrary activation. (see "Howard, A. et al. - "MobileNets: Efficient Convolutional
        Neural Networks for Mobile Vision Applications", https://arxiv.org/pdf/1704.04861.pdf)

        :param in_channels  : Input tensor channels
        :type in_channels   : int
        :param out_channels : Output tensor channels
        :type out_channels  : int
        :param stride       : Convolutional kernel (filter) striding step(s)
        :type stride        : int or tuple
        :param padding      : Input tensor padding quantity and/or mode
        :type padding       : int or tuple or str
        :param activation   : Output activation function (w. attributes), defaults to nn.ReLU()
        :param device       : Host device ('cpu' or 'cuda:X')
        :type device        : str
        """
        super(PWConv, self).__init__()
        self.layers = nn.ModuleDict()

        # 1D Convolutional Layer
        self.layers['pw_conv'] = nn.Conv2d(in_channels=in_channels,
                                           out_channels=out_channels,
                                           kernel_size=1,
                                           stride=stride,
                                           padding=padding,
                                           bias=True).to(device)

        # 2D Batch Normalization
        self.layers['batch_norm_2D'] = nn.BatchNorm2d(out_channels).to(device)

        # Non-Linear Activation
        self.act_fun = activation.to(device)

        # Weights & Bias init
        for layer in self.layers.keys():
            try:
                nn.init.kaiming_normal_(self.layers[layer].weight, mode='fan_in')                                       # Kaiming-He (Normal) init
            except:
                pass                                                                                                    # Batch Layer could not be initialized!

            self.layers[layer].bias.data.fill_(0.)                                                                      # Biases initialization (0.)

    def forward(self, x):
        """Forward method

        :param x    : Input tensor (batch_size, in_channels, height, width)
        :type x     : torch.Tensor
        :returns    : Output tensor (batch_size, out_channels, ..., ...)
        :rtype      : torch.Tensor
        """
        x = self.layers['pw_conv'](x)
        x = self.layers['batch_norm_2D'](x)
        x = self.act_fun(x)

        return x


class DWSepBlock(nn.Module):
    def __init__(self, in_channels, out_channels, dw_kernel_size, dw_stride, dw_padding, dw_activation=nn.ReLU(), pw_activation=nn.ReLU(), device=device):
        """Creates a Pytorch module comprising a Depth-wise ConvBlock, followed by a Point-wise ConvBlock.
        It is called Depth-wise Separable Convolution, and it is the basic building module of a MobileNet_V1 Architecture.
        (see F. Chollet - "Xception: Deep Learning with Depthwise Separable Convolutions", https://arxiv.org/pdf/1610.02357.pdf
        & A.G. Howard et al. - "MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications",
        https://arxiv.org/pdf/1704.04861v1.pdf)

        :param in_channels      : Input tensor channels
        :type in_channels       : int
        :param out_channels     : Output tensor channels
        :type out_channels      : int
        :param dw_kernel_size   : Convolutional kernel (filter) dimensions
        :type dw_kernel_size    : int or tuple
        :param dw_stride        : Convolutional kernel (filter) striding step(s)
        :type dw_stride         : int or tuple
        :param dw_padding       : Input tensor padding quantity and/or mode
        :type dw_padding        : int or tuple or str
        :param dw_activation    : DWConv activation function (w. attributes), defaults to nn.ReLU()
        :param pw_activation    : PWConv activation function (w. attributes), defaults to nn.ReLU()
        :param device           : Host device ('cpu' or 'cuda:X')
        :type device            : str
        """
        super(DWSepBlock, self).__init__()
        self.layers = nn.ModuleDict()

        # Depth-wise convolutional block
        self.layers['DW_Conv_Block'] = DWConv(in_channels=in_channels,
                                              kernel_size=dw_kernel_size,
                                              stride=dw_stride,
                                              padding=dw_padding,
                                              activation=dw_activation,
                                              device=device)

        # Point-wise convolutional block
        self.layers['PW_Conv_Block'] = PWConv(in_channels=in_channels,
                                              out_channels=out_channels,
                                              stride=1,
                                              padding=0,
                                              activation=pw_activation,
                                              device=device)

    def forward(self, x):
        """Forward method

        :param x    : Input tensor (batch_size, in_channels, height, width)
        :type x     : torch.Tensor
        :return     : Output tensor (batch_size, out_channels, ..., ...)
        :rtype      : torch.Tensor
        """
        x = self.layers['DW_Conv_Block'](x)
        x = self.layers['PW_Conv_Block'](x)

        return x


# ----------------------------------------- Squeeze-and-Excitation Blocks (SE)------------------------------------------
def _make_divisible(value, divisor, min_value=None):
    """This function is taken from the original repository. It ensures that a PyTorch layer has a channel number that
    is integer divisible by "divisor".
    (see https://github.com/tensorflow/models/blob/master/research/slim/nets/mobilenet/mobilenet.py)


    :param value     : input value
    :type value      : int or float
    :param divisor   : input divisor
    :type divisor    : int
    :param min_value : minimum result value
    :type min_value  : int
    :return          : division result
    :rtype           : int or float
    """
    if min_value is None:
        min_value = divisor
    new_value = max(min_value, int(value + divisor / 2) // divisor * divisor)

    if new_value < 0.9 * value:                                                                                         # Make sure that rounding does not drop of >10%.
        new_value += divisor

    return new_value


class HardSigmoid(nn.Module):                                                                                           # Auxiliary activation
    def __init__(self, inplace=False):
        """Creates a rectified Sigmoid function.
        (see A.G.Howard - "Searching for MobileNetV3", https://arxiv.org/pdf/1905.02244.pdf)

        :param inplace  : ...for consistency w. PyTorch's activation functions
        :type inplace   : bool
        """
        super(HardSigmoid, self).__init__()
        self.act_fun = nn.ReLU6(inplace=inplace).to(device)

    def forward(self, x):
        """Forward method

        :param x    : Input tensor (batch_size, ...)
        :type x     : torch.Tensor
        :return out : Output tensor (batch_size, ...)
        :rtype out  : torch.Tensor
        """
        out = self.act_fun(x + 3) / 6

        return out


class HardSwish(nn.Module):                                                                                             # Auxiliary activation
    def __init__(self, inplace=False):
        """Creates a Piecewise linearly approximated Swish function.
        (see A.G.Howard - "Searching for MobileNetV3", https://arxiv.org/pdf/1905.02244.pdf)

        :param inplace  : ...for consistency w. PyTorch's activation functions
        :type inplace   : bool
        """
        super(HardSwish, self).__init__()
        self.sigmoid = HardSigmoid(inplace=inplace).to(device)

    def forward(self, x):
        """Forward method

        :param x    : Input tensor (batch_size, ...)
        :type x     : torch.Tensor
        :return out : Output tensor (batch_size, ...)
        :rtype out  : torch.Tensor
        """
        out = x * self.sigmoid(x)

        return out


class SquExBlock(nn.Module):
    def __init__(self, in_channels, reduction, activation, device=device):
        """Creates a Pytorch module consisting of a Squeeze-and-Excitation convolutional block w. an arbitrary output
        activation function. (see A.G.Howard - "Searching for MobileNetV3", https://arxiv.org/pdf/1905.02244.pdf)

        :param in_channels  : Input tensor channels
        :type in_channels   : int
        :param reduction    : Reduction factor for intermediate channels
        :type reduction     : int or float
        :param activation   : Output activation function (w. attributes), default should be HardSigmoid()
        :param device       : Host device ('cpu' or 'cuda:X')
        :type device        : str
        """
        super(SquExBlock, self).__init__()
        self.layers = nn.ModuleDict()

        # Layers Initialization
        self.layers['pool'] = nn.AdaptiveAvgPool2d(1).to(device)
        self.layers['fc_1'] = nn.Linear(in_channels, _make_divisible(in_channels // reduction, 8), device=device)
        self.act_fun_1 = nn.ReLU().to(device)
        self.layers['fc_2'] = nn.Linear(_make_divisible(in_channels // reduction, 8), in_channels, device=device)
        self.act_fun_2 = activation.to(device)

    def forward(self, x):
        """Forward method

        :param x    : Input tensor (batch_size, in_channels, height, width)
        :type x     : torch.Tensor
        :return     : Output tensor (batch_size, in_channels, height, width)
        :rtype      : torch.Tensor
        """
        b, c, _, _ = x.size()

        y = self.layers['pool'](x).view(b, c)
        y = self.layers['fc_1'](y)
        y = self.act_fun_1(y)
        y = self.layers['fc_2'](y)
        y = self.act_fun_2(y).view(b, c, 1, 1)

        # Scaling
        out = x * y

        return out
