###################################################################################################
# coding: utf-8
###################################################################################################
"""
# This script is written in python 2.7.
#
# It relies on externally linked libraries that are freely available and easy to install for Linux
# systems, but a bitch to get working on windows.
#
# The necessary prerequisits to use this program are:
# 1) FigureGenerator49.f90 - the uncompiled fortran code is available at www.caseydietrich.com
# 2) a fortran compiler - (gfortran works well) to compile the previous script into a binary
#                         executable
# 3) GMT 4.5.x - This is available in repositories of most debian based Linux OSs and is easily
#                installed using apt-get.
#                Note: GMT 4.5.x is no longer available in the Ubuntu repositories and needs to be
#                      downloaded and installed following instructions on the developer's site.
# 4) ghostscript - also available from repositories using apt-get
# 5) imagemagick - also available from repositories using apt-get
#
# Once you have a system up and running with these prerequisits you should get example input files
# for FigureGenerator from Casey Dietrich's website and edit them to fit your needs.
#
# !HINT! Keep your temporary folder path as short as possible to avoid getting overflow errors from
#        Fortran.
#
# Test case 1: 2 storm folders in 7 minutes.
# Test case 2: 25 storm folder in 1 hour and 46 minutes.
#
# Created by: Jared Dorvinen on November 23rd 2015
# contact at: jdorvinen@dewberry.com
"""
###################################################################################################
# Import modules
###################################################################################################
import os
from os.path import join
import subprocess
import shutil
from time import sleep
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
plt.style.use(['ggplot', 'bmh'])

###################################################################################################
# Set variables
###################################################################################################
PARENT_DIRECTORY = "/media/sf_P_DRIVE/04/QC/Tropical_Released09152016"
FIGGEN = "FigureGen49.sh"
SUB_DIRECTS = ["T1",
               "T2",
               "T3",
               "T4",
               "T5",
               "T6",
               "T7",
               "T8",
               "T9"
              ]
INPUT_FILES = ["maxele_overview.inp",
               "maxvel_overview.inp",
               "maxwvel_overview.inp",
               "minpr_overview.inp",
               "maxrs_overview.inp",
               "HSatmaxele_overview.inp",
               "TPSatmaxele_overview.inp",
               "DIRatmaxele_overview.inp",
               "DSPRatmaxele_overview.inp",
              ]
OTHER_FILES = ["RAMPP_Logo.eps",
               "Default2.pal",
               "labels_WFL.txt",
               FIGGEN
              ]
STORM_LIST = ["OS1_Exit_0010_005", "OS1_Exit_0010_006", "OS1_Exit_0010_007", "OS1_Exit_0010_008", "OS1_Exit_0010_009", "OS1_Exit_0010_010", "OS1_Exit_0010_011", "OS1_Exit_0010_012", "OS1_Exit_0010_013", "OS1_Exit_0010_014", "OS1_Inland_0010_005", "OS1_Inland_0010_006", "OS1_Inland_0010_007", "OS1_Inland_0010_008", "OS1_HC_LF_A_0002_003", "OS1_HC_LF_A_0002_004", "OS1_HC_LF_A_0002_005", "OS1_HC_LF_A_0002_006", "OS1_HC_LF_B_0002_005", "OS1_HC_LF_B_0002_006", "OS1_HC_LF_B_0002_007", "OS1_HC_LF_C_0002_005", "OS1_HC_LF_C_0002_006", "OS1_HC_LF_C_0002_007", "OS1_HC_LF_C_0002_008", "OS1_HC_LF_D_0002_005", "OS1_HC_LF_D_0002_006", "OS1_HC_LF_D_0002_007", "OS1_HC_LF_A_0008_003", "OS1_HC_LF_A_0008_004", "OS1_HC_LF_A_0008_005", "OS1_HC_LF_A_0008_006", "OS1_HC_LF_B_0008_005", "OS1_HC_LF_B_0008_006", "OS1_HC_LF_B_0008_007", "OS1_HC_LF_B_0008_008", "OS1_HC_LF_C_0008_005", "OS1_HC_LF_C_0008_006", "OS1_HC_LF_C_0008_007", "OS1_HC_LF_C_0008_008", "OS1_HC_LF_C_0008_009", "OS1_HC_LF_C_0008_010", "OS1_HC_LF_C_0008_011", "OS1_HC_LF_D_0008_005", "OS1_HC_LF_D_0008_006", "OS1_HC_LF_D_0008_007", "OS1_HC_LF_D_0008_008", "OS1_HC_LF_D_0008_009", "OS1_HC_LF_D_0008_010", "OS1_HC_LF_D_0008_011", "OS1_HC_LF_D_0008_012", "OS1_HC_LF_D_0008_013", "OS1_HC_LF_D_0008_014", "OS1_HC_LF_D_0008_015", "OS1_HC_LF_D_0008_016", "OS1_HC_LF_D_0008_017", "OS1_HC_LF_D_0008_018", "OS1_HC_LF_D_0008_019", "OS1_HC_LF_D_0008_020", "OS1_HC_LF_D_0008_021", "OS1_HC_LF_D_0008_022", "OS1_HC_LF_D_0008_023", "OS1_HC_LF_A_0013_004", "OS1_HC_LF_A_0013_005", "OS1_HC_LF_B_0013_005", "OS1_HC_LF_B_0013_006", "OS1_HC_LF_C_0013_005", "OS1_HC_LF_C_0013_006", "OS1_HC_LF_C_0013_007", "OS1_HC_LF_D_0013_005", "OS1_HC_LF_D_0013_006", "OS1_HC_LF_D_0013_007", "OS1_HC_LF_D_0013_008", "OS1_HC_LF_D_0013_009", "OS1_HC_LF_D_0013_010", "OS1_HC_LF_D_0013_011", "OS1_HC_LF_D_0013_012", "OS1_HC_LF_A_0009_005", "OS1_HC_LF_B_0009_005", "OS1_HC_LF_C_0009_005", "OS1_HC_LF_C_0009_006", "OS1_HC_LF_C_0009_006a", "OS1_HC_LF_D_0009_005", "OS1_HC_LF_D_0009_005a", "OS1_HC_LF_D_0009_006", "OS1_HC_LF_D_0009_006a", "OS1_HC_LF_D_0009_007", "OS1_HC_LF_D_0009_007a", "OS1_HC_LF_D_0009_008", "OS1_HC_LF_D_0009_009", "OS1_Exit_0008_005", "OS1_Exit_0008_006", "OS1_Exit_0008_007", "OS1_Inland_0008_005", "OS1_Inland_0008_006"]
PROCESSES = []

#List of Stations
#WFL
STATIONS = ['Cedar Key',
            'Clearwater Beach',
            'St. Petersburg',
            'Old Port Tampa',
            'McKay Bay Entrance',
            'Port Manatee',
            'Naples']

'''#SWFL
STATIONS = ['NOAA - St. Petersburg',
            'NOAA - Port Manatee',
            "USGS 02299735 - Venice Inlet at Crow's Nest Marina",
            'USGS 02293332 - Charlotte Harbor at Port Boca Grande',
            'USGS 02299230 - Myakka River at North Port Charlotte',
            'USGS 02297460 - Peace River at Harbour Heights',
            'NOAA - Fort Myers',
            'USF - Matanzas Pass',
            'USF - Big Carlos Pass',
            'USF - Spring Creek',
            'NOAA - Naples',
            'USGS 02290928 - Barron River at Everglades City'
           ]
    '''
###################################################################################################
# Define sub-functions
###################################################################################################
def delete_files(storm_directory, storm):
    """ Clean up temporary files left by make_figures() and move figure to QC folder """
    # Check if the main QC folder exists, if not create it
    qc_main = PARENT_DIRECTORY+"QC"
    if os.path.exists(qc_main) is False:
        os.mkdir(qc_main)

    # Check if the QC folder for this storm exists, if not create it
    qcfolder = join(qc_main, storm+"_QC")
    if os.path.exists(qcfolder) is False:
        os.mkdir(qcfolder)

    # Walk through files in storm directory
    for root, directories, files in os.walk(storm_directory):

        # Delete temporary directories
        for directory in directories:
            if directory in SUB_DIRECTS:
                shutil.rmtree(join(root, directory))

        # Check all files
        for filed in files:

            # Delete intermediate files created by Figure Generator
            if filed.split(".")[-1] in ["ps", "eps", "gmtdefaults4"]:
                os.remove(join(root, filed))

            # Delete all input files used by Figure Generator
            elif filed in OTHER_FILES or filed in INPUT_FILES:
                os.remove(join(root, filed))

            # Move finished plots and figures to the storm's QC folder
            elif filed.split(".")[-1] in ["jpg", "pdf"]:
                shutil.move(filed, qcfolder)

            # Ignore data files
            else:
                pass

def import_hydrograph(input_directory, input_file):
    """Import data from fort.61 files"""
    #Import data
    with open(join(input_directory, input_file), 'r') as inputfile:
        inputfile.readline() #waste the top line

        parameters_in = inputfile.readline()
        parameters = " ".join(parameters_in.split()).split(' ', 5)

        ntrspe = int(parameters[0])
        nstae = int(parameters[1])
        #dt_times_nspoolge = parameters[2]
        #nspoolge = parameters[3]
        #irtype = parameters[4]

        index = np.arange(ntrspe)
        columns = ['TIME', 'IT']
        numbers = map(str, list(range(1, nstae+1)))
        columns.extend(numbers)

        dataframe = pd.DataFrame(index=index, columns=columns)

        for i in range(ntrspe):
            data = list(map(float, " ".join(inputfile.readline().split()).split(' ', 1)))
            dataframe['TIME'][i] = data[0]/(24*3600)
            dataframe['IT'][i] = data[1]
            for j in range(nstae):
                data2 = list(map(float, " ".join(inputfile.readline().split()).split(' ', 1)))
                if data2[1] == -99999:
                    dataframe[str(j+1)][i] = np.nan
                else:
                    dataframe[str(j+1)][i] = data2[1]
    return dataframe, nstae

def plot_hydrograph(input_directory, dataframe, nstae):
    '''Plot Hydrographs using fort.61 data'''
    # Initialize figure and subplots
    fig, axs = plt.subplots(nstae, 1, figsize=(12, nstae*3))

    # Set figure title
    fig.suptitle(input_directory.rsplit('/')[-1], fontsize=18)

    # Set up subplot axes labels and ticks
    for i in range(nstae):
        axs[i].grid(True)
        axs[i].set_title(STATIONS[i])
        axs[i].plot(dataframe['TIME'].tolist(),
                    dataframe[str(i+1)].tolist())
        axs[i].set_ylabel("Elevation (m)")
        axs[i].set_xlabel("Time (days)")
        axs[i].tick_params(axis='both', labelsize=12)
    for i in range(nstae-1):
        axs[i].set_xlabel("")
        axs[i].tick_params(labelbottom='off')

    # Save figures as jpeg and pdf
    fig.savefig(join(input_directory, "hydrographs.jpg"), dpi=200)
    fig.savefig(join(input_directory, "hydrographs.pdf"), dpi=100)
    plt.close('all')

def make_figures(root):
    """ Plot figures using data from ADCIRC .63 and .61 files """
    # Plot hydrographs using fort.61 file
    if os.path.exists(join(root, "fort.61")):
        print("Plotting hydrograph "+join(root, "fort.61"))
        dataframe, nstae = import_hydrograph(root, "fort.61")
        plot_hydrograph(root, dataframe, nstae)

    # Check for dispersion file
    if os.path.exists(join(root, "DSPRatmaxele.63")) is False:
        sub_directs = SUB_DIRECTS[:-1]
        input_files = INPUT_FILES[:-1]
    else:
        sub_directs = SUB_DIRECTS[:]
        input_files = INPUT_FILES[:]

    # Copy other files to storm directory
    for other_file in OTHER_FILES:
        if os.path.exists(join(root, other_file)) is False:
            shutil.copy(join(PARENT_DIRECTORY, other_file),
                        join(root, other_file))

    # Create temporary folders in storm directory
    for directory in sub_directs:
        if os.path.exists(join(root, directory)) is False:
            os.mkdir(join(root, directory))

    # Copy input files to storm directory
    for input_file in input_files:
        if os.path.exists(join(root, input_file)) is False:
            shutil.copy(join(PARENT_DIRECTORY, input_file),
                        join(root, input_file))

        # Run Figure Generator on '.63' files
        process = subprocess.Popen([join(root, FIGGEN), "-I ", input_file])
        PROCESSES.append(process)

###################################################################################################
# Main
###################################################################################################
def main():
    """ main function """

    # Walk through storms
    for storm in STORM_LIST:
        root = join(PARENT_DIRECTORY, storm)
        os.chdir(root)
        print(root)

        # Make figures
        make_figures(root)

        # Wait for processes to finish
        while len(PROCESSES) > 0:
            sleep(15)
            for process_number in reversed(range(len(PROCESSES))):
                if PROCESSES[process_number].poll() is not None:
                    del PROCESSES[process_number]

        # Clean up
        sleep(5)
        delete_files(root, storm)

if __name__ == "__main__":
    main()
