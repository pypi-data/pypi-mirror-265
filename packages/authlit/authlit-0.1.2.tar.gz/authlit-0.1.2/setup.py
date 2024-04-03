import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="authlit",
    version="0.1.2",
    author="Badal Sahani",
    author_email="badalsahani8381@gmail.com",
    description="A streamlit library which provides a Login/Sign-Up UI with an option to reset password, also supports cookies.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AGI-24/st-auth.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "streamlit",
        "extra_streamlit_components",
        "streamlit_option_menu",
        "streamlit_cookies_manager",
        "sqlalchemy",
        "pymysql",
        "pymongo",
        "argon2-cffi",
        "bcrypt",
        "PyYAML",
    ],
)
