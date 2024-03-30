import numpy as np
import matplotlib.pyplot as plt
import librosa
#import crepe
import json

class Waveform:
    def __init__(self, fp: str = None, sample_rate: int = 8000, duration: int = 30):
        self.fp = fp
        self.sample_rate = sample_rate
        self.interval = 1 / self.sample_rate
        
        self.duration = duration
        self.samples = np.array(0)
    
        self._process()
    
    def __repr__(self):
        return f"Waveform({self.duration}s, {self.duration * self.samples} samples)"
    
    @staticmethod
    def normalise(samples: np.ndarray) -> np.ndarray:
        return samples / np.max(np.abs(samples))
        
    def _process(self):
        self.samples, _ = librosa.load(self.fp, sr=self.sample_rate, duration=self.duration)
        self.samples = self.normalise(self.samples)
        self.tempo, self.beat_frames = librosa.beat.beat_track(y=self.samples, sr=self.sample_rate)
        self.beat_times = librosa.frames_to_time(self.beat_frames, sr=self.sample_rate)
        
    @property
    def deviation(self) -> list: 
        # relative squared deviation (mse w.r.t. mean ~= 0)
        # how "exciting" the moment is compared to the average moment in the song i suppose
        return self.normalise((self.samples - np.mean(self.samples)) ** 2)

    
"""
    def spectrogram_pitch_analysis(self):
        self.S = np.abs(librosa.stft(self.samples, center=False, hop_length=10))

        fig, ax = plt.subplots()
        img = librosa.display.specshow(librosa.amplitude_to_db(self.S, ref=np.max), y_axis='log', x_axis='time', ax=ax)
        times = librosa.frames_to_time(self.S, sr=self.sample_rate, hop_length=10)
        print(times)
        ax.set_title('Power spectrogram')

        fig.colorbar(img, ax=ax, format="%+2.0f dB")
        #plt.xlim([0, len(self.samples) / self.sample_rate])
        
        
        
        plt.show()
        
        pitches, _ = librosa.piptrack(S=self.S, sr=self.sample_rate)

        # Extract pitch values for each time frame
        mean_pitch = np.mean(pitches, axis=1)

        # Create time axis
        times = librosa.times_like(mean_pitch)
        #print(times, mean_pitch)
        # Plot pitch values over time
        plt.figure(figsize=(10, 4))
        plt.plot(times, mean_pitch, label='Pitch')
        plt.xlabel('Time (s)')
        plt.ylabel('Pitch (Hz)')
        plt.title('Pitch Tracking')
        plt.legend()
        plt.grid()
        plt.show()
        """