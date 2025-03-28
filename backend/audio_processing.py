# audio_processing.py
import librosa
import numpy as np

def extract_features(audio_path: str):
    """
    Extract pitch, tempo, etc. from audio file using librosa.
    Return a dictionary with relevant features.
    """
    y, sr = librosa.load(audio_path, sr=None, mono=True)

    # 1. Pitch Estimation (using librosa's piptrack or yin)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_values = []
    for i in range(len(magnitudes[0])):
        index = magnitudes[:, i].argmax()
        pitch = pitches[index, i]
        if pitch > 0:
            pitch_values.append(pitch)
    mean_pitch = np.mean(pitch_values) if pitch_values else 0.0

    # Alternatively, we could use librosa.yin for fundamental frequency:
    # f0 = librosa.yin(y, fmin=50, fmax=2000)
    # mean_pitch = np.mean(f0)

    # 2. Tempo/Rhythm
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    # beat_frames gives the frame indices of the beat events
    # from that we can derive rhythmic consistency if we want
    # For demonstration, just storing the 'tempo' measure
    rhythm_consistency = np.std(np.diff(beat_frames)) if len(beat_frames) > 2 else 0.0

    # 3. Tempo consistency (laye) approximation:
    # We'll define "tempo consistency" as the standard deviation of the beat intervals:
    tempo_consistency = 1.0 / (1.0 + rhythm_consistency)  # invert for "larger is better"

    # 4. Pitch quality: We can approximate by the standard deviation of the pitch
    pitch_std = np.std(pitch_values) if pitch_values else 0.0
    pitch_quality = 1.0 / (1.0 + pitch_std)

    # 5. Pace: We might define pace as how quickly the user is singing relative
    # to the track length or relative to the measured tempo. 
    # For demonstration, let's just store the tempo as "pace."
    pace = tempo  

    return {
        "mean_pitch": float(mean_pitch),
        "tempo": float(tempo),
        "tempo_consistency": float(tempo_consistency),
        "pitch_quality": float(pitch_quality),
        "pace": float(pace)
    }
