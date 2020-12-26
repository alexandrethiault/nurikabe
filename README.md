# Nurikabe
A simple pygame implementation for the Nurikabe grid game provided with a setup.py file to build a standalone Windows 10 exe app with cx_Freeze, and a 4.6 MB zip of a pre-built version.

## Play the game by executing Nurikabe.py

You will need Python 3.7 (or more recent) installed on your computer (see https://www.anaconda.com/distribution/ for a Python distribution, or https://pyzo.org/start.html if you also want an integrated development environment).

If not already done, install the pygame module (version >=1.9, preferably >=2.0). This can be done with the ´pip install pygame´ command.

To launch the game, you can either use the ´python Nurikabe.py´ command in the directory where you placed the repository, or directly execute the Nurikabe.py file opened in your favorite IDE.

## Build an exe installer with setup.py

Install the cx_Freeze module with ´pip install cx_Freeze´ and execute the ´python setup.py bdist_msi´ command in the directory where you placed the repository. A distribuable .msi installer (up to 60 MB depending on your Python version with pygame 1.9.x, 15 MB with pygame 2.0.x) has been created in the ´dist/´ folder. You can delete the ´build/´ folder.

The remaining installation step doesn't require having a Python environment on your computer as a .msi installer is by nature already standalone.

Simply double click the .msi installer and follow the instructions to install a standalone .exe app. Once this step is completed, go to the folder where it has been installed (the default is ´C:/Users/[you]/AppData/Programs/Nurikabe´). If you see a ´cleanup.bat´ next to ´Nurikabe.exe´ (it will only be there if the .msi installer was created with the pygame version being at least 2.0, don't try to add it manually if it's not there), double click it (or ´cleanup.sh´ if you prefer). This will remove a lot of unnecessary files and modules that cx_Freeze added, representing 70%+ of the total size of the app. The remaining files should be exactly those included in ´Nurikabe.zip´ from this repository, the difference being that simply unzipping it does not create a desktop shortcut.
