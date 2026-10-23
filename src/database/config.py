import os

import streamlit as st
from supabase import Client, create_client

SUPABASE_URL = st.secrets.get('SUPABASE_URL') or os.getenv('SUPABASE_URL')
SUPABASE_KEY = st.secrets.get('SUPABASE_KEY') or os.getenv('SUPABASE_KEY')

supabase: Client | None = (
    create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None
)


def require_supabase() -> Client:
    if supabase is None:
        raise RuntimeError(
            'Supabase is not configured. Add SUPABASE_URL and SUPABASE_KEY to '
            'Streamlit secrets or environment variables.'
        )
    return supabase