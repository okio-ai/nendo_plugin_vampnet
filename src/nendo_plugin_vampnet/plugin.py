"""A nendo plugin for VampNet music generation."""
from logging import Logger
from typing import Any, Optional

from nendo import Nendo, NendoConfig, NendoError, NendoGeneratePlugin, NendoTrack
from vampnet.interface import Interface

from .config import VampConfig
from .nendo_vampnet import get_vamp_variation, load_vamp_model

settings = VampConfig()


class NendoVampGenerator(NendoGeneratePlugin):
    """A nendo plugin for VampNet music generation based on VampNet by Hugo Flores Garcia.
    https://github.com/hugofloresgarcia/vampnet

    Attributes:
        nendo_instance (Nendo): The Nendo instance.
        config (NendoConfig): The Nendo config.
        logger (Logger): The Nendo logger.
        model (Interface): The VampNet model.
        current_model (str): The name of the current VampNet model.

    Examples:
        ```python
        from nendo import Nendo, NendoConfig

        nendo = Nendo(config=NendoConfig(plugins=["nendo_plugin_vampnet"]))

        track = nendo.library.add_track(file_path="path/to/file.wav")

        outpainting = nendo.plugins.vampnet(
            track=track,
            prefix_secs=2,
            suffix_secs=0
        )

        outpainting.play()
    """

    nendo_instance: Nendo = None
    config: NendoConfig = None
    logger: Logger = None
    model: Interface = None
    current_model: str = None

    def __init__(self, **data: Any):
        """Initialize the plugin."""
        super().__init__(**data)
        self.current_model = settings.vamp_model
        self.model = load_vamp_model(self.current_model)

    @NendoGeneratePlugin.run_track
    def generate_variations(
            self,
            track: NendoTrack,
            seed: int = 0,
            rand_mask_intensity: int = 1,
            n_conditioning_codebooks: int = 0,
            prefix_s: int = 0,
            suffix_s: int = 2,
            duration: int = 10,
            periodic_p: int = 0,
            periodic_w: int = 0,
            onset_mask_width: int = 0,
            beat_mask_width: int = 50,
            beat_mask_downbeats: bool = True,
            dropout: int = 0,
            num_steps: int = 36,
            top_p: int = 0,
            masktemp: float = 1.5,
            sampletemp: float = 1.0,
            typical_filtering: bool = False,
            typical_mass: float = 0.15,
            typical_min_tokens: int = 64,
            vamp_model: str = "vampnet",
    ) -> NendoTrack:
        """Generate variations for a given collection using VampNet with a base model or a fine-tuned checkpoint.

        Args:
            track (NendoTrack): The track to generate variations for.
            seed (int): The seed to use for the random number generator.
            prefix_s (int): The number of seconds to use as a prefix for the variation.
            suffix_s (int): The number of seconds to use as a suffix for the variation.
            duration (int): The duration of the variation in seconds.
            vamp_model (Optional[str]): The name of the VampNet model to use.
            rand_mask_intensity (Optional[int]): The intensity of the random mask.
            n_conditioning_codebooks (Optional[int]): The number of conditioning codebooks to use.
            periodic_p (Optional[int]): The periodic mask probability.
            periodic_w (Optional[int]): The periodic mask width.
            onset_mask_width (Optional[int]): The onset mask width.
            beat_mask_width (Optional[int]): The beat mask width.
            beat_mask_downbeats (Optional[bool]): Whether to mask downbeats or upbeats.
            dropout (Optional[int]): The dropout probability.
            num_steps (Optional[int]): The number of steps to use.
            top_p (Optional[int]): The top p probability.
            masktemp (Optional[float]): The mask temperature to use.
            sampletemp (Optional[float]): The sample temperature to use.
            typical_filtering (Optional[bool]): Whether to use typical filtering.
            typical_mass (Optional[float]): The typical mass to use.
            typical_min_tokens (Optional[int]): The typical minimum tokens to use.

        Returns:
            NendoTrack: A `Nendotrack` containing the generated variation.
        """
        if vamp_model != self.current_model:
            self.model = load_vamp_model(vamp_model)
            self.current_model = vamp_model

        meta = {
            "model": vamp_model,
            "seed": seed,
            "prefix_s": prefix_s,
            "suffix_s": suffix_s,
            "duration": duration,
            "rand_mask_intensity": rand_mask_intensity,
            "n_conditioning_codebooks": n_conditioning_codebooks,
            "periodic_p": periodic_p,
            "periodic_w": periodic_w,
            "onset_mask_width": onset_mask_width,
            "beat_mask_width": beat_mask_width,
            "beat_mask_downbeats": beat_mask_downbeats,
            "dropout": dropout,
            "num_steps": num_steps,
            "top_p": top_p,
            "masktemp": masktemp,
            "sampletemp": sampletemp,
            "typical_filtering": typical_filtering,
            "typical_mass": typical_mass,
            "typical_min_tokens": typical_min_tokens,
        }

        if duration > settings.max_duration:
            raise NendoError("Duration must be less than 10 seconds.")

        frames = track.sr * duration
        variation = get_vamp_variation(
            interface=self.model,
            signal=track.signal[:, :frames],
            sr=track.sr,
            rand_mask_intensity=rand_mask_intensity,
            n_conditioning_codebooks=n_conditioning_codebooks,
            prefix_s=prefix_s,
            suffix_s=suffix_s,
            periodic_p=periodic_p,
            periodic_w=periodic_w,
            onset_mask_width=onset_mask_width,
            beat_mask_width=beat_mask_width,
            beat_mask_downbeats=beat_mask_downbeats,
            dropout=dropout,
            num_steps=num_steps,
            top_p=top_p,
            seed=seed,
            masktemp=masktemp,
            sampletemp=sampletemp,
            typical_filtering=typical_filtering,
            typical_mass=typical_mass,
            typical_min_tokens=typical_min_tokens,
        )

        return self.nendo_instance.library.add_related_track_from_signal(
            signal=variation.T,
            sr=track.sr,
            track_meta=meta,
            related_track_id=track.id,
            track_type="vamp",
            relationship_type="vamp"
        )
