# PDF Splitter

**This python application is intended to be used to correct lecture note pdf formatting for the CMU-Q "Probability Theory for Computer Science" course by Hasan Demirkoparan**

## Instructions

1. Clone the Repo
2. Install conda if it isn't already
3. Initialize a conda environment with the provided environment.yml
   `conda env create --name pdf_splitter --file=environment.yml"`
4. Run the file with `python split.py`
5. You will be prompted to select the file(s) you want to be fixed
6. You will be prompted to select the output directory of the fixed files
7. You will optionally be asked if you want to correct the final rotation of the file. If the "fixed" lecture file comes out upside down, or rotated, you can run the program again with a certain degree angle (e.g. 180) to correct its rotation.
8. The files will be outputted to the directory of selection. Enjoy! If there are any additional features or bugs that may occur, please file an Issue or reach out to me at belalm@andrew.cmu.edu
