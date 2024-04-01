from typing import Tuple

import torch

from ..triton_kernels.bitmat_kernel import batched_bitmat
from .packing import pack_ternary


def terniarize(weights: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Terniarizes the weights and returns the scale.
    """
    scale = 1 / torch.max(weights.abs().mean(), torch.tensor(1e-5))
    return torch.clamp((weights * scale).to(torch.int8), -1, 1), scale

def quantize_activations(x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Quantizes the activations and returns the scale for each row.
    """
    scale = (127 / torch.max(x.abs().max(dim=-1).values, torch.tensor(1e-5))).unsqueeze(-1)
    return torch.clamp((x * scale), -127, 128).to(torch.int8), scale


class BitMat(torch.autograd.Function):
    def forward(ctx, W, X, scale_w=None):
        """
        During the forward pass, we ternarize the weights, pack them and then quantize the activations.
        We then perform the bit matrix multiplication and return the scaled results.
        ternarization:
        scale_w = 1 / mean(abs(W))                              | STE
        W = clip(round(W * scale_w), -1, 1)                     | STE
        packing:
        packed_w = 4 int8 -> 1 int8                             | STE
        quantization:
        scale_x = 127 / max(abs(X))                             | STE
        X = clip(round(X * scale_x), -127, 128)                 | STE
        bit matrix multiplication:
        Y = X @ w_packed.t()                                    | dot product
        Y = Y / (scale_w * scale_x)                             | STE
        """
        if W.training:
            W, scale_w = terniarize(W)
            packed_w = pack_ternary(W, 4)
            X, scale_x = quantize_activations(X)
            ctx.save_for_backward(X, scale_x)
            y = batched_bitmat(X, packed_w)
            return y / scale_w / scale_x
        else:
            assert scale_w is not None, "scale_w must be provided during inference"
            X, scale_x = quantize_activations(X)
            y = batched_bitmat(X, W)
            return y / scale_w / scale_x


    @staticmethod
    def backward(ctx, grad_output):
        X, scale_x = ctx.saved_tensors
        # get dW
        grad_W = grad_output @ (X / scale_x).t().to(torch.float16) # TODO: check dim
        return grad_W, None, None

def bitmat(W: torch.Tensor, X: torch.Tensor) -> torch.Tensor:
    return BitMat.apply(W, X)