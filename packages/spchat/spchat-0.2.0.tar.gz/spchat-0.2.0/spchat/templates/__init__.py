from .ca import Calm2Template
from .stability import (
    StabilityPrompterDefault,
    StabilityPrompterDefaultWithHistory,
    StabilityPrompterV1,
    StabilityPrompterV1WithFun,
    StabilityPrompterV2,
    StabilityPrompterV2FarHistoryWithFun,
    StabilityPrompterV2NoRepetitionWithFun,
    StabilityPrompterV2WithFun,
    StabilityPrompterV3,
    StabilityPrompterV4,
)

__all__ = [
    "Calm2Template",
    "ChatPrompter",
    "StabilityPrompterDefault",
    "StabilityPrompterDefaultWithHistory",
    "StabilityPrompterV1",
    "StabilityPrompterV1WithFun",
    "StabilityPrompterV2",
    "StabilityPrompterV2FarHistoryWithFun",
    "StabilityPrompterV2NoRepetitionWithFun",
    "StabilityPrompterV2WithFun",
    "StabilityPrompterV3",
    "StabilityPrompterV4",
]


TEMPLATE_REGISTRY: dict = {
    "calm2": Calm2Template,
    "stability_default": StabilityPrompterDefault,
    "stability_default_with_history": StabilityPrompterDefaultWithHistory,
    "stability_v1": StabilityPrompterV1,
    "stability_v1_fun": StabilityPrompterV1WithFun,
    "stability_v2": StabilityPrompterV2,
    "stability_v2_fun_far_history": StabilityPrompterV2FarHistoryWithFun,
    "stability_v2_fun_no_repetition": StabilityPrompterV2NoRepetitionWithFun,
    "stability_v2_fun": StabilityPrompterV2WithFun,
    "stability_v3": StabilityPrompterV3,
    "stability_v4": StabilityPrompterV4,
}
