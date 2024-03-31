from ProcessAudio.AudioAugmentation import AudioAugmentation
from ProcessAudio.Features import Features


class AllDataAugmentation(AudioAugmentation):

    def __init__(
        self,
        file_path,
        label: list = [None],
        path_save: str = "",
        to_graph: bool = False,
    ):
        """
        Initialize the class with the file path and the label
        """

        super().__init__(file_path, save=path_save, graph=to_graph)
        self.label = label

    def build_all(
        self,
        extract_features: bool = False,
        # select aumented
        original_included: bool = False,
        noise_aumented: bool = False,
        noise2_aumented: bool = False,
        stretch_aumented: bool = False,
        shift_aumented: bool = False,
        crop_aumented: bool = False,
        loudness_aumented: bool = False,
        speed_aumented: bool = False,
        normalizer_aumented: bool = False,
        polarizer_aumented: bool = False,
    ):
        """
        Build all data augmentation and extract features if it's necessary

        @type extract_features: bool
        @param extract_features: if True, extract features from all data

        @type original_included: bool
        @param original_included: if True, include the original data

        @type noise_aumented: bool
        @param noise_aumented: if True, include the noise data

        @type noise2_aumented: bool
        @param noise2_aumented: if True, include the noise2 data

        @type stretch_aumented: bool
        @param stretch_aumented: if True, include the stretch data

        @type shift_aumented: bool
        @param shift_aumented: if True, include the shift data

        @type crop_aumented: bool
        @param crop_aumented: if True, include the crop data

        @type loudness_aumented: bool
        @param loudness_aumented: if True, include the loudness data

        @type speed_aumented: bool
        @param speed_aumented: if True, include the speed data

        @type normalizer_aumented: bool
        @param normalizer_aumented: if True, include the normalizer data

        @type polarizer_aumented: bool
        @param polarizer_aumented: if True, include the polarizer data

        @rtype: list
        @return: all data and all labels
        """

        all_data = [
            self.get_original() if original_included else None,
            self.add_noise(noise_factor=0.05) if noise_aumented else None,
            self.add_noise2() if noise2_aumented else None,
            self.stretch(rate_stretch=0.8) if stretch_aumented else None,
            self.shift() if shift_aumented else None,
            self.add_crop() if crop_aumented else None,
            self.loudness() if loudness_aumented else None,
            self.speed() if speed_aumented else None,
            self.normalizer() if normalizer_aumented else None,
            self.polarizer() if polarizer_aumented else None,
        ]

        all_data = [x for x in all_data if x is not None]

        if extract_features:
            print("Extracting features to", self.audio_file)
            all_data = self.extract_features(all_data)

        all_label = [self.label for _ in range(len(all_data))]
        return all_data, all_label

    def extract_features(self, all_data) -> list:
        """
        Extract features from all data

        @type all_data: list
        @param all_data: list of audio data

        @rtype: list
        @return: list of features
        """

        features = Features(complete_answer=False)

        for i in range(len(all_data)):

            info_audio = (all_data[i], self.rate)
            features.set_data(info_audio)

            all_data[i] = features.build_basic()

        return all_data
