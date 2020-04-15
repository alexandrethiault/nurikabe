# Nurikabe
A simple pygame implementation for the Nurikabe grid game provided with a setup.py file to build a standalone exe app with cx_Freeze.

## Play the game by executing Nurikabe.py

You will need python 3.7 (or more recent) installed on your computer (see https://www.anaconda.com/distribution/ for a Python distribution, or https://pyzo.org/start.html if you also want an integrated development environment).

If not already done, install the pygame module. This can be done with the ´pip install pygame´ command.

To execute the python script, you can either use the ´python Nurikabe.py´ command in the directory where you placed the repository, or directly execute the Nurikabe.py file opened in an IDE.

## Build an exe installer with setup.py

Install the cx_Freeze module with ´pip install cx_Freeze´ and execute the ´python setup.py bdist_msi´ command in the directory where you placed the repository. A distribuable .msi installer (51 MB) has been created in the dist/ folder. You can delete the build/ folder. Simply double click it and follow the instructions to install a standalone exe app. This installation step doesn't require having a Python environment on your computer as an installer is by nature already standalone.
