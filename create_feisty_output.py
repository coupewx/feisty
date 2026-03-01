import os
import glob as glob
import numpy as np
from pathlib import Path


def year_4digit(year):
    year = abs(int(year))
    if year > 9999:
        return 'you broke it'
    if year < 10:
        return '000'+str(year)
    elif year < 100:
        return '00'+str(year)
    elif year<1000:
        return '0'+str(year)
    else:
        return str(year)
    

desired_variables='TEMP_mean_150m,TEMP_BOTTOM_2,mesozooC_zint_150m,pocToFloor_2,mesozoo_loss_zint_150m_2'
   
#print('module load anaconda')
#print('conda activate base')
#print('module load python')
#print('module load nco')
#print('module load intel/2022.1.2')
#print('module load cdo')

#os.system('module load intel/2022.1.2')
#os.system('module load nco')
#os.system('module load cdo')



def ncrcat_files(EXECUTE_COMMANDS,MAKE_TEMP_DIRECTORY,YEAR,CASENAME,desired_variables,INITIAL_DIRECTORY,CURRENT_VARIABLE):  
    CHANGE_TIME=True
    NEW_YEAR = 2000
    DOUT_S_ROOT = INITIAL_DIRECTORY + '/proc/'
    TEMPORARY_PROCESSING_FOLDER = DOUT_S_ROOT+'/temporary/'
    TEMPORARY_PROCESSING_FOLDER_FILES = sorted(glob.glob(TEMPORARY_PROCESSING_FOLDER+'/*.nc')) 
    FIRST_DAY = TEMPORARY_PROCESSING_FOLDER_FILES[0][-13:-3].replace('-',''); #print(FIRST_DAY)
    LAST_DAY  = TEMPORARY_PROCESSING_FOLDER_FILES[-1][-13:-3].replace('-',''); #print(LAST_DAY)
    FINAL_FILE=DOUT_S_ROOT + '/tseries/feisty/' + CASENAME + '.pop.h.' +  CURRENT_VARIABLE+'.'+FIRST_DAY+'-'+LAST_DAY+'.nc'
    CMD = 'ncrcat '+TEMPORARY_PROCESSING_FOLDER+'/*.nc '+ FINAL_FILE
    print()
    print(CMD)
    CMD2= 'rm -r '+ TEMPORARY_PROCESSING_FOLDER+'/*.nc' #
    print(CMD2)
    CMD3='cdo -settaxis,2000-01-01,00:00,1day '+FINAL_FILE+' '+FINAL_FILE 
    print(CMD3)
       
    if EXECUTE_COMMANDS:
        if Path(FINAL_FILE).is_file():
            print('This file already exists! ABORT!')
            os.system(CMD2)
        else:
            os.system(CMD)
            if Path(FINAL_FILE).is_file():
                print('The file exists. We can now delete the files in /temporary')
                os.system(CMD2)
                print('Changing year axis to '+str(NEW_YEAR)+'....')
                os.system(CMD3)
            else:
                print('ERROR! Failed to create file.')
                os.system(CMD2)
    
    
    
def ncks_files(EXECUTE_COMMANDS,MAKE_TEMP_DIRECTORY,YEAR,CASENAME,desired_variables,INITIAL_DIRECTORY,MAKE_FEISTY_DIRECTORY):
    if MAKE_TEMP_DIRECTORY:
        os.system('mkdir '+INITIAL_DIRECTORY+'/proc/')
        os.system('mkdir '+INITIAL_DIRECTORY+'/proc/temporary/')
        os.system('mkdir ' +INITIAL_DIRECTORY+'/proc/tseries')
    if MAKE_FEISTY_DIRECTORY:
        os.system('mkdir ' +INITIAL_DIRECTORY+'/proc/tseries/feisty')
        #os.system('mkdir ' +INITIAL_DIRECTORY+'/proc/tseries/day_1')
    
    VARIABLES=desired_variables.split(',')
    for CURRENT_VARIABLE in VARIABLES:   
        YEAR=year_4digit(YEAR)    
        INITIAL_FILES=sorted(glob.glob(INITIAL_DIRECTORY+'/hist/'+CASENAME+'.pop.h.ecosys.nday1.'+YEAR+'*.nc')) # nw_cntrl_tuv_01.pop.h.ecosys.nday1.0005-
        DOUT_S_ROOT = INITIAL_DIRECTORY + '/proc/'#'/scratch/alpine/joco6825/cesm/nw_cases/archive/nw_cntrl_09_datm_feisty/ocn/hist/feisty/'
        TEMPORARY_PROCESSING_FOLDER = DOUT_S_ROOT+'/temporary/'

        for fi in INITIAL_FILES:
            CURRENT_DAY = fi[-13:-3]; #print(CURRENT_DAY)
            CMD= 'ncks -v '+CURRENT_VARIABLE+',HT '+fi+' '+ TEMPORARY_PROCESSING_FOLDER+CASENAME+'.pop.h.ecosys.nday1.'+CURRENT_DAY+'.nc'
            print(CMD)
            if EXECUTE_COMMANDS:
                os.system(CMD)    
        ncrcat_files(EXECUTE_COMMANDS,MAKE_TEMP_DIRECTORY,YEAR,CASENAME,desired_variables,INITIAL_DIRECTORY,CURRENT_VARIABLE)
    

  
'''
module load cdo
module load nco

python
import runpy
runpy.run_path('/projects/joco6825/nw_cases/nw_cntrl_tuv_01/create_feisty_output.py')

'''

execute_commands = True
make_temp_directory=False
make_feisty_directory=False

YEARS=['0002','0003','0004']
casename='nw_cntrl_tuv_01'
initial_directory='/scratch/alpine/joco6825/cesm/nw_cases/archive/'+casename+'/ocn/'

for year in YEARS:
    ncks_files(execute_commands,make_temp_directory,year,casename,desired_variables,initial_directory,make_feisty_directory)
    

    