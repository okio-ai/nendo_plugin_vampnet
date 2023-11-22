"""A wrapper for VampNet to generate variations from audio signals."""
import os
from typing import Optional
from zipfile import ZipFile

import numpy as np
import requests
from audiotools import AudioSignal
from nendo import NendoError
from tqdm import tqdm
from vampnet import Interface
from vampnet import mask as pmask


def load_vamp_model(model_name: str) -> Interface:
    """Loads a VampNet model by name.

    Args:
        model_name (str): The name of the model to load.

    Returns:
        Interface: The loaded VampNet model.
    """
    model_name = f"models/{model_name}"
    if not os.path.exists(model_name):
        download_models(model_name)
    return Interface(
        coarse_ckpt=f"{model_name}/coarse.pth",
        coarse2fine_ckpt=f"{model_name}/c2f.pth",
        codec_ckpt=f"{model_name}/codec.pth",
        coarse_chunk_size_s=10,
        coarse2fine_chunk_size_s=3,
        wavebeat_ckpt=f"{model_name}/../wavebeat.pth",
        device="cuda",
    )


def download_models(model_dir: str):
    """Downloads the VampNet base models and extract them to the given directory.

    Currently defaults to the VampNet base checkpoints on Zenodo.
    https://zenodo.org/records/8136629

    Args:
        model_dir (str): The directory to download the models to.

    """
    os.makedirs(model_dir, exist_ok=True)

    download_url = "https://zenodo.org/records/8136629/files/models.zip?download=1"
    zip_file = "models.zip"

    with requests.get(download_url, stream=True, timeout=2000) as r:
        r.raise_for_status()
        total_size_in_bytes = int(r.headers.get("content-length", 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)
        with open(zip_file, "wb") as f:
            for data in r.iter_content(block_size):
                progress_bar.update(len(data))
                f.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            os.remove(model_dir)
            raise NendoError("Error while downloading models.")


    print("Extracting models...")
    with ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall("./")

    os.remove(zip_file)


def get_vamp_variation(
    interface: Interface,
    signal: np.ndarray,
    sr: int,
    rand_mask_intensity: int,
    n_conditioning_codebooks: int,
    prefix_s: int,
    suffix_s: int,
    periodic_p: int,
    periodic_w: int,
    onset_mask_width: int,
    beat_mask_width: int,
    beat_mask_downbeats: bool,
    dropout: int,
    num_steps: int,
    top_p: int,
    seed: int,
    masktemp: float,
    sampletemp: float,
    typical_filtering: bool,
    typical_mass: float,
    typical_min_tokens: int,
) -> np.ndarray:
    """Generates a variation from a given audio signal using VampNet.

    Args:
        interface (Interface): The VampNet interface to use.
        signal (np.ndarray): The audio signal to generate a variation from.
        sr (int): The sample rate of the audio signal.
        rand_mask_intensity (Optional[int]): The intensity of the random mask.
        n_conditioning_codebooks (Optional[int]): The number of conditioning codebooks to use.
        prefix_s (Optional[int]): The number of seconds to use as a prefix.
        suffix_s (Optional[int]): The number of seconds to use as a suffix.
        periodic_p (Optional[int]): The periodic mask probability.
        periodic_w (Optional[int]): The periodic mask width.
        onset_mask_width (Optional[int]): The onset mask width.
        beat_mask_width (Optional[int]): The beat mask width.
        beat_mask_downbeats (Optional[bool]): Whether to mask downbeats or upbeats.
        dropout (Optional[int]): The dropout probability.
        num_steps (Optional[int]): The number of steps to use.
        top_p (Optional[int]): The top p probability.
        seed (Optional[int]): The seed to use.
        masktemp (Optional[float]): The mask temperature to use.
        sampletemp (Optional[float]): The sample temperature to use.
        typical_filtering (Optional[bool]): Whether to use typical filtering.
        typical_mass (Optional[float]): The typical mass to use.
        typical_min_tokens (Optional[int]): The typical minimum tokens to use.

    Returns:
        np.ndarray: The generated variation.
    """
    sig = AudioSignal(signal, sample_rate=sr)
    sig = interface.preprocess(sig)
    z = interface.encode(sig)

    ncc = n_conditioning_codebooks

    # build the mask
    mask = pmask.linear_random(z, rand_mask_intensity)
    mask = pmask.mask_and(
        mask, pmask.inpaint(z, interface.s2t(prefix_s), interface.s2t(suffix_s)),
    )
    mask = pmask.mask_and(
        mask, pmask.periodic_mask(z, periodic_p, periodic_w, random_roll=True),
    )
    if onset_mask_width > 0:
        mask = pmask.mask_or(
            mask, pmask.onset_mask(sig, z, interface, width=onset_mask_width),
        )
    if beat_mask_width > 0:
        beat_mask = interface.make_beat_mask(
            sig,
            after_beat_s=(beat_mask_width / 1000),
            mask_upbeats=not beat_mask_downbeats,
        )
        mask = pmask.mask_and(mask, beat_mask)

    # these should be the last two mask ops
    mask = pmask.dropout(mask, dropout)
    mask = pmask.codebook_unmask(mask, ncc)

    _top_p = top_p if top_p > 0 else None

    _seed = seed if seed > 0 else None
    zv, mask_z = interface.coarse_vamp(
        z,
        mask=mask,
        sampling_steps=num_steps,
        mask_temperature=masktemp * 10,
        sampling_temperature=sampletemp,
        return_mask=True,
        typical_filtering=typical_filtering,
        typical_mass=typical_mass,
        typical_min_tokens=typical_min_tokens,
        top_p=_top_p,
        gen_fn=interface.coarse.generate,
        seed=_seed,
    )

    zv = interface.coarse_to_fine(
        zv,
        mask_temperature=masktemp * 10,
        sampling_temperature=sampletemp,
        mask=mask,
        sampling_steps=num_steps,
        seed=_seed,
    )

    return interface.to_signal(zv).cpu().numpy()[0][0]
