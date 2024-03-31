# https://medium.com/@alibugra/audio-data-augmentation-f26d716eee66
# https://medium.com/@makcedward/data-augmentation-for-audio-76912b01fdf6
# https://github.com/makcedward/nlpaug/blob/master/example/audio_augmenter.ipynb
import os

from nlpaug.util import AudioVisualizer

try:
    import librosa
    import librosa.display as librosa_display
except ImportError:
    print("Librosa is not installed. Please install it.")
    import subprocess

    subprocess.call(["pip3", "install", "librosa", "--user", "--upgrade"])
    exit()

import nlpaug.augmenter.audio as naa

import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write


class AudioAugmentation:
    graph: bool = False

    verbose: bool = False

    def __init__(self, audio_file, graph=False, save: str = None):
        self.audio_file = audio_file
        self.graph = graph
        self.save = save
        if isinstance(audio_file, str):
            if self.verbose:
                print("Aumentando archivo de audio", audio_file)
            self.name_file = audio_file.split(".")[-2].split(os.sep)[-1]
            self.data, self.rate = self.__read_audio_file(self.audio_file)
        elif isinstance(audio_file, tuple):
            if self.verbose:
                print("Audio file is a tuple")
            self.data, self.rate, self.name_file = audio_file

    def middleware_in(
        method_name: str = "",
    ):
        """
        Middleware to execute before and after the functions of the class
        """

        def _middleware_in(f):
            def wrapper(self, *args, **kwargs):
                # execution before executing the function
                if self.verbose:
                    print(
                        "\t" * 2, f"Middleware in {f.__name__} ({method_name})", end=""
                    )

                # execution of the function
                ejecucion_ok = True
                try:
                    output = f(self, *args, **kwargs)
                except Exception as e:
                    ejecucion_ok = False
                    output = e
                    if self.verbose:
                        print(
                            f"Error in the execution of the function {f.__name__}: {e}"
                        )

                # execution after executing the function
                if ejecucion_ok:
                    if self.graph:
                        self.plot_audio(output)
                        if self.verbose:
                            print(" - Graph", end="")

                    if self.save is not None:
                        try:
                            if isinstance(output, list):
                                if self.verbose:
                                    print(output)
                                output = np.array(output)
                            self.write_audio_file(
                                self.save + self.name_file + "_" + f"{f.__name__}.wav",
                                output,
                                self.rate,
                            )
                            if self.verbose:
                                print(
                                    f" - Save in {self.save + self.name_file + '_' + f'{f.__name__}.wav'}",
                                    end="",
                                )
                        except Exception as e:
                            if self.verbose:
                                print(
                                    f" - Error to save file ({self.save + self.name_file + '_' + f'{f.__name__}.wav'}): {e}",
                                    end="",
                                )
                                print(type(output))

                if self.verbose:
                    print()
                return output

            return wrapper

        return _middleware_in

    def plot_audio(self, data2=None):
        """
        Plot the audio signal, with the original audio signal and the audio signal with the changes

        @type data2: np.array
        @param data2: audio data to plot with the original audio signal
        """

        librosa_display.waveshow(self.data, sr=self.rate, alpha=0.5)
        if data2 is not None:
            librosa_display.waveshow(data2, sr=self.rate, color="r", alpha=0.25)

        plt.tight_layout()
        plt.show()

    @middleware_in(method_name="loudness_f")
    def loudness(self):
        """
        Change the loudness of the audio signal

        @rtype: np.array
        @return: audio with changed loudness
        """

        try:
            aug = naa.LoudnessAug()
            augmented_data = aug.augment(self.data)[0]
            return augmented_data
        except Exception as e:
            return None

    @middleware_in(method_name="mask_f")
    def add_mask(self):
        """
        Add a mask to the audio signal, removing a part of it

        @rtype: np.array
        @return: audio with mask
        """

        try:
            aug = naa.MaskAug(sampling_rate=self.rate, mask_with_noise=False)
            augmented_data = aug.augment(self.data)[0]
            return augmented_data
        except Exception as e:
            return None

    @middleware_in(method_name="pitch_f")
    def pitch(self, fact=(2, 3)):
        """
        Change the pitch of the audio signal

        @type fact: tuple
        @param fact: factor to change the pitch

        @rtype: np.array
        @return: audio with changed pitch
        """

        try:
            aug = naa.PitchAug(sampling_rate=self.rate, factor=fact)
            augmented_data = aug.augment(self.data)[0]
            return augmented_data
        except Exception as e:
            return None

    @middleware_in(method_name="original")
    def get_original(self):
        """
        Get the original audio signal
        """

        return self.data

    @middleware_in(method_name="crop")
    def add_crop(self):
        """
        Crop the audio signal, removing a part of it

        @rtype: np.array
        @return: audio cropped
        """

        try:
            crop = naa.CropAug(sampling_rate=self.rate)
            augmented_data = crop.augment(self.data)[0]
            return augmented_data
        except Exception as e:
            return None

    @staticmethod
    def __read_audio_file(file_path: str, cut: bool = False):
        """
        Read an audio file, the data is necessary the audio was read with librosa.load method

        @type file_path: str
        @param file_path: path to the audio file

        @type cut: bool
        @param cut: if True the audio signal is cut to the input length

        @rtype: tuple
        @return: audio data and sample rate
        """

        try:
            input_length = 16000
            data, rate = librosa.core.load(file_path)
            if cut:
                if len(data) > input_length:
                    data = data[:input_length]
                else:
                    data = np.pad(
                        data, (0, max(0, input_length - len(data))), "constant"
                    )
            return data, rate
        except Exception as e:
            print(f"Error to read file {file_path}: {e}")
            return None, None

    @staticmethod
    def write_audio_file(file: str, data: np.array, sample_rate: int):
        """
        Write an audio file

        @type file: str
        @param file: path to save the audio file

        @type data: np.array
        @param data: audio data

        @type sample_rate: int
        @param sample_rate: sample rate
        """

        try:
            write(file, sample_rate, data)
        except Exception as e:
            print(f"Error to write file {file}: {e}")

    @staticmethod
    def plot_time_series(data):
        """
        Plot the audio time series
        """

        fig = plt.figure(figsize=(14, 8))
        plt.title("Raw wave ")
        plt.ylabel("Amplitude")
        plt.plot(np.linspace(0, 1, len(data)), data)
        plt.show()

    @middleware_in(method_name="ruido")
    def add_noise(self, noise_factor: float = 0.005):
        """
        Add noise to the audio signal

        @type noise_factor: float
        @param noise_factor: factor to add noise

        @rtype: np.array
        @return: audio with noise
        """

        try:
            noise = np.random.randn(len(self.data))
            data_noise = self.data + noise_factor * noise
            data_noise = data_noise.astype(type(self.data[0]))  # Cast back to same
            return data_noise
        except Exception as e:
            return None

    @middleware_in(method_name="ruido2")
    def add_noise2(self):
        """
        Add noise to the audio signal

        @rtype: np.array
        @return: audio with noise
        """

        try:
            aug = naa.NoiseAug()
            augmented_data = aug.augment(self.data)[0]
            return augmented_data
        except Exception as e:
            return None

    @middleware_in(method_name="shift")
    def shift(self):
        """
        Shift the audio signal

        @rtype: np.array
        @return: audio shifted
        """

        try:
            aug = naa.ShiftAug()
            augmented_data = aug.augment(self.data)[0]
            return augmented_data
        except Exception as e:
            try:
                return np.roll(self.data, 1600)
            except Exception as e:
                return None

    @middleware_in(method_name="stretch")
    def stretch(self, rate_stretch: float = 1.0, cut: bool = False):
        """
        Stretch the audio signal, making it longer or shorter

        @type rate_stretch: float
        @param rate_stretch: rate to stretch the audio signal

        @type cut: bool
        @param cut: if True the audio signal is cut to the input length

        @rtype: np.array
        @return: audio stretched
        """

        try:
            aug = naa.TimeStretchAug()
            augmented_data = aug.augment(self.data)[0]
            return augmented_data
        except Exception as e:
            try:
                input_length = 16000
                data = librosa.effects.time_stretch(self.data, rate=rate_stretch)
                if cut:
                    if len(data) > input_length:
                        data = data[:input_length]
                    else:
                        data = np.pad(
                            data, (0, max(0, input_length - len(data))), "constant"
                        )
                return data
            except Exception as e:
                return None

    @middleware_in(method_name="speed")
    def speed(self):
        """
        Speed up the audio signal

        @rtype: np.array
        @return: audio with speed up
        """

        try:
            aug = naa.SpeedAug()
            augmented_data = aug.augment(self.data)[0]
            return augmented_data
        except Exception as e:
            return None

    @middleware_in(method_name="normalizador")
    def normalizer(self):
        """
        Normalize the audio signal

        @rtype: np.array
        @return: audio normalized
        """

        try:
            aug = naa.NormalizeAug(method="minmax")
            augmented_data = aug.augment(self.data)[0]
            return augmented_data
        except Exception as e:
            return None

    @middleware_in(method_name="polarizador")
    def polarizer(self):
        """
        Invert the polarity of the audio signal

        @rtype: np.array
        @return: audio with inverted polarity
        """

        try:
            aug = naa.PolarityInverseAug()
            augmented_data = aug.augment(self.data)[0]
            return augmented_data
        except Exception as e:
            return None
