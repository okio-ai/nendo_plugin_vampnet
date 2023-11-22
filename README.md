# Nendo Plugin Vampnet

<br>
<p align="left">
    <img src="https://okio.ai/docs/assets/nendo_core_logo.png" width="350" alt="nendo core">
</p>
<br>


![Documentation](https://img.shields.io/website/https/nendo.ai)
[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/okio_ai.svg?style=social&label=Follow%20%40okio_ai)](https://twitter.com/okio_ai) [![](https://dcbadge.vercel.app/api/server/XpkUsjwXTp?compact=true&style=flat)](https://discord.gg/XpkUsjwXTp)

Nendo Plugin for VampNet: Music Generation via Masked Acoustic Token Modeling 
(by [Hugo Flores Garcia](https://github.com/hugofloresgarcia/vampnet)).

## Features 

- Generate unconditional variations
- Use custom finetuned vampnet models
- Generate in- and outpaintings from a `NendoTrack`
 
## Requirements

This plugin requires the manual installation of `vampnet` via its git repository:

`pip install git+https://github.com/hugofloresgarcia/vampnet.git@0c0c6bc`

## Installation

1. [Install Nendo](https://github.com/okio-ai/nendo#installation)
2. `pip install nendo-plugin-vampnet`

## Usage

Take a look at a basic usage example below.
For more detailed information, please refer to the [documentation](https://okio.ai/docs/plugins).

For more advanced examples, check out the examples folder.
or try it in colab:

<a target="_blank" href="https://colab.research.google.com/drive/1IRH3gXLgqtMjfOknMkEmSqPmrEdiKAxM?usp=sharing">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

```python
from nendo import Nendo, NendoConfig

nd = Nendo(config=NendoConfig(plugins=["nendo_plugin_vampnet"]))
track = nd.library.add_track(file_path='/path/to/track.mp3')

vamp = nd.plugins.vampnet(track=track, prefix_secs=2, suffix_secs=0)
vamp.play()
```

## Contributing

Visit our docs to learn all about how to contribute to Nendo: [Contributing](https://okio.ai/docs/contributing/)

## License

Nendo: MIT License

Vampnet: MIT License

Pretrained Models: The weights for the models are licensed CC BY-NC-SA 4.0. Likewise, any VampNet models fine-tuned on the pretrained models are also licensed CC BY-NC-SA 4.0.