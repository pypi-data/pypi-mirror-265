from ..bitlinear import BitLinear
from transformers import AutoModel

def apply_bitlinear(hf_model: AutoModel) -> AutoModel:
    """
    Apply the weights of a model to a huggingface model.
    """
    for name, param in model.named_parameters():
        if 'weight' in name:
            hf_model.config[name] = param
        elif 'bias' in name:
            hf_model.config[name] = param
    return hf_model