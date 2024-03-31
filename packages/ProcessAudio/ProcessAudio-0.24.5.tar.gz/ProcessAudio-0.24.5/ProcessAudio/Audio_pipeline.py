import os
import numpy as np
from sklearn.pipeline import Pipeline

from ProcessAudio.Features import Features as Audio_features
from ProcessAudio.Graph import Audio_images as Audio_graph
from ProcessAudio.Split import Split as Audio_split
import tempfile


class Audio_pipeline:

    def extract_features(
        self,
        audio_path: str,
        split_time: int = 10,
        hight_frecuency_filter=1400,
        low_frecuency_filter=None,
        activate_remove_audio_noise=True,
        activate_silence_reduction_miliseconds=1000,
    ):
        """
        This method is used to extract the features of an audio file
        firts split the audio in parts of split_time seconds
        then extract the features of each part (mfcc, chroma, tonnetz)
        and finally generate the images of the mfcc and mel of each part

        @type audio_path: str
        @param audio_path: path of the audio file

        @type split_time: int
        @param split_time: time in seconds to split the audio

        @type hight_frecuency_filter: int
        @param hight_frecuency_filter: hight frecuency filter

        @type low_frecuency_filter: int
        @param low_frecuency_filter: low frecuency filter

        @type activate_remove_audio_noise: bool
        @param activate_remove_audio_noise: activate remove audio noise

        @type activate_silence_reduction_miliseconds: int
        @param activate_silence_reduction_miliseconds: silence reduction in miliseconds

        @rtype: dict
        @return: dictionary with the features of the audio file
        """

        end_data = {
            "features": [],
            "audio": audio_path,
            "seconds_split": split_time,
        }

        with tempfile.TemporaryDirectory() as tmpdirname:
            pipeline = Pipeline(
                [
                    (
                        "split",
                        Audio_split(
                            output_path_to_save_audios=os.path.join(
                                tmpdirname, "audios_dataset"
                            ),
                            activate_remove_audio_noise=activate_remove_audio_noise,
                            activate_silence_reduction_miliseconds=activate_silence_reduction_miliseconds,
                        ),
                    ),
                    (
                        "features",
                        Audio_features(
                            complete_answer=True,
                            **dict(mfcc=True, chroma=True, tonnetz=True)
                        ),
                    ),
                    (
                        "graph",
                        Audio_graph(
                            output_path_to_save_images=tmpdirname,
                            **dict(
                                hight_frecuency_filter=hight_frecuency_filter,
                                low_frecuency_filter=low_frecuency_filter,
                            )
                        ),
                    ),
                ]
            )

            y_pred = pipeline.transform(dict(audio=audio_path, seconds=split_time))

            durations = y_pred.get("durations", 0)
            if durations ==0:
                return None
            
            features = y_pred.get("features")
            audios_images = y_pred.get("audios_images")
            mfcc_s = [dat["mfcc"] for dat in audios_images]
            mel_s = [dat["mel"] for dat in audios_images]

            for feature, duration, mfcc, mel in zip(features, durations, mfcc_s, mel_s):
                end_data["features"].append(
                    dict(
                        features=feature,
                        duration=duration,
                        mfcc_image=mfcc,
                        mel_image=mel,
                    )
                )

            end_data["duration_before_prepreprocesing"] = y_pred[
                "duration_before_prepreprocesing"
            ]
            end_data["duration_after_prepreprocesing"] = y_pred[
                "duration_after_prepreprocesing"
            ]

        return end_data


    def extract_spectogram(
        self,
        audio_path: str,
        split_time: int = 10,
        hight_frecuency_filter=1400,
        low_frecuency_filter=None,
        activate_remove_audio_noise=True,
        activate_silence_reduction_miliseconds=1000,
    ):
        """
        This method is used to extract the features of an audio file
        firts split the audio in parts of split_time seconds
        then extract the features of each part (mfcc, chroma, tonnetz)
        and finally generate the images of the mfcc and mel of each part

        @type audio_path: str
        @param audio_path: path of the audio file

        @type split_time: int
        @param split_time: time in seconds to split the audio

        @type hight_frecuency_filter: int
        @param hight_frecuency_filter: hight frecuency filter

        @type low_frecuency_filter: int
        @param low_frecuency_filter: low frecuency filter

        @type activate_remove_audio_noise: bool
        @param activate_remove_audio_noise: activate remove audio noise

        @type activate_silence_reduction_miliseconds: int
        @param activate_silence_reduction_miliseconds: silence reduction in miliseconds

        @rtype: dict
        @return: dictionary with the features of the audio file
        """

        end_data = {
            "features": [],
            "audio": audio_path,
            "seconds_split": split_time,
        }

        with tempfile.TemporaryDirectory() as tmpdirname:
            pipeline = Pipeline(
                [
                    (
                        "split",
                        Audio_split(
                            output_path_to_save_audios=os.path.join(
                                tmpdirname, "audios_dataset"
                            ),
                            activate_remove_audio_noise=activate_remove_audio_noise,
                            activate_silence_reduction_miliseconds=activate_silence_reduction_miliseconds,
                        ),
                    ),
                    (
                        "graph",
                        Audio_graph(
                            output_path_to_save_images=tmpdirname,
                            **dict(
                                hight_frecuency_filter=hight_frecuency_filter,
                                low_frecuency_filter=low_frecuency_filter,
                            )
                        ),
                    ),
                ]
            )

            y_pred = pipeline.transform(dict(audio=audio_path, seconds=split_time))

            durations = y_pred.get("durations", 0)
            if durations ==0:
                return None
            
            features = y_pred.get("features")
            audios_images = y_pred.get("audios_images")
            mfcc_s = [dat["mfcc"] for dat in audios_images]
            mel_s = [dat["mel"] for dat in audios_images]

            for feature, duration, mfcc, mel in zip(features, durations, mfcc_s, mel_s):
                end_data["features"].append(
                    dict(
                        features=feature,
                        duration=duration,
                        mel_image=mel,
                    )
                )

            end_data["duration_before_prepreprocesing"] = y_pred[
                "duration_before_prepreprocesing"
            ]
            end_data["duration_after_prepreprocesing"] = y_pred[
                "duration_after_prepreprocesing"
            ]

        return end_data

def save_feature(feature: np.array, path: str):
    """
    This method is used to save a feature in a file

    @type feature: np.array
    @param feature: feature to save

    @type path: str
    @param path: path to save the feature
    """

    np.savetxt(path, feature, delimiter=",")


def save_image(image, path: str):
    """
    This method is used to save an image in a file

    @type image: PIL.Image
    @param image: image to save

    @type path: str
    @param path: path to save the image
    """

    image.save(path)
    image.close()


def read_feature(path: str):
    """
    This method is used to read a feature from a file

    @type path: str
    @param path: path to read the feature

    @rtype: np.array
    @return: feature readed
    """

    return np.loadtxt(path, delimiter=",")
