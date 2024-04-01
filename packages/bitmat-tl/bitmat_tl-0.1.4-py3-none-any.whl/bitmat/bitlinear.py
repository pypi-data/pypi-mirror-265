import torch

from .utils.bitmat import bitmat
from .utils.rmsnorm import RMSLayerNorm


class BitLinear(torch.nn.Module):
    """
    A linear layer that uses packed terniary matrix multiplication.
    """
    def __init__(self, in_features, out_features, eps, bias=False):
        super(BitLinear, self).__init__()
        self.eps = eps
        self.weight = torch.nn.Parameter(torch.zeros(out_features, in_features))
        if bias:
            self.bias = torch.nn.Parameter(torch.tensor(out_features))
        else:
            self.bias = None
        self.norm = RMSLayerNorm(out_features, 1e-5)
        self._post_init()
    def _post_init(self):
        torch.nn.init.kaiming_normal_(self.weight, mode='fan_out', nonlinearity='relu')

    def forward(self, x):
        x = self.norm(x)
        return bitmat(self.weight, x)


