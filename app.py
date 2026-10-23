import streamlit as st

from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen

from src.components.dialog_auto_enroll import auto_enroll_dialog

def main():
    st.set_page_config(
        page_title='Snap - Making Attendance faster using AI',
        page_icon= "https://ibb.co"
    )
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    # 1. Grab query params at the beginning of the execution run
    join_code = st.query_params.get('join-code')

    # 2. Handle automatic login type navigation if a join-code is present
    if join_code and st.session_state.login_type != 'student':
        st.session_state.login_type = 'student'
        st.rerun()

    # 3. Handle modal dialog triggers safely before layout builds
    if join_code and st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
        if not st.session_state.get('enrollment_dialog_active'):
            st.session_state.enrollment_dialog_active = True
            auto_enroll_dialog(join_code)
    else:
        # Reset toggle tracker when no join parameters exist or active state drops
        st.session_state.enrollment_dialog_active = False

    # 4. Render primary application view routing
    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()

        case 'student':
            student_screen()
        
        case None:
            home_screen()

if __name__ == "__main__":
    main()
