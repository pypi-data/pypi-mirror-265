#
#   Feature Pyramid Network
#   Copyright EAVISE
#
import torch.nn as nn
import torch.nn.functional as F
from ._util import Combinator

__all__ = ['FPN', 'PAFPN']


class FPN(nn.Module):
    """ Feature Pyramid Network. |br|
    This class provides a highly customizable FPN implementation.

    Args:
        in_channels (list): list with number of channels of the different input blocks
        out_channels (int): Number of output channels
        num_outputs (int, optional): Number of output tensors from the FPN (see Note); Default **number of input blocks**
        start_output (int, optional): Whether to skip some output tensors (see Note); Default **0**
        make_lateral (function, optional): Function that should return a :class:`torch.nn.Module` for the lateral part; Default **1x1 Conv2d**
        lateral_kwargs (dict or list of dicts): Extra kwargs that are passed to the `make_lateral` function; Default **None**
        make_predicition (function, optional): Function that should return a :class:`torch.nn.Module` for the predicition part; Default **3x3 Conv2d**
        predicition_kwargs (dict or list of dicts): Extra kwargs that are passed to the `make_predicition` function; Default **None**
        make_downsample (function, optional): Function that should return a :class:`torch.nn.Module` for the downsample part; Default **1x1 MaxPool2d with stride 2**
        downsample_kwargs (dict or list of dicts): Extra kwargs that are passed to the `make_downsample` function; Default **None**
        interpolation_mode (string, optional): Type of interpolation when upsampling lateral outputs before addition; Default **nearest**

    .. figure:: /.static/api/fpn.*
       :width: 100%
       :alt: Feature Pyramid Network module design

       The FPN module consists of 3 different blocks: lateral, prediction and downsample.
       You can modify each of these blocks by providing the correct make function and (optionally) keyword arguments. |br|
       By modifying the `num_outputs` and `start_output` arguments, you can choose which output blocks you want.

    Note:
        The `num_outputs` argument can be less or more than **len(in_channels)**.
        If it is less than the number of input blocks, we only run a prediction head on the first `num_outputs` blocks.
        If it is more than the number of input blocks, we run extra downsampling blocks on the last prediction output.

        Finally, the module also allows to skip some of the firs few output blocks, by specifying a number for the `start_output` argument.

    Note:
        All "make" functions have the following signature: ``function(in_channels, out_channels, **kwargs)``.

        The `in_channels` and `out_channels` get computed depending on the block and values of the `in_channels` and `out_channels` arguments. |br|
        The keyword arguments of the different "make" functions are taken from the matching `..._kwargs` arguments,
        which can either be a fixed dictionary which will be used each time the function gets called,
        or a list of dictionaries, with different values for each of the different modules.

        If you pass a list of dictionaries, it should contain the correct number of dictionaries:
            - **lateral**: `len(in_channels)`
            - **prediction**: `min(num_outputs, len(in_channels) - start_output)`
            - **downsample**: `max(0, num_outputs - len(in_channels) + start_output)`
    """
    def __init__(
        self,
        in_channels,
        out_channels,
        num_outputs=None,
        start_output=0,
        make_lateral=None,
        lateral_kwargs=None,
        make_prediction=None,
        prediction_kwargs=None,
        make_downsample=None,
        downsample_kwargs=None,
        interpolation_mode='nearest',
    ):
        super().__init__()
        self.interpolation_mode = interpolation_mode
        self.start_output = min(start_output, len(in_channels) - 1)
        self.num_outputs = num_outputs if num_outputs is not None else len(in_channels)
        assert self.num_outputs > 0, 'We need at least one output'

        make_lateral = make_lateral if make_lateral is not None else self._make_lateral
        make_prediction = make_prediction if make_prediction is not None else self._make_prediction
        make_downsample = make_downsample if make_downsample is not None else self._make_downsample

        self.lateral = nn.ModuleList([
            make_lateral(c, out_channels, **self._get_kwarg(lateral_kwargs, i, {}))
            for i, c in enumerate(in_channels)
        ])

        num_pred = max(min(self.num_outputs, len(in_channels) - start_output), 1)
        self.prediction = nn.ModuleList([
            make_prediction(out_channels, out_channels, **self._get_kwarg(prediction_kwargs, i, {}))
            for i in range(num_pred)
        ])

        self.downsample = None
        num_down = self.num_outputs - len(in_channels) + start_output
        if num_down > 0:
            self.downsample = nn.ModuleList([
                make_downsample(out_channels, out_channels, **self._get_kwarg(downsample_kwargs, i, {}))
                for i in range(num_down)
            ])

    def forward(self, *x):
        assert len(x) >= len(self.lateral), f'Not enough input feature maps supplied: {len(x)} / {len(self.lateral)}'

        lateral = [layer(x[i]) for i, layer in enumerate(self.lateral)]
        for i in range(len(lateral)-1, 0, -1):
            size = lateral[i-1].shape[-2:]
            lateral[i-1] += F.interpolate(lateral[i], size=size, mode=self.interpolation_mode)

        outputs = [layer(lateral[self.start_output+i]) for i, layer in enumerate(self.prediction)]
        if self.downsample is not None:
            for downsample in self.downsample:
                outputs.append(downsample(outputs[-1]))

        return tuple(outputs[-self.num_outputs:])

    @staticmethod
    def _make_lateral(in_channels, out_channels, **kwargs):
        return nn.Conv2d(in_channels, out_channels, 1, 1, 0, bias=True)

    @staticmethod
    def _make_prediction(in_channels, out_channels, **kwargs):
        return nn.Conv2d(in_channels, out_channels, 3, 1, 1, bias=True)

    @staticmethod
    def _make_downsample(in_channels, out_channels, **kwargs):
        return nn.MaxPool2d(1, 2)

    @staticmethod
    def _get_kwarg(value, index, default=None):
        if value is None:
            return default
        elif isinstance(value, (list, tuple)):
            return value[index] if len(value) > index else default
        else:
            return value


class FPN2(nn.Module):
    """
    Feature Pyramid Network. |br|
    TODO

    Args:
        TODO

    Note:
        The combine blocks get the 2 inputs in the following order: `combine([regular_input, upsampled_input])`.
    """

    def __init__(
        self,
        in_channels,
        out_channels,
        make_lateral=None,
        lateral_kwargs=None,
        make_upsample=None,
        upsample_kwargs=None,
        make_combine=None,
        combine_kwargs=None,
    ):
        super().__init__()
        assert len(in_channels) == len(out_channels), f'{self.__class__.__name__} outputs the same number of feature maps as inputs'

        make_lateral = make_lateral if make_lateral is not None else self._make_lateral
        make_upsample = make_upsample if make_upsample is not None else self._make_upsample
        make_combine = make_combine if make_combine is not None else self._make_combine

        self.lateral = nn.ModuleList([
            make_lateral(ci, co, **self._get_kwarg(lateral_kwargs, i, {}))
            for i, (ci, co) in enumerate(zip(in_channels, out_channels))
        ])

        self.upsample = nn.ModuleList([
            make_upsample(ci, co, **self._get_kwarg(upsample_kwargs, i, {}))
            for i, (ci, co) in enumerate(zip(out_channels[:-1], out_channels[1:]))
        ])

        self.combine = nn.ModuleList([
            make_combine(c, c, **self._get_kwarg(combine_kwargs, i, {}))
            for i, c in enumerate(out_channels[1:])
        ])

    def forward(self, *x):
        # Unpack input if it is passed as a list/tuple
        if len(x) == 1 and isinstance(x[0], (list, tuple)):
            x = x[0]
        assert len(x) == len(self.lateral), f'Incorrect number of inputs (requires {len(self.lateral)})'

        lateral = [layer(input) for input, layer in zip(x, self.lateral)]

        upsampled = lateral[:1]
        for input, upsample, combine in zip(lateral[1:], self.upsample, self.combine):
            upsampled.append(combine((input, upsample(upsampled[-1]))))

        return upsampled

    @staticmethod
    def _make_lateral(in_channels, out_channels, **kwargs):
        return nn.Conv2d(in_channels, out_channels, 1, 1, 0, bias=True)

    @staticmethod
    def _make_upsample(in_channels, out_channels, **kwargs):
        assert in_channels == out_channels, 'This upsample implementation requires the input and output channels to be the same'
        return nn.Upsample(scale_factor=2, mode='nearest')

    @staticmethod
    def _make_combine(in_channels, out_channels, **kwargs):
        return Combinator(type='sum')

    @staticmethod
    def _get_kwarg(value, index, default=None):
        if value is None:
            return default
        elif isinstance(value, (list, tuple)):
            return value[index] if len(value) > index else default
        else:
            return value


class PAFPN(FPN2):
    """
    Path Aggregation Feature Pyramid Network :cite:`panet`. |br|

    Args:
        TODO

    Note:
        The combine blocks get the 2 inputs in the following order:
            - `combine([regular_input, upsampled_input])`
            - `combine([downsampled_input, regular_input])`
    """

    def __init__(
        self,
        in_channels,
        out_channels,
        make_lateral=None,
        lateral_kwargs=None,
        make_upsample=None,
        upsample_kwargs=None,
        make_downsample=None,
        downsample_kwargs=None,
        make_combine=None,
        combine_kwargs=None,
    ):
        super().__init__(
            in_channels,
            out_channels,
            make_lateral=make_lateral,
            lateral_kwargs=lateral_kwargs,
            make_upsample=make_upsample,
            upsample_kwargs=upsample_kwargs,
            make_combine=make_combine,
            combine_kwargs=combine_kwargs,
        )

        make_downsample = make_downsample if make_downsample is not None else self._make_downsample
        make_combine = make_combine if make_combine is not None else self._make_combine

        self.downsample = nn.ModuleList([
            make_downsample(ci, co, **self._get_kwarg(downsample_kwargs, i, {}))
            for i, (ci, co) in enumerate(zip(out_channels[-1:0:-1], out_channels[-2::-1]))
        ])

        # Extra combine for the downsample path
        self.combine.extend([
            make_combine(c, c, **self._get_kwarg(combine_kwargs, i, {}))
            for i, c in enumerate(out_channels[-2::-1], start=len(self.combine))
        ])

    def forward(self, *x):
        upsampled = super().forward(x)

        downsampled = upsampled[-1:]
        for input, downsample, combine in zip(upsampled[-2::-1], self.downsample, self.combine[len(x)-1:]):
            downsampled.append(combine((downsample(downsampled[-1]), input)))

        return downsampled[::-1]

    @staticmethod
    def _make_downsample(in_channels, out_channels, **kwargs):
        return nn.Conv2d(in_channels, out_channels, 3, 2, 1, bias=True)
