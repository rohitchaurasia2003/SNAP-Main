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

    
    join_code = st.query_params.get('join-code')

    
    if join_code and st.session_state['login_type'] != 'student':
        st.session_state['login_type'] = 'student'
        st.layer_changed = True  # Custom trigger state flag to ensure clean sync pass
        st.rerun()

    
    if join_code and st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
        if not st.session_state.get('enrollment_dialog_active'):
            st.session_state['enrollment_dialog_active'] = True
            auto_enroll_dialog(join_code)
    else:
        
        st.session_state['enrollment_dialog_active'] = False

    
    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()

        case 'student':
            student_screen()
        
        case None:
            home_screen()

if __name__ == "__main__":
    main()
