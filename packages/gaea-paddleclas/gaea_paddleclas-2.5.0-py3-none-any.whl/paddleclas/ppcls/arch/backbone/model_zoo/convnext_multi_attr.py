#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : convnext.py
@Author        : jiangnan19
@Date          : 2022/5/10
@Description   :
"""
# Code was based on https://github.com/facebookresearch/ConvNeXt

import paddle
import paddle.nn as nn
import paddle.nn.functional as F
from ppcls.utils.save_load import load_dygraph_pretrain, load_dygraph_pretrain_from_url
import numpy as np

MODEL_URLS = {
    "ConvNext_Multi_Attr": "",  
}

__all__ = list(MODEL_URLS.keys())

trunc_normal_ = nn.initializer.TruncatedNormal(std=0.02)
zeros_ = nn.initializer.Constant(value=0.0)
ones_ = nn.initializer.Constant(value=1.0)
kaiming_ = nn.initializer.KaimingNormal()
normal_ = nn.initializer.Normal(mean=0.0, std=0.02)


class Identity(nn.Layer):
    """
    indentity class
    """
    def __init__(self):
        """
        init
        """
        super().__init__()

    def forward(self, x):
        """
        forward
        """
        return x


def drop_path(x, drop_prob=0.0, training=False):
    """
    drop path func
    """
    if drop_prob == 0.0 or not training:
        return x
    keep_prob = paddle.to_tensor(1 - drop_prob)
    shape = (paddle.shape(x)[0], ) + (1, ) * (x.ndim - 1)
    random_tensor = keep_prob + paddle.rand(shape, dtype=x.dtype)
    random_tensor = paddle.floor(random_tensor)  # binarize
    output = x.divide(keep_prob) * random_tensor
    return output


class DropPath(nn.Layer):
    """
    drop path class
    """
    def __init__(self, drop_prob=None):
        """
        init
        """
        super(DropPath, self).__init__()
        self.drop_prob = drop_prob

    def forward(self, x):
        """
        forward
        """
        return drop_path(x, self.drop_prob, self.training)


class Block(nn.Layer):
    """ ConvNeXt Block. There are two equivalent implementations:
    (1) DwConv -> LayerNorm (channels_first) -> 1x1 Conv -> GELU -> 1x1 Conv; all in (N, C, H, W)
    (2) DwConv -> Permute to (N, H, W, C); LayerNorm (channels_last) -> Linear -> GELU -> Linear; Permute back

    Args:
        dim (int): Number of input channels.
        drop_path (float): Stochastic depth rate. Default: 0.0
        layer_scale_init_value (float): Init value for Layer Scale. Default: 1e-6.
    """

    def __init__(self, dim, drop_path=0., layer_scale_init_value=1e-6):
        """
        init
        """
        super().__init__()
        self.dwconv = nn.Conv2D(dim, dim, kernel_size=7, padding=3,
                                groups=dim)  # depthwise conv
        self.norm = LayerNorm(dim, epsilon=1e-6)
        self.pwconv1 = nn.Linear(
            dim, 4 * dim)  # pointwise/1x1 convs, implemented with linear layers
        self.act = nn.GELU()
        self.pwconv2 = nn.Linear(4 * dim, dim)

        self.gamma = paddle.create_parameter(
            shape=[dim],
            dtype='float32',
            default_initializer=nn.initializer.Constant(
                value=layer_scale_init_value)
        ) if layer_scale_init_value > 0 else None

        self.drop_path = DropPath(drop_path) if drop_path > 0. else Identity()

    def forward(self, x):
        """
        forward
        """
        input = x
        x = self.dwconv(x)
        x = x.transpose([0, 2, 3, 1])  # (N, C, H, W) -> (N, H, W, C)
        x = self.norm(x)
        x = self.pwconv1(x)
        x = self.act(x)
        x = self.pwconv2(x)
        if self.gamma is not None:
            x = self.gamma * x
        x = x.transpose([0, 3, 1, 2])  # (N, H, W, C) -> (N, C, H, W)

        x = input + self.drop_path(x)
        return x


class LayerNorm(nn.Layer):
    """ LayerNorm that supports two data formats: channels_last (default) or channels_first.
    The ordering of the dimensions in the inputs. channels_last corresponds to inputs with
    shape (batch_size, height, width, channels) while channels_first corresponds to inputs
    with shape (batch_size, channels, height, width).
    """

    def __init__(self,
                 normalized_shape,
                 epsilon=1e-6,
                 data_format="channels_last"):
        """
        init
        """
        super().__init__()

        self.weight = paddle.create_parameter(shape=[normalized_shape],
                                              dtype='float32',
                                              default_initializer=ones_)

        self.bias = paddle.create_parameter(shape=[normalized_shape],
                                            dtype='float32',
                                            default_initializer=zeros_)

        self.epsilon = epsilon
        self.data_format = data_format
        if self.data_format not in ["channels_last", "channels_first"]:
            raise NotImplementedError
        self.normalized_shape = (normalized_shape, )

    def forward(self, x):
        """
        forward
        """
        if self.data_format == "channels_last":
            return F.layer_norm(x, self.normalized_shape, self.weight,
                                self.bias, self.epsilon)
        elif self.data_format == "channels_first":
            # u = x.mean(1, keepdim=True)
            # s = (x - u).pow(2).mean(1, keepdim=True)
            # x = (x - u) / paddle.sqrt(s + self.epsilon)
            # x = self.weight[:, None, None] * x + self.bias[:, None, None]
            # return x
            mean = x.mean(1, keepdim=True)
            std = x.std(1, keepdim=True)
            return self.weight[:, None, None] * (x - mean) / (std + self.epsilon) + self.bias[:, None, None]              


class Flatten(nn.Layer):
    """
    Flatten
    """
    def forward(self, input):
        """
        forward
        """
        return paddle.reshape(input, (input.shape[0], -1))


class Head(nn.Layer):
    """
    Head
    """
    def __init__(self, num_features, num_class, mask_ratio=0.67, frozen=False, use_mask=False):
        """
        init
        """
        super(Head, self).__init__()
        self.num_features = num_features
        self.num_class = num_class
        self.frozen = frozen
        self.mask_ratio = mask_ratio
        self.use_mask = use_mask
        self.avgpool = nn.AdaptiveAvgPool2D(output_size=(1, 1))
        self.fc = nn.Linear(self.num_features[1], self.num_class)
        self.output_layer = nn.Sequential(nn.BatchNorm2D(self.num_features[0]),
                                          nn.Dropout(0.3),
                                          Flatten(),
                                          nn.Linear(self.num_features[0], self.num_features[1]),
                                          nn.BatchNorm1D(self.num_features[1]),
                                          nn.ReLU())
            
        # 若冻结权重
        if self.frozen:
            for name, p in self.named_parameters():
                p.stop_gradient = True
        
        # 初始化权重参数
        self.apply(self._init_weights)

    def _init_weights(self, m):
        """
        init weights
        """
        if isinstance(m, nn.Conv2D):
            kaiming_(m.weight)
        elif isinstance(m, nn.BatchNorm2D):
            ones_(m.weight)
            zeros_(m.bias)
        elif isinstance(m, nn.Linear):
            normal_(m.weight)
            zeros_(m.bias)

    def combine_mask(self, slice_score):
        """
        mask
        """
        slice_h, slice_w = slice_score.shape[2], slice_score.shape[3]
        # slice_mask = 0.2 * paddle.ones((slice_h, slice_w))
        # slice_mask[:int(slice_h * self.mask_ratio), :] = 1.2
        # 解决无法转trt的问题
        slice_mask01 = 1.2 * paddle.ones((round(slice_h * self.mask_ratio), slice_w))
        slice_mask02 = 0.2 * paddle.ones((round(slice_h * (1 - self.mask_ratio)), slice_w))
        slice_mask = paddle.concat(x=[slice_mask01, slice_mask02], axis=0)
        return slice_mask * slice_score            

    def forward(self, x):
        """
        forward
        """
        if self.use_mask:
            x = self.combine_mask(x)
        x = self.avgpool(x)
        x = self.output_layer(x)
        res = self.fc(x)
        return res


class ConvNeXt(nn.Layer):
    """ ConvNeXt
        A Paddle impl of : `A ConvNet for the 2020s`  -
          https://arxiv.org/pdf/2201.03545.pdf
    Args:
        in_chans (int): Number of input image channels. Default: 3
        depths (tuple(int)): Number of blocks at each stage. Default: [3, 3, 9, 3]
        dims (int): Feature dimension at each stage. Default: [96, 192, 384, 768]
        drop_path_rate (float): Stochastic depth rate. Default: 0.
        layer_scale_init_value (float): Init value for Layer Scale. Default: 1e-6.
        head_init_scale (float): Init scaling value for classifier weights and biases. Default: 1.
    """

    def __init__(
        self,
        head_frozen=False,
        in_chans=3,
        heads_mask=None,
        heads_mask_ratio=None,
        class_num=None,
        depths=[3, 3, 9, 3],
        dims=[96, 192, 384, 768],
        drop_path_rate=0.,
        layer_scale_init_value=1e-6,
        head_init_scale=1.,
    ):
        """
        init
        """
        super().__init__()

        self.head_nums = len(class_num)

        self.downsample_layers = nn.LayerList(
        )  # stem and 3 intermediate downsampling conv layers
        stem = nn.Sequential(
            nn.Conv2D(in_chans, dims[0], kernel_size=4, stride=4),
            LayerNorm(dims[0], epsilon=1e-6, data_format="channels_first"))
        self.downsample_layers.append(stem)
        for i in range(3):
            downsample_layer = nn.Sequential(
                LayerNorm(dims[i], epsilon=1e-6, data_format="channels_first"),
                nn.Conv2D(dims[i], dims[i + 1], kernel_size=2, stride=2),
            )
            self.downsample_layers.append(downsample_layer)

        self.stages = nn.LayerList(
        )  # 4 feature resolution stages, each consisting of multiple residual blocks
        dp_rates = [
            x.item() for x in paddle.linspace(0, drop_path_rate, sum(depths))
        ]
        cur = 0
        for i in range(4):
            stage = nn.Sequential(*[
                Block(dim=dims[i],
                      drop_path=dp_rates[cur + j],
                      layer_scale_init_value=layer_scale_init_value)
                for j in range(depths[i])
            ])
            self.stages.append(stage)
            cur += depths[i]

        # self.norm = nn.LayerNorm(dims[-1], epsilon=1e-6)  # final norm layer  [batchsize, 768]
        # self.avgpool = nn.AdaptiveAvgPool2D((1, 1))

        # 创建多个属性分类头
        self.head = []
        for i in range(self.head_nums):
            head = Head(num_features=[dims[-1], 512], \
                num_class=class_num[i], mask_ratio=heads_mask_ratio[i], frozen=False, use_mask=heads_mask[i])
            self.head.append(head)
        self.head = nn.LayerList(self.head)
        
        self.apply(self._init_weights)

    def _init_weights(self, m):
        """
        init weights
        """
        if isinstance(m, (nn.Conv2D, nn.Linear)):
            trunc_normal_(m.weight)
            zeros_(m.bias)

    def forward_features(self, x):
        """
        backbone forward
        """
        for i in range(4):
            x = self.downsample_layers[i](x)
            x = self.stages[i](x)
        # return self.norm(x.mean([-2, -1]))
        # return self.avgpool(x)
        return x
    
    def forward(self, inputs):
        """
        forward
        """
        if isinstance(inputs, list):                    # train 

            # 按照batchsize的维度合并输入的数据
            x = paddle.concat(inputs, axis=0)

            # 使用合并的数据共享backbone
            x = self.forward_features(x)
            num_or_sections = [inputs[i].shape[0] for i in range(self.head_nums)]
            features = paddle.split(x, num_or_sections=num_or_sections, axis=0)

            # 分别使用不同的数据计算不同的head
            out = []
            for i in range(self.head_nums):
                out.append(self.head[i](features[i]))

        else:                                           # eval or inference or export
            x = self.forward_features(inputs)
            
            out = []
            for i in range(self.head_nums):
                out.append(self.head[i](x))
        
        return out        
        
        # elif isinstance(inputs, dict):                  # eval
        #     inputs_data = inputs['data']
        #     x = self.forward_features(inputs_data)
            
        #     out = []
        #     for i in range(self.head_nums):
        #         out.append(self.head[i](x))
        #     return out
        
        # else:                                           # inferece
        #     x = self.forward_features(inputs)
        #     out_scores = []
        #     out_class_ids = []
        #     for i in range(self.head_nums):
        #         res = self.head[i](x)
        #         res_output = F.softmax(res, axis=1)
        #         res_score = paddle.max(res_output, axis=-1)
        #         res_id = paddle.argmax(res_output, axis=-1)
        #         out_scores.append(res_score)
        #         out_class_ids.append(res_id)
        #     scores = paddle.concat([paddle.unsqueeze(item, 1) for item in out_scores], axis=1)
        #     class_ids = paddle.concat([paddle.unsqueeze(item, 1) for item in out_class_ids], axis=1)
        #     return scores, class_ids
            

def _load_pretrained(pretrained, model, url, use_ssld=False):
    """
    load pretrained
    """
    if pretrained is False:
        pass
    elif pretrained is True:
        load_dygraph_pretrain_from_url(model, url, use_ssld=use_ssld)
    elif isinstance(pretrained, str):
        load_dygraph_pretrain(model, pretrained)
    else:
        raise RuntimeError(
            "pretrained type is not available. Please use `string` or `boolean` type."
        )


def ConvNext_Multi_Attr(pretrained=False, use_ssld=False, **kwargs):
    """
    基于convnext的多头属性识别网络
    """
    model = ConvNeXt(depths=[3, 3, 9, 3], dims=[96, 192, 384, 768], **kwargs)
    _load_pretrained(
        pretrained, model, MODEL_URLS["ConvNext_Multi_Attr"], use_ssld=use_ssld)
    return model


if __name__ == '__main__':
    """
    此文件单独运行时，需要将convnext_multi_attr中的_load_pretrained注释掉
    """
    # train
    # t1 = np.ones((2, 3, 144, 48))
    # t2 = np.ones((8, 3, 144, 48))
    # t3 = np.ones((1, 3, 144, 48))
    # input_tensor1 = paddle.to_tensor(t1, dtype='float32')
    # input_tensor2 = paddle.to_tensor(t2, dtype='float32')
    # input_tensor3 = paddle.to_tensor(t3, dtype='float32')
    # net = ConvNext_Multi_Attr(class_num=[2, 2, 2], heads_mask=[False, True, False], heads_mask_ratio=[0.6, 0.6, 0.6])
    # output = net([input_tensor1, input_tensor2, input_tensor3])
    # print('output = {}'.format(output))

    # inference
    t1 = np.ones((5, 3, 144, 48))
    input_tensor1 = paddle.to_tensor(t1, dtype='float32')
    net = ConvNext_Multi_Attr(class_num=[2, 2, 3], heads_mask=[False, True, False], heads_mask_ratio=[0.6, 0.6, 0.6])
    net.eval()
    scores, class_ids = net(input_tensor1)
    print('scores = {}'.format(scores))
    print('classids = {}'.format(class_ids))
