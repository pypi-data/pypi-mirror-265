import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np
import os
import json

from MusicInsights.Waveform import Waveform

def overload(Type):
    def decorator(func):
        def wrapper(*args):
            if len(args) == 2:
                return func(*args)
            
            elif len(args) == 1 and isinstance(args[0], Type):
                return func(args[0].samples, args[0].sample_rate)
            
            else:
                raise TypeError("Invalid args")
            
        return wrapper
    return decorator

@overload(Waveform)
def playback(samples: list[float], sample_rate: int) -> None:
    """ Playback audio sampled from mp3

    Args:
        samples (list[float]): np.ndarray of (normalised) amplitudes
        sample_rate (int): sample rate of samples
        
    Args:
        waveform (Waveform): Waveform object instance
    """
    
    assert sample_rate >= 8000, "Sample rate must be >= 8000" # replayer requires >= 8000
        
    sd.play(samples, sample_rate)  
    sd.wait() 

@overload(Waveform)

def visualise(samples: list[float], sample_rate: int) -> None:
    """ Visualise amplitudes in audio waveform

    Args:
        samples (list[float]): np.ndarray of (normalised) amplitudes
        sample_rate (int): sample rate of samples
        
    Args:
        waveform (Waveform): Waveform object instance
    """
    
    time = np.arange(len(samples)) / sample_rate

    plt.plot(time, samples)
    
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    
    plt.title('Waveform')
    
    plt.grid(True)
    plt.show()
    
def to_json(waveform, directory, freq_stft=None) -> None: # TODO actually understand and implement librosa.piptrack (requires some weird lerping) or crepe for frequency analysis and subsequent mode/chroma analysis - time investment likely not worth the effort
    with open(directory + f"\\{os.path.splitext(os.path.split(waveform.fp)[-1])[0]}.json", "w") as f:
        json.dump(
            {
                "mean_tempo": waveform.tempo,
                "sample_rate": waveform.sample_rate,
                "samples": {
                    p: {
                        "elapsed_time": float(waveform.interval * p),
                        "amplitude": np.abs(float(s)),
                        "deviation": float(waveform.deviation[p]),
                        "beat": p in waveform.beat_frames,
                    }
                    for p, s in enumerate(waveform.samples)    
                },
            },
            f,
            indent=2
        )
        
""" JSON {
    average_tempo (bpm): int,
    
    samples{
        sample_index: {
            elapsed_time (s): float, # consider ms for crepe
            amplitude: float,
            deviation: float,
            beat: bool, # separates music into "beat" intervals, potentially generate separate animateddiff per beat segment
            frequency (from stft): float,
            pitch (from piptrack): float,
            mode (major/minor): str,
        }
        ...
    }
}

"""