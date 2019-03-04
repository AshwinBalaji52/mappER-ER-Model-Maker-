import cx_Freeze
import sys
import os
import graphviz
import tkinter


os.environ['TCL_LIBRARY'] =r'C:/Python/Python36-32/tcl/tcl8.6'
os.environ['TK_LIBRARY'] = r'C:/Python/Python36-32/tcl/tk8.6'


base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("mappER.py", base=base, icon="mappER_Image.ico")]

cx_Freeze.setup(
    name = "mappER",
    options = {"build_exe": {"packages":["tkinter","graphviz","os"], "include_files":["mappER_Image.ico"]}},
    version = "1.0",    description = "Entity Relation Diagram Maker",
    executables = executables
    )
