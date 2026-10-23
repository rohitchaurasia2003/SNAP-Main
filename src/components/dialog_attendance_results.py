import streamlit as st

from src.database.db import create_attendance

def show_attendance_result(df, logs):
    st.write('Please review attendance before confirming.')
    st.dataframe(df, hide_index=True, width='stretch')

    col1, col2 = st.columns(2)

    with col1:
        if st.button('Discard', width='stretch'):
            st.session_state.voice_attendance_results = None
            st.session_state.attendance_images = []
            st.session_state.attendance_image_hashes = set()
            st.rerun()

    with col2:
        if st.button('Confirm & Save', width='stretch', type='primary'):
            try:
                if not logs:
                    st.warning('There are no attendance records to save.')
                    return
                create_attendance(logs)
                st.toast("Attendance taken")
                st.session_state.attendance_images = []
                st.session_state.attendance_image_hashes = set()
                st.session_state.voice_attendance_results = None
                st.rerun()
            except Exception as error:
                st.error(f'Could not save attendance: {error}')



@st.dialog("Attendance Reports")
def attendance_result_dialog(df, logs):
    show_attendance_result(df, logs)