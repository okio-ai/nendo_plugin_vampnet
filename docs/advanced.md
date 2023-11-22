# Advanced Usage

The vampnet plugin offers a great amount of parameters to customize the output of the plugin and explore different
variations of your track.
The following table gives an overview of the most important parameters:

| Parameter                | Description                                                                                                                               |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| rand_mask_intensity      | The random mask intensity (if this is less than 1, scatters prompts throughout the audio, should be between 0.9 and 1.0).                 |
| n_conditioning_codebooks | The number of conditioning codebooks (probably 0).                                                                                        |
| prefix_s                 | The number of seconds to use as a prefix.                                                                                                 |
| suffix_s                 | The number of seconds to use as a suffix.                                                                                                 |
| periodic_p               | The periodic prompt  (0 - unconditional, 2 - lots of hints, 8 - a couple of hints, 16 - occasional hint, 32 - very occasional hint, etc). |
| periodic_w               | The periodic prompt width (steps, 1 step ~= 10milliseconds).                                                                              |
| onset_mask_width         | The onset mask width (multiplies with the periodic mask, 1 step ~= 10milliseconds).                                                       |
| beat_mask_width          | The beat prompt in ms.                                                                                                                    |
| beat_mask_downbeats      | Whether to mask downbeats only.                                                                                                           |
| dropout                  | The dropout probability.                                                                                                                  |
| num_steps                | The number of steps to use (should normally be between 12 and 36).                                                                        |
| top_p                    | The top p probability. (0.0 = off)                                                                                                        |
| masktemp                 | The mask temperature to use.                                                                                                              |
| sampletemp               | The sample temperature to use.                                                                                                            |
| typical_filtering        | Whether to use typical filtering.                                                                                                         |
| typical_mass             | The typical mass to use (should probably stay between 0.1 and 0.5).                                                                       |
| typical_min_tokens       | The typical minimum tokens to use (should probably stay between 1 and 256).                                                               |

!!! tip
    If you're interested in more details be sure to read the VampNet [paper on arxiv](https://arxiv.org/abs/2307.04686).

## Preset patterns from the official paper

### Unconditional

| Parameter           | Value |
|---------------------|-------|
| periodic_p          | 0     |
| onset_mask_width    | 0     |
| beat_mask_width     | 0     |
| beat_mask_downbeats | False |

### Slight Periodic Variation

| Parameter           | Value |
|---------------------|-------|
| periodic_p          | 5     |
| onset_mask_width    | 5     |
| beat_mask_width     | 0     |
| beat_mask_downbeats | False |

### Moderate Periodic Variation

| Parameter           | Value |
|---------------------|-------|
| periodic_p          | 13    |
| onset_mask_width    | 5     |
| beat_mask_width     | 0     |
| beat_mask_downbeats | False |

### Strong Periodic Variation

| Parameter           | Value |
|---------------------|-------|
| periodic_p          | 17    |
| onset_mask_width    | 5     |
| beat_mask_width     | 0     |
| beat_mask_downbeats | False |

### Very Strong Periodic Variation

| Parameter           | Value |
|---------------------|-------|
| periodic_p          | 21    |
| onset_mask_width    | 5     |
| beat_mask_width     | 0     |
| beat_mask_downbeats | False |

### Beat-Driven Variation

| Parameter           | Value |
|---------------------|-------|
| periodic_p          | 0     |
| onset_mask_width    | 0     |
| beat_mask_width     | 50    |
| beat_mask_downbeats | False |

### Beat-Driven Variation (Downbeats Only)

| Parameter           | Value |
|---------------------|-------|
| periodic_p          | 0     |
| onset_mask_width    | 0     |
| beat_mask_width     | 50    |
| beat_mask_downbeats | True  |

### Beat-Driven Variation (Downbeats Only, Strong)

| Parameter           | Value |
|---------------------|-------|
| periodic_p          | 0     |
| onset_mask_width    | 0     |
| beat_mask_width     | 20    |
| beat_mask_downbeats | True  |
