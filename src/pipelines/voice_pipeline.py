from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import io
import librosa
import streamlit as st


@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()


def _as_embedding_vector(embedding):
    if embedding is None:
        return None

    try:
        vector = np.asarray(embedding, dtype=np.float64)
    except (TypeError, ValueError):
        return None
    if vector.ndim != 1 or vector.size == 0 or not np.all(np.isfinite(vector)):
        return None

    return vector


def get_voice_embedding(audio_bytes):
    try:
        encoder = load_voice_encoder()

        audio, _ = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        if audio.size == 0:
            raise ValueError('The audio recording is empty.')
        wav = preprocess_wav(audio)
        embedding = encoder.embed_utterance(wav)
        return embedding.tolist()
    except Exception as error:
        st.error(f'Could not process the voice recording: {error}')
        return None


def identify_speaker(new_embedding, candidates_dict, threshold=0.65):
    query_embedding = _as_embedding_vector(new_embedding)
    if query_embedding is None or not candidates_dict or not 0 <= threshold <= 1:
        return None, 0.0

    best_sid = None
    best_score = -1.0

    query_norm = np.linalg.norm(query_embedding)
    if query_norm == 0:
        return None, 0.0

    for sid, stored_embedding in candidates_dict.items():
        stored_vector = _as_embedding_vector(stored_embedding)
        if stored_vector is None or stored_vector.shape != query_embedding.shape:
            continue

        stored_norm = np.linalg.norm(stored_vector)
        if stored_norm == 0:
            continue

        similarity = float(np.dot(query_embedding, stored_vector) / (query_norm * stored_norm))
        if similarity > best_score:
            best_score = similarity
            best_sid = sid

    if best_score >= threshold:
        return best_sid, best_score

    return None, best_score


def process_bulk_audio(audio_bytes, candidates_dict, threshold=0.65):
    try:
        encoder = load_voice_encoder()

        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        if audio.size == 0:
            raise ValueError('The audio recording is empty.')
        segments = librosa.effects.split(audio, top_db=30)

        identified_results = {}

        for start, end in segments:
            if (end - start) < sr * 0.5:
                continue

            segment_audio = audio[start:end]
            wav = preprocess_wav(segment_audio)
            embedding = encoder.embed_utterance(wav)

            sid, score = identify_speaker(embedding, candidates_dict, threshold)

            if sid is not None:
                if sid not in identified_results or score > identified_results[sid]:
                    identified_results[sid] = score

        return identified_results
    except Exception as error:
        st.error(f'Could not analyze the audio recording: {error}')
        return None

    