# ProcessAudio
 Libreria python para hacer data augmentation en audios y/o extraer caracteristicas a audios

---

# Installation

```bash
pip install ProcessAudio
```
---

# Description

A `ProcessAudio` object should be created and use its attributes.

This library have tree main functions:

* `Features`: Extract features from audio
* `AudioAugmentation`: Augment audio in different ways
* `AllDataAugmentation`: Augment audio in different ways and extract features
---

[Back To Top ↥](#ProcessAudio)

## Features methods

* `set_data(data_audio:str="<path_audio_file>)`: Set data to extract features
* `get_croma()`: Extract croma features
* `get_mfcc()`: Extract mfcc features
* `get_rmse()`: Extract rmse features
* `get_centroide_espectral()`: Extract spectral centroid features
* `get_rolloff()`: Extract spectral rolloff features
* `get_cruce_por_cero()`: Extract zero crossing rate features
* `get_ancho_banda_espectral()`: Extract spectral bandwidth features
* `build_all()`: Extract all features in a list
---

[Back To Top ↥](#ProcessAudio)

## AudioAugmentation methods

* `loudness()`: Apply loudness to audio file creating a new data
* `add_mask()`: Apply mask to audio file creating a new data
* `pitch()`: Apply pitch to audio file creating a new data
* `get_original()`: Get original audio file
* `add_crop()`: Apply crop to audio file creating a new data
* `add_noise()`: Apply noise to audio file creating a new data
* `add_noise2()`: Apply noise to audio file creating a new data
* `shift()`: Apply shift to audio file creating a new data
* `stretch()`: Apply stretch to audio file creating a new data
* `speed()`: Apply speed to audio file creating a new data
* `normalizer()`: Apply normalizer to audio file creating a new data
* `polarizer()`: Apply polarizer to audio file creating a new data
* `write_audio_file()`: Write audio file
* `plot_time_series()`: Plot time series
---

[Back To Top ↥](#ProcessAudio)

## AllDataAugmentation methods

* `build_all(extract_features: bool)`: Augment audio and extract features if extract_features is True

---

[Back To Top ↥](#ProcessAudio)

# Usage

## Example Features
```python
import os
from ProcessAudio.Features import Features

filepath = os.path.dirname(os.path.abspath(__file__)) + os.sep
path_file = filepath + "demo" + os.sep + "dat_92.wav"

features = Features()
features.set_data(path_file)
DATA = features.build_all() # Extract all features
print(DATA)
print(len(DATA))
```
---

[Back To Top ↥](#ProcessAudio)

## Example AudioAugmentation
```python
import os
from ProcessAudio.AudioAugmentation import AudioAugmentation

filepath = os.path.dirname(os.path.abspath(__file__)) + os.sep
path_file = filepath + "demo" + os.sep + "dat_92.wav"
folder_save = filepath + "new_audios" + os.sep

aumentation = AudioAugmentation(audio_file=path_file, save=folder_save)
audio_con_ruido = aumentation.add_noise(factor_ruido=0.05)
audio_normalizer = aumentation.normalizer()
audio_loudness = aumentation.loudness()
```
---

[Back To Top ↥](#ProcessAudio)

## Example AllDataAugmentation
```python
import os
from ProcessAudio.AllDataAugmentation import AllDataAugmentation

filepath = os.path.dirname(os.path.abspath(__file__)) + os.sep
path_file = filepath + "demo" + os.sep + "dat_92.wav"
folder_save = filepath + "new_audios" + os.sep

aumentation = AllDataAugmentation(path_file, path_save=folder_save, label=["cero", "uno"])
data, label = aumentation.build_all(extract_features=True)
print(len(data), len(label))
print(len(data[0]), label[0])
```
---

[Back To Top ↥](#ProcessAudio)

# Citing


If you want to cite ProcessAudio in an academic paper, there are two ways to do it.

- APA:

    WISROVI, W.S.R.V. (2022). Python library to augment audio data and/or extract audio features (Version 0.22.11) [Computer Software]. https://github.com/wisrovi/ProcessAudio

- BibTex:

    @software{WISROVI_Instrument_Classifier_2022,
author = {WISROVI, William Steve Rodríguez Villamizar},
month = {10},
title = {{Python library to augment audio data and/or extract audio features}},
URL = {https://github.com/wisrovi/ProcessAudio},
version = {0.22.11},
year = {2022}
}


---

[Back To Top ↥](#ProcessAudio)

# License

GPLv3 License

---

[Back To Top ↥](#ProcessAudio)

# Support:
<p>
    <a href="https://www.buymeacoffee.com/wisrovirod8">
        <img align="left" src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" height="50" width="210" alt="wisrovirod8" />
    </a>
</p>

