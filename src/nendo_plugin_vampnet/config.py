"""Default settings for the Nendo VampNet plugin."""

from nendo import NendoConfig
from pydantic import Field


class VampConfig(NendoConfig):
    """Default settings for the Nendo VampNet plugin.

    Attributes:
        vamp_model (str): VampNet model to use
        max_duration (int): Maximum duration of a generated variation in seconds
    """

    vamp_model: str = Field("vampnet")
    max_duration: int = Field(10)
