import os, sys, cx_Freeze, pygame

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))

shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "Nurikabe",               # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]Nurikabe.exe",# Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     "",                       # Icon
     0,                        # IconIndex
     None,                     # ShowCmd
     "TARGETDIR"               # WkDir
    )
]


if pygame.__version__ < "2":
    incl_dlls = ["libiomp5md.dll", "mkl_intel_thread.dll", "mkl_core.dll"]
else:
    incl_dlls = [] # This will indeed make the app wayyyy lighter
incl_dlls = [os.path.join(PYTHON_INSTALL_DIR,"Library","bin",i) for i in incl_dlls]

excludes = ["babel", "cryptography", "Cython", "distutils", "docutils", "IPython", "jedi", "llvmlite", "lxml", "markupsafe", "matplotlib", "mkl", "nbconvert", "numba", "numpy", "PIL", "prompt_toolkit", "psutil", "PyQt5", "pytest", "pytz", "scipy", "sphinx", "tkinter", "tornado", "win32com", "zmq", "email", "html", "http", "logging", "pkg_resources", "pydoc_data", "pyreadline", "test", "unittest", "urllib", "xml"]

base = None
if sys.platform == "win32":
    base = "Win32GUI"

cx_Freeze.setup(
    name="Nurikabe",
    author= "Alexandre Thiault",
    description="Nurikabe numérique pour Windows 10",
    options=
    {
        "build_exe":
        {
            "packages": ["pygame", "ctypes"],
            "excludes": excludes,
            "include_files": ["cleanup.bat", "cleanup.sh", "Icones", "Grilles"] + incl_dlls
        },
        "bdist_msi":
        {
            "data": {"Shortcut": shortcut_table}
        },
    },
    executables =
    [
        cx_Freeze.Executable(
            script="Nurikabe.py",
            base=base,
            targetName="Nurikabe.exe",
            icon=os.path.join("Icones","app_icon.ico"),
        ),
        #cx_Freeze.Executable("grille_vide.py")
    ]
)

# python setup.py build         -> exe
# python setup.py bdist_msi     -> msi and exe