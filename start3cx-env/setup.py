import sys
from cx_Freeze import setup, Executable


base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable("CkVoipWeb.py", base=base)
]

buildOptions = dict(
    packages=[],
    includes=[],
    include_files=[],
    excludes=[]
)

setup(
    name="CkVoip",
    author="System",
    author_email="guilherme.machancoses@gmail.com",
    version="1.0",
    description="RunTreeCx",
    options=dict(build_exe=buildOptions),
    executables=executables
)
