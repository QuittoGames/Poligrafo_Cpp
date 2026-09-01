from dataclasses import dataclass, field


@dataclass
class Data:
    latest_state: list = field(default_factory=list)
    modules_local: list = field(
        default_factory=lambda: [
            "controller",
            "data",
            "frontend",
            "services",
            "model",
            "utils",
        ]
    )

    Debug: bool = (
        False  # Set True to inject synthetic data (bypasses real Arduino reader)
    )
