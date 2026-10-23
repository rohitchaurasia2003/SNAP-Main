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
    
    # 1. Initialize session states safely
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    # 2. Grab URL query parameters at the absolute start of execution
    join_code = st.query_params.get('join-code')

    # 3. Handle routing rules and user transitions cleanly BEFORE rendering layout elements
    if join_code and st.session_state['login_type'] != 'student':
        st.session_state['login_type'] = 'student'
        st.layer_changed = True  # Custom trigger state flag to ensure clean sync pass
        st.rerun()

    # 4. Safely handle the Modal Dialog trigger condition using a boolean gate
    if join_code and st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
        if not st.session_state.get('enrollment_dialog_active'):
            st.session_state['enrollment_dialog_active'] = True
            auto_enroll_dialog(join_code)
    else:
        # Clear dialog tracking if conditional parameters are missing
        st.session_state['enrollment_dialog_active'] = False

    # 5. Render primary visual routing layers securely
    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()

        case 'student':
            student_screen()
        
        case None:
            home_screen()

if __name__ == "__main__":
    main()
