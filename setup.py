import cx_Freeze
import os

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
     'TARGETDIR'               # WkDir
     )
    ]

msi_data = {"Shortcut": shortcut_table}
bdist_msi_options = {'data': msi_data}

mkl_dlls = ["mkl_intel_thread.dll", "mkl_core.dll", "libiomp5md.dll"]

cx_Freeze.setup(
    name="Nurikabe",
    author= "Alexandre Thiault",
    description="Nurikabe jouable sur Windows 10",
    options={
            "build_exe": {"packages":["os", "pygame", "ctypes"],
                            "excludes":["babel", "cryptography", "Cython", "distutils", "docutils", "IPython", "jedi", "llvmlite", "lxml", "markupsafe", "matplotlib", "mkl", "nbconvert", "numba", "numpy", "PIL", "prompt_toolkit", "psutil", "PyQt5", "pytest", "pytz", "scipy", "sphinx", "tkinter", "tornado", "win32com", "zmq"]+["email", "html", "http", "logging", "pkg_resources", "pydoc_data", "pyreadline", "test", "unittest", "urllib"],
                            "include_files": ["Icones","Grilles"]+ [os.path.join(PYTHON_INSTALL_DIR,"Library","bin",i) for i in mkl_dlls]
            },
            "bdist_msi": bdist_msi_options,
    },
    executables = [
            cx_Freeze.Executable(script="Nurikabe.py",
                base="Win32GUI",
                targetName = "Nurikabe.exe",
                icon=os.path.join("Icones","app_icon.ico"),
                #shortcutName = "Nurikabe",
                #shortcutDir = "DesktopFolder"
            ),
            cx_Freeze.Executable("grille_vide.py")
            ]
    )

# python setup.py build         pour créer l'exécutable
# python setup.py bdist_msi     pour créer l'installeur