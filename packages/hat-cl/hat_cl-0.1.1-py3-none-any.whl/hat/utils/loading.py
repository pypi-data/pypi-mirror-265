import warnings

import torch
import torch.nn as nn

from hat.exceptions import ModuleLoadingWarning


def _get_subset_state_dict(
    state_dict: dict[str, torch.Tensor],
    key: str,
) -> dict[str, torch.Tensor]:
    """Helper function to get a subset of the state dict."""
    if key in state_dict:
        return {key: state_dict[key]}
    else:
        return {
            _k[len(key) + 1 :]: _v  # noqa: E203
            for _k, _v in state_dict.items()
            if _k.startswith(f"{key}.")
        }


def load_from_base_module_state_dict(
    hat_module: nn.Module,
    base_module_state_dict: dict[str, torch.Tensor],
):
    """Helper function to load the state dict of a base module to a HAT module.

    This function loads the state dict of a base module to a HAT module. The
    function assumes that the base module and the HAT module have the same
    structure. The function will recursively load the state dict of the base
    module to the HAT module.

    Args:
        hat_module: The HAT module to load the state dict to.
        base_module_state_dict: The state dict of the base module to load the
          state dict from.

    """
    from hat.modules.utils import base_to_task_dependent_mapping as mapping

    if hat_module.__class__ in mapping.values():
        hat_module.load_from_base_module_state_dict(base_module_state_dict)
    elif hat_module.__class__ in mapping.keys():
        hat_module.load_state_dict(base_module_state_dict)
    elif len(list(hat_module.named_children())) == 0:
        warnings.warn(
            f"Module of class {hat_module.__class__} is not a"
            f" registered task dependent module. Will load the"
            f" state dict using PyTorch `load_state_dict`.",
            ModuleLoadingWarning,
        )
        hat_module.load_state_dict(base_module_state_dict)
    else:
        for _n, _m in hat_module.named_children():
            _subset_state_dict = _get_subset_state_dict(
                base_module_state_dict,
                _n,
            )
            if len(_subset_state_dict) > 0:
                load_from_base_module_state_dict(_m, _subset_state_dict)
            else:
                warnings.warn(
                    f"Child module {_n} of class {_m.__class__}"
                    f" is not found in the state dict. Skipping...",
                    ModuleLoadingWarning,
                )


def load_from_base_module(
    hat_module: nn.Module,
    base_module: nn.Module,
):
    """Helper function to load the weights of a base module to a HAT module.

    This function loads the weights of a base module to a HAT module. The
    function assumes that the base module and the HAT module have the same
    structure. The function will recursively load the weights of the base
    module to the HAT module.

    Args:
        hat_module: The HAT module to load the weights to.
        base_module: The base module to load the weights from.

    """
    return load_from_base_module_state_dict(
        hat_module=hat_module,
        base_module_state_dict=base_module.state_dict(),
    )
