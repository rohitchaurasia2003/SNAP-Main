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

    vector = np.asarray(embedding, dtype=np.float64)
    if vector.ndim != 1 or vector.size == 0:
        return None

    return vector


def get_voice_embedding(audio_bytes):
    try:
        encoder = load_voice_encoder()

        audio, _ = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        wav = preprocess_wav(audio)
        embedding = encoder.embed_utterance(wav)
        return embedding.tolist()
    except Exception:
        st.error('Voice recog error')
        return None


def identify_speaker(new_embedding, candidates_dict, threshold=0.65):
    try:
        query_embedding = _as_embedding_vector(new_embedding)
        if query_embedding is None or not candidates_dict:
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
    except Exception:
        return None, 0.0


def process_bulk_audio(audio_bytes, candidates_dict, threshold=0.65):
    try:
        encoder = load_voice_encoder()

        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        segments = librosa.effects.split(audio, top_db=30)

        identified_results = {}

        for start, end in segments:
            if (end - start) < sr * 0.5:
                continue

            segment_audio = audio[start:end]
            wav = preprocess_wav(segment_audio)
            embedding = encoder.embed_utterance(wav)

            sid, score = identify_speaker(embedding, candidates_dict, threshold)

            if sid:
                if sid not in identified_results or score > identified_results[sid]:
                    identified_results[sid] = score

        return identified_results
    except Exception:
        st.error('Bulk process error')
        return {}

    