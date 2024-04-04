from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="yayy",
    version="0.1.3",
    author="Pablo Escobar",
    description="Si Un Problema Puede Solucionarse, Entonces No Vale La Pena Preocuparse Por El.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["pyperclip", "google-generativeai", "pyautogui"],
    entry_points={
        "console_scripts": [
            "fkvit=yayy.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={'yayy': ['assets/*.json']},
    include_package_data=True,
    license="MIT"
)