import streamlit as st
import segno
import io
from urllib.parse import quote


@st.dialog("Share Class Link")
def share_subject_dialog(subject_name, subject_code):
    app_domain = "remotesnapclass-main.streamlit.app"
    join_url = f"https://{app_domain}/?join-code={quote(str(subject_code), safe='')}"

    st.header("Scan to Join")

    qr = segno.make(join_url)

    out = io.BytesIO()

    qr.save(out, kind='png', scale=10, border=1)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('### Copy Link')
        st.link_button('Open class join link', join_url, width='stretch')
        st.code(join_url, language="text")
        st.code(subject_code, language="text")
        st.info('Copy this link to share on Whatsapp or Email')

    with col2:
        st.markdown('### Scan to Join')
        st.image(out.getvalue(), caption='QRCODE for class joining')

        