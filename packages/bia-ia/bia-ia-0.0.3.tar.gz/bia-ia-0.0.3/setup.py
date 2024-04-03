# --------------------------
# Deploy folder
#
# setup definition
# --------------------------

from setuptools import setup

__project__ = "bia-ia"
__version__ = "0.0.3"
__description__ = "BIA (IA), your IA powered vocal assistant"
__packages__ = ["bia-ia", "bia-ia.utils", "bia-ia.controllers", "bia-ia.models.blocks", "bia-ia.models.database", "bia-ia.models.openAI", "bia-ia.models.robot", "bia-ia.models.speech", "bia-ia.data", "bia-ia.deploy", "bia-ia.views", "bia-ia.bin"]
__author__ = "TylerDDDD"
__author_email__ = "makertylerdddd@gmail.com"
__classifiers__ = [
	"Development Status :: 3 - Alpha", 
	"Intended Audience :: Education", 
	"Programming Language :: Python :: 3",
]
__readme__ = "README.md"
__keywords__ = ["robot", "otto", "ai", "vocal", "assistant",]
__requires__ = ["nltk", "openai", "websockets", "argostranslate", "py3langid", "pyautogui", "pyaudio", "speechrecognition", "pyttsx3", "parrot", "opencv-python", "customtkinter", "pyduinocli", "webbrowser"]

setup(
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    author = __author__,
    author_email = __author_email__,
    classifiers = __classifiers__,
    readme = __readme__,
    keywords = __keywords__,
    install_requires = __requires__,
    package_data={'bia': ['config.cfg', '_config.cfg', 'bia.db']},
    include_package_data=True,
)
