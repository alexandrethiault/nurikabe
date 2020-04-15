# nurikabe
A simple pygame implementation for the Nurikabe grid game with a setup.py file to build a msi standalone app installer.
As a first upload to github, it only supports Windows 10 for now.
It is given as a modifiable python script Nurikabe.py as well as an executable that can be installed with Nurikabe-0.0.0-amd64.msi.

## Install python script

You will need python >=3.7 installed on your computer (see https://www.anaconda.com/distribution/ for a Python distribution, or https://pyzo.org/start.html if you also want an integrated development environment)

Clone the repository to download it. You'll only need the Nurikabe.py and grille_vide.py scripts and the Grille/ and Icones/ folders.

If not already done, install the pygame module. This can be done with the ´pip install pygame´ command.

## Execute python script

To execute the python script, you can either use the ´python Nurikabe.py´ command in the directory where you placed the repository, or directly execute the Nurikabe.py file opened in an IDE.

## Build installer from python scripts

Delete or rename dist/ as the installer will be built here.

Install the cx_Freeze with ´pip install cx_Freeze´ and execute the ´python setup.py bdist_msi´ command in the directory where you placed the repository. A distribuable .msi installer has been created in the dist/folder. You can delete the build/ folder.

## Build executable from .msi installer

An installer is in the dist/ folder (if deleted, see previous section). Simply double click it and follow the instructions.
