import torch
from torch import nn

from ..bitlinear import BitLinear
from transformers import AutoModel

def apply_bitlinear_to_hf_model(model: AutoModel) -> AutoModel:
    rms_layers = {}

    for name, module in list(model.named_children()):
        if 'RMS' in type(module).__name__:
            if hasattr(module, 'eps'):
                rms_eps = module.eps
            elif hasattr(module, 'epsilon'):
                rms_eps = module.epsilon
            elif hasattr(module, 'variance_epsilon'):
                rms_eps = module.variance_epsilon
            else:
                raise RuntimeError(
                    "Model type not mappable, please open an issue on GitHub citing the model you are using")

            # save weights and eps
            rms_layers[name] = {'eps': rms_eps}

            delattr(model, name)

    # Secondo passaggio: sostituire i layer lineari con BitLinear
    for name, module in model.named_children():
        if isinstance(module, nn.Linear):
            in_features = module.in_features
            out_features = module.out_features
            bias = module.bias is not None

            # Determina se esiste un layer RMSNorm precedente e ottiene il suo epsilon
            rms_eps = rms_layers.get(f"{name}_rms", {}).get('eps', torch.tensor(1e-5))

            bit_linear = BitLinear(in_features, out_features, rms_eps, bias)
            if bias:
                bit_linear.bias.data.copy_(module.bias.data)
            bit_linear.weight.data.copy_(module.weight.data)

            # Sostituisci Linear con BitLinear
            setattr(model, name, bit_linear)

        else:
            # Applica ricorsivamente ai moduli figli
            apply_bitlinear_to_hf_model(module)

    return model
