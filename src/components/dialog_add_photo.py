import hashlib
from io import BytesIO

import streamlit as st
from PIL import Image


def _add_photo(image_bytes):
    image_hash = hashlib.sha256(image_bytes).hexdigest()
    image_hashes = st.session_state.setdefault('attendance_image_hashes', set())
    if image_hash in image_hashes:
        return False

    try:
        image = Image.open(BytesIO(image_bytes)).convert('RGB')
    except (OSError, ValueError) as error:
        st.error(f'Could not read image: {error}')
        return False

    st.session_state.setdefault('attendance_images', []).append(image)
    image_hashes.add(image_hash)
    return True


@st.dialog("Capture or upload photos")
def add_photos_dialog():
    st.write('Add classroom photos to scan for attendance')

    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'camera'
    if 'photo_dialog_instance' not in st.session_state:
        st.session_state.photo_dialog_instance = 0
    st.session_state.setdefault('attendance_images', [])
    st.session_state.setdefault('attendance_image_hashes', set())

    t1, t2 = st.columns(2)

    with t1:
        type_camera = "primary" if st.session_state.photo_tab == 'camera' else 'tertiary'
        if st.button('Camera', type=type_camera, width='stretch'):
            st.session_state.photo_tab = 'camera'



    with t2:
        type_upload = "primary" if st.session_state.photo_tab == 'upload' else 'tertiary'
        if st.button('Upload photos', type=type_upload, width='stretch'):
            st.session_state.photo_tab = 'upload'

    if st.session_state.photo_tab == 'camera':
        cam_photo = st.camera_input(
            'Take Snapshot',
            key=f"dialog_cam_{st.session_state.photo_dialog_instance}",
        )
        if cam_photo:
            if _add_photo(cam_photo.getvalue()):
                st.toast('Photo Captured')


    if st.session_state.photo_tab == 'upload':
        uploaded_files = st.file_uploader(
            'Choose image files',
            type=['jpg', 'png', 'jpeg'],
            accept_multiple_files=True,
            key=f"dialog_upload_{st.session_state.photo_dialog_instance}",
        )

        if uploaded_files:
            added_count = 0
            for f in uploaded_files:
                if _add_photo(f.getvalue()):
                    added_count += 1
            if added_count:
                st.toast(f'{added_count} photo(s) uploaded successfully')

    st.divider()
    if st.button('Done', type='primary', width='stretch'):
        st.session_state.photo_dialog_instance += 1
        st.session_state.photo_tab = 'camera'
        st.rerun()