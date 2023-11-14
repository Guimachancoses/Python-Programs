import sys
from cx_Freeze import setup, Executable


base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable("sizePst.py", base=base)
]

buildOptions = dict(
    packages=[],
    includes=[],
    include_files=[],
    excludes=[]
)

setup(
    name="sizePst",
    author="System",
    author_email="guilherme.machancoses@gmail.com",
    version="1.0",
    description="sizeAchivePst",
    options=dict(build_exe=buildOptions),
    executables=executables
)
