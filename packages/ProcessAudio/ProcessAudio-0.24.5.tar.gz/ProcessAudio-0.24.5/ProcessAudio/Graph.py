from typing import Tuple
import numpy as np
import os
from PIL import Image
import librosa
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
from sklearn.base import BaseEstimator, TransformerMixin
from efficientnet.keras import preprocess_input
from ProcessAudio.Features import Features
from tensorflow.keras.preprocessing.image import ImageDataGenerator


features = Features(complete_answer=True)


class Audio_images(BaseEstimator, TransformerMixin):

    def __init__(self, output_path_to_save_images: str = None, **config):
        self.output_path_to_save_images = output_path_to_save_images

        try:
            for folder in ["mfcc", "mel"]:
                os.makedirs(
                    os.path.join(self.output_path_to_save_images, folder), exist_ok=True
                )
        except Exception as e:
            pass

        self.config = config

    def spectrogram(
        self,
        data: np.array,
        sr: int,
        output_path: str = None,
        title: str = "Spectrogram",
    ):
        """
        Plot and save a spectrogram, the data is necessary the audio was read with Util.read_audio method

        @type data: np.array
        @param data: audio data

        @type sr: int
        @param sr: sample rate

        @type title: str
        @param title: title of the plot

        @rtype: str
        @return: path to the plot
        """

        frequencies, times, spectrogram_data = signal.spectrogram(data, sr)

        plt.figure(figsize=(10, 5))
        plt.pcolormesh(times, frequencies, np.log10(spectrogram_data))
        plt.xlabel("Time [s]")
        plt.ylabel("Frequency [Hz]")
        plt.title(title)
        plt.colorbar(label="Intensity [dB]")

        if output_path is None:
            output_path = "spectrogram.png"

        plt.savefig(output_path)

        plt.close()

        return output_path

    def log_mel_spectrogram(
        self,
        data: np.array,
        sr: int,
        output_path: str = None,
        title: str = "log_mel_spectrogram",
    ):
        """
        Plot and save a log-mel spectrogram, the data is necessary the audio was read with Util.read_audio method

        @type data: np.array
        @param data: audio data

        @type sr: int
        @param sr: sample rate

        @type output_path: str
        @param output_path: path to save the plot

        @type title: str
        @param title: title of the plot
        """

        # Calcular el log-mel espectrograma
        mel_spectrogram = librosa.feature.melspectrogram(y=data, sr=sr)
        log_mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)

        # Plotear el log-mel espectrograma
        plt.figure(figsize=(10, 5))
        librosa.display.specshow(
            log_mel_spectrogram, sr=sr, x_axis="time", y_axis="mel"
        )
        plt.colorbar(format="%+2.0f dB")
        plt.title(title)
        plt.tight_layout()

        if output_path is None:
            output_path = "log_mel_spectrogram.png"

        plt.savefig(output_path)
        plt.close()

        return output_path

    def spectogram_for_training(
        self,
        audio_path: str,
        mel_output_path: str = None,
        mfcc_output_path: str = None,
        hight_frecuency_filter: int = 0,
        low_frecuency_filter: int = 100000,
    ):
        y, sr = librosa.load(audio_path)

        if low_frecuency_filter is None:
            low_frecuency_filter = sr / 2.0

        features.set_data((y, sr))

        HOP_SIZE = 1024  # Number of audio frames between STFT columns

        """
        
        
                mel spectrogram
                
        
        """

        def normalize(data):
            # Normalize
            data -= data.min()
            data /= data.max()

            return data

        if mel_output_path is not None:
            try:
                mel_spec = normalize(
                    features.get_mel_spectrogram(
                        hight_frecuency_filter=hight_frecuency_filter,
                        low_frecuency_filter=low_frecuency_filter,
                    )
                )
                plt.figure()
                librosa.display.specshow(
                    mel_spec,
                    sr=sr,
                    hop_length=HOP_SIZE,
                    x_axis="time",
                    y_axis="mel",
                )
                plt.axis("off")  # Quital los nombres de los ejes x e y
                plt.title(None)  # Elimina el título
                plt.grid(False)  # Desactiva la cuadrícula
                plt.tight_layout()  # Elimina el espacio en blanco
                plt.savefig(
                    mel_output_path, bbox_inches="tight", pad_inches=0
                )  # Ajusta automáticamente el tamaño de la imagen
                plt.close()
            except Exception as e:
                pass

        """
        
        
                mfcc
                
        
        """
        if mfcc_output_path is not None:
            try:
                mfcc = features.get_mfcc()
                plt.figure()
                librosa.display.specshow(
                    mfcc,
                    sr=sr,
                    hop_length=HOP_SIZE,
                    x_axis="time",
                )
                plt.axis("off")  # Quital los nombres de los ejes x e y
                plt.title(None)  # Elimina el título
                plt.grid(False)  # Desactiva la cuadrícula
                plt.tight_layout()  # Elimina el espacio en blanco
                plt.savefig(
                    mfcc_output_path, bbox_inches="tight", pad_inches=0
                )  # Ajusta automáticamente el tamaño de la imagen
                plt.close()
            except Exception as e:
                pass

    def image_aumentation(
        self,
        imagespath_clases_tuple: Tuple[str, str] = None,
        img_size: tuple = (224, 224),
        active_image_aumentation: bool = True,
        batch: int = 16,
        # dataframe [optional]
        dataframe_input_output_tuple: Tuple[
            pd.DataFrame, str, str
        ] = None,  # (df, input, output)
    ):

        if not active_image_aumentation:
            datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
        else:
            datagen = ImageDataGenerator(
                preprocessing_function=preprocess_input,  # Reescalar los píxeles para que estén en el rango [-1, 1]
                rescale=1.0
                / 255,  # Reescalar los píxeles para que estén en el rango [0, 1]
                rotation_range=20,  # Rotación aleatoria en un rango de 20 grados
                width_shift_range=0.2,  # Desplazamiento aleatorio horizontal
                height_shift_range=0.2,  # Desplazamiento aleatorio vertical
                shear_range=0.2,  # Cizallamiento aleatorio
                zoom_range=0.1,  # Zoom aleatorio
                horizontal_flip=True,  # Volteo horizontal aleatorio
                fill_mode="nearest",  # Modo de relleno para los píxeles fuera del borde
            )

        if dataframe_input_output_tuple is not None:
            df = dataframe_input_output_tuple[0]
            input_col = dataframe_input_output_tuple[1]
            output_col = dataframe_input_output_tuple[2]

            directory = os.path.dirname(df[input_col].iloc[0])
            df[input_col] = df[input_col].apply(os.path.basename)

            batches = datagen.flow_from_dataframe(
                dataframe=df,
                shuffle=True,
                directory=directory,
                x_col=input_col,  # Nombre de la columna que contiene las rutas de las imágenes
                y_col=output_col,  # Nombre de la columna que contiene las etiquetas de las clases
                target_size=img_size,  # Tamaño al que se redimensionarán las imágenes
                batch_size=batch,  # Tamaño del lote
                class_mode="categorical",  # Modo de clase (categórico para clasificación)
            )
        else:
            imagespath = imagespath_clases_tuple[0]
            clases_list = imagespath_clases_tuple[1]

            # Crear un generador de datos de imágenes a partir del directorio
            batches = datagen.flow_from_directory(
                directory=imagespath,
                classes=clases_list,
                shuffle=True,
                target_size=img_size,  # Tamaño al que se redimensionarán las imágenes
                batch_size=batch,  # Tamaño del lote
                class_mode="categorical",  # Modo de clase (categórico para clasificación)
            )

        # example: next(batches) for get a batch of images of the generator of the df[input_col]

        return batches

    def transform(self, audios_data: dict = None):
        """
        Transform the audio data to images

        @type audios_data: dict
        @param audios_data: dictionary with the audio data

        @rtype: dict
        @return: dictionary with the audio data and the images
        """

        assert audios_data is not None, "The audios_saved is required"
        assert (
            audios_data.get("audio") is not None
            or audios_data.get("audios") is not None
        ), "The audio data is required"

        audios_to_process = []
        if (
            audios_data.get("audios") is not None
            and isinstance(audios_data.get("audios"), list)
            and len(audios_data.get("audios")) > 0
        ):
            audios_to_process = audios_data.get("audios")
        else:
            audios_to_process.append(audios_data.get("audio"))

        audios_images = []

        for audio in audios_to_process:
            mfcc_path = os.path.join(
                self.output_path_to_save_images,
                "mfcc",
                os.path.basename(audio).split(".")[0] + ".png",
            )

            mel_path = os.path.join(
                self.output_path_to_save_images,
                "mel",
                os.path.basename(audio).split(".")[0] + ".jpg",
            )

            self.spectogram_for_training(
                mfcc_output_path=mfcc_path,
                mel_output_path=mel_path,
                audio_path=audio,
                hight_frecuency_filter=self.config.get("hight_frecuency_filter", 0),
                low_frecuency_filter=self.config.get("low_frecuency_filter", 100000),
            )

            mfcc_image = Image.open(mfcc_path) if os.path.exists(mfcc_path) else None
            mel_image = Image.open(mel_path) if os.path.exists(mel_path) else None

            audios_images.append(
                {
                    "mfcc": mfcc_image,
                    "mel": mel_image,
                }
            )

        audios_data["audios_images"] = audios_images

        return audios_data
