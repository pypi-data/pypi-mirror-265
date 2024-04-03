import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_cookies_manager import EncryptedCookieManager
from authlit.utils import (
    authenticate_user,
    generate_otp,
    get_otp,
    is_valid_username,
    is_email_valid,
    is_email_unique,
    is_username_unique,
    register_user,
    update_password
)
from authlit.email.send_mail import send_otp_via_email


class AuthUI:
    """
    Builds the UI for the Login/Sign Up page.
    """
    def __init__(
        self,
        company_name: str,
        logout_button_name: str = "Logout",
        hide_menu_bool: bool = False,
        hide_footer_bool: bool = False,
    ):
        """
        Arguments:
        -----------
        1. self
        2. company_name : This is the name of the person/ organization which will send the password reset email.
        3. logout_button_name : The logout button name.
        4. hide_menu_bool : Pass True if the streamlit menu should be hidden.
        5. hide_footer_bool : Pass True if the 'made with streamlit' footer should be hidden.
        """
        self.company_name = company_name
        self.logout_button_name = logout_button_name
        self.hide_menu_bool = hide_menu_bool
        self.hide_footer_bool = hide_footer_bool

        self.cookies = EncryptedCookieManager(
            prefix="streamlit_login_ui_yummy_cookies",
            password="9d68d6f2-4258-45c9-96eb-2d6bc74ddbb5-d8f49cab-edbb-404a-94d0-b25b1d4a564b",
        )

        if not self.cookies.ready():
            st.stop()


    def get_username(self):
        if st.session_state["LOGOUT_BUTTON_HIT"] == False:
            fetched_cookies = self.cookies
            if "__streamlit_login_signup_ui_username__" in fetched_cookies.keys():
                username = fetched_cookies["__streamlit_login_signup_ui_username__"]
                return username


    def login_widget(self) -> None:
        """
        Creates the login widget, checks and sets cookies, authenticates the users.
        """

        # Checks if cookie exists.
        if st.session_state["LOGGED_IN"] == False:
            if st.session_state["LOGOUT_BUTTON_HIT"] == False:
                fetched_cookies = self.cookies
                if "__streamlit_login_signup_ui_username__" in fetched_cookies.keys():
                    if (
                        fetched_cookies["__streamlit_login_signup_ui_username__"]
                        != "1c9a923f-fb21-4a91-b3f3-5f18e3f01182"
                    ):
                        st.session_state["LOGGED_IN"] = True

        if st.session_state["LOGGED_IN"] == False:
            st.session_state["LOGOUT_BUTTON_HIT"] = False
            _, sc, _ = st.columns([2, 3, 2])
            del_login = sc.empty()
            with del_login.form("Login Form"):
                username = st.text_input("Username", placeholder="Your unique username")
                password = st.text_input(
                    "Password", placeholder="Your password", type="password"
                )

                st.markdown("###")
                login_submit_button = st.form_submit_button(label="Login")

                if login_submit_button == True:
                    authenticate_user_check = authenticate_user(
                        username, password
                    )

                    if authenticate_user_check == False:
                        st.error("Invalid Username or Password!")

                    else:
                        st.session_state["LOGGED_IN"] = True
                        self.cookies["__streamlit_login_signup_ui_username__"] = (
                            username
                        )
                        self.cookies.save()
                        del_login.empty()
                        st.experimental_rerun()

    def sign_up_widget(self) -> None:
        """
        Creates the sign-up widget and stores the user info in a secure way in the _secret_auth_.json file.
        """
        _, sc, _ = st.columns([2, 3, 2])
        with sc.form("Sign Up Form"):
            name_sign_up = st.text_input("Name *", placeholder="Please enter your name")
            valid_name_check = is_valid_username(name_sign_up)

            email_sign_up = st.text_input(
                "Email *", placeholder="Please enter your email"
            )
            valid_email_check = is_email_valid(email_sign_up)
            unique_email_check = is_email_unique(email_sign_up)

            username_sign_up = st.text_input(
                "Username *", placeholder="Enter a unique username"
            )
            unique_username_check = is_username_unique(username_sign_up)

            password_sign_up = st.text_input(
                "Password *", placeholder="Create a strong password", type="password"
            )

            st.markdown("###")
            sign_up_submit_button = st.form_submit_button(label="Register")

            if sign_up_submit_button:
                if not valid_name_check:
                    st.error("Please enter a valid name!")
                    return

                if not valid_email_check:
                    st.error("Please enter a valid Email!")
                    return

                if not unique_email_check:
                    st.error("Email already exists!")
                    return

                if unique_username_check is None:
                    st.error("Please enter a non - empty Username!")
                    return

                if not unique_username_check:
                    st.error(f"Sorry, username {username_sign_up} already exists!")
                    return

                register_user(
                    name_sign_up,
                    email_sign_up,
                    username_sign_up,
                    password_sign_up,
                )
                st.success("Registration Successful!")

    def forgot_password(self) -> None:
        """
        Creates the forgot password widget and after user authentication (email), triggers an email to the user
        containing a random password.
        """
        if 'forgot_pass' not in st.session_state:
            st.session_state['forgot_pass'] = 'enter_email'

        _, sc, _ = st.columns([2, 3, 2])
        with sc.form("Forgot Password Form"):
            if st.session_state['forgot_pass'] == 'enter_email':
                email = st.text_input(
                    "Email", placeholder="Please enter your email"
                )
                send_otp = st.form_submit_button(label="Send OTP")
                if send_otp:
                    if is_email_valid(email):
                        otp = generate_otp(300)
                        print(otp)
                        send_otp_via_email(email, email, self.company_name, otp)
                        st.session_state['forgot_pass'] = 'enter_otp'
                        st.session_state['email'] = email
                    else:
                        st.error("Invalid Email!")
            
            elif st.session_state['forgot_pass'] == 'enter_otp':
                st.info("An OTP has been sent to your email. Please enter the OTP.")
                otp = st.text_input(
                    "OTP", placeholder="Please enter the OTP sent to your email"
                )
                submit_otp = st.form_submit_button(label="Submit OTP")
                if submit_otp:
                    if otp.isdigit() and int(otp) == get_otp():
                        st.session_state['forgot_pass'] = 'enter_new_password'
                    else:
                        st.error("Invalid OTP!")

            elif st.session_state['forgot_pass'] == 'enter_new_password':
                st.info("Please enter a new password.")
                new_password = st.text_input(
                    "New Password", placeholder="Please enter the new password"
                )
                confirm_password = st.text_input(
                    "Confirm Password", placeholder="Please confirm the new password"
                )
                reset_password = st.form_submit_button(label="Reset Password")
                if reset_password:
                    if new_password != confirm_password:
                        st.error("Passwords don't match!")
                    else:
                        email = st.session_state.get('email')
                        update_password(new_password, email=email)
                        st.session_state['forgot_pass'] = 'password_set'

            elif st.session_state['forgot_pass'] == 'password_set':
                st.success("Password reset successful!")
                ok = st.form_submit_button(label="OK")
                if ok:
                    st.session_state['forgot_pass'] = 'enter_email'


    def logout_widget(self) -> None:
        """
        Creates the logout widget in the sidebar only if the user is logged in.
        """
        if st.session_state["LOGGED_IN"] == True:
            st.sidebar.markdown("## Hi"+ " " + self.get_username())
            del_logout = st.sidebar.empty()
            del_logout.markdown("#")
            logout_click_check = del_logout.button(self.logout_button_name)

            if logout_click_check == True:
                st.session_state["LOGOUT_BUTTON_HIT"] = True
                st.session_state["LOGGED_IN"] = False
                self.cookies["__streamlit_login_signup_ui_username__"] = (
                    "1c9a923f-fb21-4a91-b3f3-5f18e3f01182"
                )
                del_logout.empty()
                st.experimental_rerun()

    def nav_sidebar(self):
        """
        Creates the side navigaton bar
        """
        main_page_sidebar = st.sidebar.empty()
        with main_page_sidebar:
            selected_option = option_menu(
                menu_title="Navigation",
                menu_icon="list-columns-reverse",
                icons=[
                    "box-arrow-in-right",
                    "person-plus",
                    "x-circle",
                    "arrow-counterclockwise",
                ],
                options=[
                    "Login",
                    "Create Account",
                    "Forgot Password?",
                ],
                styles={
                    "container": {"padding": "5px"},
                    "nav-link": {
                        "font-size": "14px",
                        "text-align": "left",
                        "margin": "0px",
                    },
                },
            )
        return main_page_sidebar, selected_option

    def hide_menu(self) -> None:
        """
        Hides the streamlit menu situated in the top right.
        """
        st.markdown(
            """ <style>
        #MainMenu {visibility: hidden;}
        </style> """,
            unsafe_allow_html=True,
        )

    def hide_footer(self) -> None:
        """
        Hides the 'made with streamlit' footer.
        """
        st.markdown(
            """ <style>
        footer {visibility: hidden;}
        </style> """,
            unsafe_allow_html=True,
        )

    def build_login_ui(self):
        """
        Brings everything together, calls important functions.
        """
        if "LOGGED_IN" not in st.session_state:
            st.session_state["LOGGED_IN"] = False

        if "LOGOUT_BUTTON_HIT" not in st.session_state:
            st.session_state["LOGOUT_BUTTON_HIT"] = False

        main_page_sidebar, selected_option = self.nav_sidebar()

        if selected_option == "Login":
            self.login_widget()

        if selected_option == "Create Account":
            self.sign_up_widget()

        if selected_option == "Forgot Password?":
            self.forgot_password()


        self.logout_widget()

        if st.session_state["LOGGED_IN"] == True:
            main_page_sidebar.empty()

        if self.hide_menu_bool == True:
            self.hide_menu()

        if self.hide_footer_bool == True:
            self.hide_footer()

        return st.session_state["LOGGED_IN"]
