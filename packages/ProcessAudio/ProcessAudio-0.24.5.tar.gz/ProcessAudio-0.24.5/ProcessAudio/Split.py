import os
import pydub
import uuid
from ProcessAudio.Util import Util as Audio_util
from ProcessAudio.Graph import Audio_images as Audio_graph

from sklearn.base import BaseEstimator, TransformerMixin


audio_util = Audio_util()
audio_graph = Audio_graph()


class Split(BaseEstimator, TransformerMixin):

    __audio: pydub.AudioSegment
    audio_path: str
    output_path: str

    def __init__(
        self,
        output_path_to_save_audios: str,
        activate_remove_audio_noise: bool = False,
        activate_silence_reduction_miliseconds: int = None,
    ):
        """
        @type output_path_to_save_audios: str
        @param output_path_to_save_audios: path to save the audio files

        @type activate_remove_audio_noise: bool
        @param activate_remove_audio_noise: if True, the audio is denoised

        @type activate_silence_reduction_miliseconds: int
        @param activate_silence_reduction_miliseconds: if not None, the silence is reduced in miliseconds
        """

        os.makedirs(output_path_to_save_audios, exist_ok=True)
        self.output_path = output_path_to_save_audios

        self.__denoise_audio = activate_remove_audio_noise
        self.__silence_reduce_miliseconds = activate_silence_reduction_miliseconds

        if (
            self.__silence_reduce_miliseconds is not None
            and self.__silence_reduce_miliseconds > 0
        ):
            if self.__silence_reduce_miliseconds < 500:
                self.__silence_reduce_miliseconds = 500

    def __read_audio(self, try_forced: bool = True):
        try:
            if self.audio_path.endswith(".mp3"):
                self.__audio = pydub.AudioSegment.from_mp3(self.audio_path)
            elif self.audio_path.endswith(".wav"):
                self.__audio = pydub.AudioSegment.from_wav(self.audio_path)
            else:
                if try_forced:
                    self.__audio = pydub.AudioSegment.from_file(self.audio_path)
                else:
                    raise ValueError(
                        "File format not supported, please use .mp3 or .wav"
                    )
        except Exception as e:
            print(f"Error reading the audio file: {e}")
            self.__audio = None

    def __split(self, start: int, end: int, save: bool = False):

        _output_path = os.path.join(self.output_path, f"{uuid.uuid4()}.wav")

        audio = self.__audio[start:end]

        if save:
            audio.export(_output_path, format="wav")

        return audio, _output_path if save else None

    def __clean_audio(self):
        if self.__denoise_audio:
            self.__audio = audio_util.denoise_audio(self.__audio)

        if (
            self.__silence_reduce_miliseconds is not None
            and self.__silence_reduce_miliseconds > 0
        ):
            self.__audio = audio_util.reduce_silence(
                self.__audio, self.__silence_reduce_miliseconds
            )

    def __split_by_seconds(self, seconds: int):
        """
        Split the audio in seconds

        @type seconds: int
        @param seconds: seconds to split the audio

        @rtype: Union[list, str]
        @return: list of audios or list of paths where the audios are saved
        """

        if self.__audio is None:
            return []

        audio_duration = len(self.__audio)
        audios = []

        for start in range(0, audio_duration, seconds * 1000):
            end = start + seconds * 1000
            if end > audio_duration:
                end = audio_duration
            audios.append(self.__split(start, end)[0])

        audios_saved = []
        for audio_id, audio in enumerate(audios):
            name = uuid.uuid4().hex.lower()

            audio_output_path = os.path.join(self.output_path, f"{name}_{audio_id}.wav")
            audio.export(audio_output_path, format="wav")

            audios_saved.append(audio_output_path)

        audios = audios_saved

        return audios

    def transform(
        self,
        audio_data: dict = dict(
            audio=None,
            seconds=None,
        ),
    ):
        """
        @type audio_data: dict
        @param audio_data: dictionary with the audio and the seconds to split the audio
        """

        audio_path = audio_data.get("audio")
        seconds = audio_data.get("seconds")

        assert audio_path is not None, "audio_path is required"
        assert seconds is not None, "seconds is required"

        self.audio_path = audio_path
        self.__read_audio()
        
        if self.__audio is None:
            return audio_data

        assert self.__audio is not None, "Audio not found"
        audio_data["duration_before_prepreprocesing"] = len(self.__audio) / 1000

        self.__clean_audio()
        audios_saved = self.__split_by_seconds(seconds)

        durations = []
        for audio in audios_saved:
            audio = pydub.AudioSegment.from_wav(audio)
            durations.append(len(audio) / 1000)

        audio_data["audios"] = audios_saved
        audio_data["durations"] = durations
        
        audio_data["duration_after_prepreprocesing"] = len(self.__audio) / 1000

        return audio_data
