from typing import Union
import matplotlib.pyplot as plt
import librosa.display
import librosa
import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin


class Features(BaseEstimator, TransformerMixin):
    data = None

    N_FFT = 1024  # Number of frequency bins for Fast Fourier Transform
    HOP_SIZE = 1024  # Number of audio frames between STFT columns
    WIN_SIZE = 1024  # number of samples in each STFT window
    WINDOW_TYPE = "hann"  # the windowin function
    N_MELS = 128  # Mel band parameters

    def __init__(self, complete_answer: bool = False, **config):
        """
        @type complete_answer: bool
        @param complete_answer: if True, the features are returned in a single line
                                if not the features are returned in a single array meaning
        """

        self.mfcc = None
        self.zcr = None
        self.rolloff = None
        self.spec_bw = None
        self.spec_cent = None
        self.rms = None
        self.chroma_stft = None
        self.tonnetz = None
        self.mel = None

        self.complete_answer = complete_answer
        self.__config = config

    def set_data(self, data_audio: Union[str, tuple]):
        """
        Set the data audio to process

        @type data_audio: Union[str, tuple]
        @param data_audio: audio data or tuple with audio data and sample rate
        """

        if isinstance(data_audio, str):
            rate: int = 44100
            (data, rate) = librosa.core.load(data_audio)
            self.data = data
            self.sr = rate

        if isinstance(data_audio, tuple):
            self.data = data_audio[0]
            self.sr = data_audio[1]

    def display_waveform(self, data: np.array = None, sr: int = None):
        """
        Display the waveform of the audio

        @type data: np.array
        @param data: audio data
        @type sr: int
        @param sr: sample rate
        """

        if data is not None and sr is not None:
            plt.figure(figsize=(14, 5))
            librosa.display.waveplot(data, sr=sr)

        else:
            if self.data is None:
                return None

            # display waveform
            plt.figure(figsize=(14, 5))
            librosa.display.waveplot(self.data, sr=self.sr)

    def get_croma(self):
        """
        Chroma feature to represent the energy distribution of the pitch classes

        @rtype: np.array
        @return: chroma features
        """

        if self.data is None:
            return None

        self.chroma_stft = librosa.feature.chroma_stft(y=self.data, sr=self.sr)

        if self.complete_answer:
            self.chroma_stft = librosa.feature.chroma_stft(
                y=self.data,
                sr=self.sr,
                S=np.abs(
                    librosa.stft(
                        self.data,
                        n_fft=self.N_FFT,
                        hop_length=self.HOP_SIZE,
                        window=self.WINDOW_TYPE,
                        win_length=self.WIN_SIZE,
                    )
                )
                ** 2,
            )

        return self.chroma_stft

    def get_rms(self):
        """
        Root Mean Square Energy (RMSE)
        which is the square root of the mean of the squared signal values.

        @rtype: np.array
        @return: rmse features
        """

        if self.data is None:
            return None

        self.rms = librosa.feature.rms(y=self.data)

        if self.complete_answer:
            self.rms = np.ravel(self.rms)

        return self.rms

    def get_spectral_centroid(self):
        """
        The center of mass of the spectrum.

        @rtype: np.array
        @return: spectral centroid features
        """

        if self.data is None:
            return None

        self.spec_cent = librosa.feature.spectral_centroid(y=self.data, sr=self.sr)

        if self.complete_answer:
            self.spec_cent = np.ravel(self.spec_cent)

        return self.spec_cent

    def get_spectral_bandwidth(self):
        """
        The bandwidth is the width of the band of frequencies
        where most of the energy of the signal is concentrated.

        @rtype: np.array
        @return: spectral bandwidth features
        """

        if self.data is None:
            return None

        self.spec_bw = librosa.feature.spectral_bandwidth(y=self.data, sr=self.sr)

        if self.complete_answer:
            self.spec_bw = np.ravel(self.spec_bw)

        return self.spec_bw

    def get_rolloff(self):
        """
        Also known as spectral reduction in frequency.
        where is 85% of the signal energy

        @rtype: np.array
        @return: rolloff features
        """

        if self.data is None:
            return None
        self.rolloff = librosa.feature.spectral_rolloff(y=self.data, sr=self.sr)

        if self.complete_answer:
            self.rolloff = np.ravel(self.rolloff)

        return self.rolloff

    def get_zero_crossing(self):
        """
        Zero crossing rate

        @rtype: np.array
        @return: zero crossing rate features
        """

        if self.data is None:
            return None

        self.zcr = librosa.feature.zero_crossing_rate(self.data)

        if self.complete_answer:
            self.zcr = np.ravel(self.zcr)

        return self.zcr

    def get_mfcc(self):
        """
        Mel-frequency cepstral coefficients (MFCCs)
        coefficients that collectively make up the mel-frequency cepstrum

        @rtype: np.array
        @return: mfcc features
        """

        if self.data is None:
            return None

        self.mfcc = librosa.feature.mfcc(y=self.data, sr=self.sr)

        if self.complete_answer:
            # mfcc with dct and stft

            self.mfcc = librosa.core.power_to_db(
                librosa.feature.mfcc(
                    dct_type=3,
                    y=self.data,
                    sr=self.sr,
                    n_fft=self.N_FFT,
                    hop_length=self.HOP_SIZE,
                    n_mels=self.N_MELS,
                    htk=True,
                    fmin=0.0,
                    fmax=self.sr / 2.0,
                    S=np.abs(
                        librosa.stft(
                            self.data,
                            n_fft=self.N_FFT,
                            hop_length=self.HOP_SIZE,
                            window=self.WINDOW_TYPE,
                            win_length=self.WIN_SIZE,
                        )
                    )
                    ** 2,
                ),
                ref=1.0,
            )

        return self.mfcc

    def get_tonnetz(self):
        """
        Compute tonnetz features from the harmonic component of a song

        @rtype: np.array
        @return: tonnetz features
        """

        if self.data is None:
            return None

        self.tonnetz = librosa.feature.tonnetz(y=self.data, sr=self.sr)

        if self.complete_answer:
            self.tonnetz = librosa.feature.tonnetz(
                y=self.data,
                sr=self.sr,
            )

        return self.tonnetz

    def get_mel_spectrogram(
        self,
        hight_frecuency_filter: int = 0,
        low_frecuency_filter: int = 100000,
    ):
        """
        Mel Spectrogram

        @type hight_frecuency_filter: int
        @param hight_frecuency_filter: hight frecuency filter

        @type low_frecuency_filter: int
        @param low_frecuency_filter: low frecuency filter

        @rtype: np.array
        @return: mel spectrogram features
        """

        if self.data is None:
            return None

        self.mel = librosa.feature.melspectrogram(y=self.data, sr=self.sr)

        if self.complete_answer:
            N_FFT = 1024  # Number of frequency bins for Fast Fourier Transform
            HOP_SIZE = 1024  # Number of audio frames between STFT columns
            N_MELS = 128  # Mel band parameters
            WIN_SIZE = 1024  # number of samples in each STFT window
            WINDOW_TYPE = "hann"  # the windowin function

            self.mel = librosa.core.power_to_db(
                librosa.feature.melspectrogram(
                    y=self.data,
                    S=np.abs(
                        librosa.stft(
                            self.data,
                            n_fft=N_FFT,
                            hop_length=HOP_SIZE,
                            window=WINDOW_TYPE,
                            win_length=WIN_SIZE,
                        )
                    )
                    ** 2,
                    sr=self.sr,
                    n_fft=N_FFT,
                    hop_length=HOP_SIZE,
                    n_mels=N_MELS,
                    htk=True,
                    fmin=hight_frecuency_filter,
                    fmax=low_frecuency_filter,
                ),
                ref=1.0,
            )

        return self.mel

    def build_custom_features(
        self,
        mfcc: bool = False,
        zero_crossing: bool = False,
        roolloff: bool = False,
        spectral_centroid: bool = False,
        spectral_bandwidth: bool = False,
        rms: bool = False,
        chroma_stft: bool = False,
        tonnetz: bool = False,
    ):

        features = []

        if mfcc:
            self.get_mfcc()
            mfcc = np.ravel(self.mfcc)  # 20x216
            features.append(mfcc)

        if zero_crossing:
            self.get_zero_crossing()
            features.append(self.zcr)

        if roolloff:
            self.get_rolloff()
            features.append(self.rolloff)

        if spectral_centroid:
            self.get_spectral_centroid()
            features.append(self.spec_cent)

        if spectral_bandwidth:
            self.get_spectral_bandwidth()
            features.append(self.spec_bw)

        if rms:
            self.get_rms()
            features.append(self.rms)

        if chroma_stft:
            self.get_croma()  # 12x216
            chroma_stft = np.ravel(self.chroma_stft)
            features.append(chroma_stft)

        if tonnetz:
            self.get_tonnetz()  # 6x431
            tonnetz = np.ravel(self.tonnetz)
            features.append(tonnetz)

        features = np.concatenate(features)
        features = np.ravel(features)

        if len(features) != 9498:
            # print()
            pass

        return features

    def build_basic(self) -> list:
        if self.data is None:
            return []

        self.get_croma()
        self.get_rms()
        self.get_spectral_centroid()
        self.get_spectral_bandwidth()
        self.get_rolloff()
        self.get_zero_crossing()
        self.get_mfcc()

        if not self.complete_answer:
            data_compresed = f"{np.mean(self.chroma_stft)} {np.mean(self.rms)} {np.mean(self.spec_cent)} {np.mean(self.spec_bw)} {np.mean(self.rolloff)} {np.mean(self.zcr)}"
            for e in self.mfcc:
                data_compresed += f" {np.mean(e)}"
        else:
            complete = np.concatenate(
                [
                    self.chroma_stft,
                    self.rms,
                    self.spec_cent,
                    self.spec_bw,
                    self.rolloff,
                    self.zcr,
                    self.mfcc,
                ]
            )
            data_compresed = complete.tolist()

        return data_compresed.split()

    def transform(self, audios_data: dict = None):

        assert audios_data is not None, "The audios_saved is required"
        assert (
            audios_data.get("audio") is not None
            or audios_data.get("audios") is not None
        ), "The audio data is required"
        
        audios_to_process = []
        if audios_data.get("audios") is not None and isinstance(audios_data.get("audios"), list) and len(audios_data.get("audios")) > 0:
            audios_to_process = audios_data.get("audios")
        else:
            audios_to_process.append(audios_data.get("audio"))

        audios_features = []

        for audio in audios_to_process:
            self.set_data(audio)

            if self.complete_answer:
                features = self.build_custom_features(
                    mfcc=self.__config.get("mfcc", False),
                    zero_crossing=self.__config.get("zero_crossing", False),
                    roolloff=self.__config.get("rolloff", False),
                    spectral_centroid=self.__config.get("spectral_centroid", False),
                    spectral_bandwidth=self.__config.get("spectral_bandwidth", False),
                    rms=self.__config.get("rms", False),
                    chroma_stft=self.__config.get("chroma_stft", False),
                    tonnetz=self.__config.get("tonnetz", False),
                )
            else:
                features = self.build_basic()

            audios_features.append(features)

        audios_data["features"] = audios_features

        return audios_data
