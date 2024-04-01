from authlit import AuthUI
import streamlit as st

auth = AuthUI(
    company_name="AGI24",
    hide_menu_bool=False,
    hide_footer_bool=True,
)

if __name__ == "__main__":
    LOGGED_IN = auth.build_login_ui()

    if LOGGED_IN == True:
        col1, col2 = st.columns(2)
        with col1:
            st.title("AGI24")