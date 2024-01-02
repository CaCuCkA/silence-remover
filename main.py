import argparse
import os
from glob import glob

import numpy as np
from pyAudioAnalysis import audioBasicIO as aIO
from pyAudioAnalysis import audioSegmentation as aS
from pydub import AudioSegment
from scipy.io.wavfile import write


class AudioProcessor:
    def __init__(self, input_path, output_path="non_silent_output.wav", output_format="mp3"):
        self.input_path = input_path
        self.output_path = output_path
        self.output_format = output_format

    def process_audio(self):
        input_filename = os.path.basename(self.input_path)
        print(f"Processing {input_filename}...")

        Fs, x = aIO.read_audio_file(self.input_path)

        segments = aS.silence_removal(x,
                                      Fs,
                                      0.008,
                                      0.02,
                                      smooth_window=1.0,
                                      weight=0.2,
                                      plot=False)

        non_silent_audio = []
        for start, end in segments:
            non_silent_audio.extend(x[int(start * Fs):int(end * Fs)])

        non_silent_audio = np.array(non_silent_audio)

        return Fs, non_silent_audio, input_filename

    def save_as_wav(self, Fs, non_silent_audio):
        write(self.output_path, Fs, non_silent_audio)

    def convert_to_mp3(self):
        print(f"Converting to {self.output_format}...")
        audio = AudioSegment.from_wav(self.output_path)
        audio.export(self.output_path.replace(".wav", f".{self.output_format}"), format=self.output_format)

    def remove_silence_and_save(self):
        try:
            Fs, non_silent_audio, input_filename = self.process_audio()
            self.save_as_wav(Fs, non_silent_audio)
            self.convert_to_mp3()
            print(f"{input_filename} processing and conversion completed successfully.")
            print("=" * 100)

        except Exception as e:
            print(f"Error occurred during processing {input_filename}: {str(e)}")


def process_folder(input_folder, output_folder):
    mp3_files = glob(os.path.join(input_folder, '*.mp3'))

    for mp3_file in mp3_files:
        output_file = os.path.join(output_folder, os.path.basename(mp3_file))
        audio_processor = AudioProcessor(input_path=mp3_file, output_path=output_file)
        audio_processor.remove_silence_and_save()


def process_single_file(input_file, output_folder):
    input_filename = os.path.basename(input_file)
    output_file = os.path.join(output_folder, f"no_silence_{input_filename}")
    audio_processor = AudioProcessor(input_path=input_file, output_path=output_file)
    audio_processor.remove_silence_and_save()


def process_folder(input_folder, output_folder):
    mp3_files = glob(os.path.join(input_folder, '*.mp3'))

    for mp3_file in mp3_files:
        output_file = os.path.join(output_folder, os.path.basename(mp3_file))
        audio_processor = AudioProcessor(input_path=mp3_file, output_path=output_file)
        audio_processor.remove_silence_and_save()


def main():
    parser = argparse.ArgumentParser(description="Remove silence from audio files.")
    parser.add_argument("-i", "--input", help="Input folder path")
    parser.add_argument("-o", "--output", help="Output folder path")
    parser.add_argument("-f", "--file", help="Process a single file")
    args = parser.parse_args()

    if args.file:
        process_single_file(args.file, args.output or os.getcwd())
    elif args.input and args.output:
        process_folder(args.input, args.output)
    else:
        print("Invalid arguments. Use -h or --help for usage information.")


if __name__ == '__main__':
    main()
