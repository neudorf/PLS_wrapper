# PLS_wrapper
- Wrapper function for the behavioural PLS neuroimaging matlab function `pls_analysis.m` from [https://github.com/McIntosh-Lab/PLS](https://github.com/McIntosh-Lab/PLS)
- Important: this is only developed and tested for the behavioural PLS method (option.method = 3 in matlab function)
- Requires MATLAB installation and MATLAB Engine API for Python
- Install instructions for MATLAB Engine API for Python [here](https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html)
- Only other requirement is numpy
- Works just like the original matlab implementation, but takes numpy ndarray matrices and python types as input
- Outputs an object containing the same variables as the matlab implementation, but converted to ndarrays and python types
- Warning that this creates (and removes when finished) a matlab script called `pls_analysis_py.m` to call `pls_analysis.m` from the matlab PLS package and removes the `field_descrip` variable (character arrays are problematic, and this variable is not necessary), so make sure there isn't a script called `pls_analysis_py.m` in your working directory that you don't want deleted (not likely but worth mentioning). If you want to avoid the need for this you can copy the `pls_analysis_py.m` script from this repository to your PLS directory or a matlab path directory and set `make_script=False`.

To install:
```
git clone https://github.com/neudorf/PLS_wrapper.git
cd PLS_wrapper
python -m pip install .
```
Example usage for a single group, where X is a 2D numpy matrix with each 
row representing the neuroimaging data for each subject for each condition,
subjects_n is the number of subjects examined, 1 is the number of 
conditions, Y is the behavioural data as a 2D numpy matrix with each column
representing a behavioural variable, num_perm is the number of
permutations, and num_boot is the number of bootstrap samples:
```
from PLS_wrapper import pls
res = pls.pls_analysis(X,subjects_n,1,Y,num_perm=1000,num_boot=1000)
```
Or for multiple groups, where X1 and X2 are 2D numpy matrices representing the neuroimaging data for subjects in group 1 and 2 respectively, and group1_n and group2_n are the number of subjects in groups 1 and 2 respectively:
```
from PLS_wrapper import pls
res = pls.pls_analysis([X1,X2],[group1_n,group2_n],1,Y,num_perm=1000,num_boot=1000)
```
Docstring:
```
pls_analysis(datamat_lst,num_subj_lst,num_cond,stacked_behavdata,
    num_perm=0,
    num_split=0,
    num_boot=0,
    meancentering_type=0,
    cormode=0,
    boot_type='strat',
    clim=95.0
    )
    
Python wrapper for matlab implementation of pls_analysis.
Will use matlab python library to call the original matlab script.
Uses the `pls_analysis_py.m` function in the same folder which drops the 
unsupported character array `field_descrip`.
Warning that this creates (and removes when finished) a matlab script 
called `pls_analysis_py.m` to call `pls_analysis.m` from the matlab PLS 
package and removes the `field_descrip` variable (character arrays are 
problematic, and this variable is not necessary), so make sure there isn't 
a script called `pls_analysis_py.m` in your working directory that you 
don't want deleted (not likely but worth mentioning).

Parameters
----------
datamat_lst         :   list of 2D ndarrays, one for each group. 
                        Rows represent independent variable data. 
                        If a single 2D ndarray is given will convert to 
                        list automatically.
num_subj_lst        :   list of integers representing sizes of groups. 
                        If a single integer is given will convert to list 
                        automatically.
num_cond            :   int representing number of conditions.
stacked_behavdata   :   2D ndarray with columns representing behavioural 
                        data
num_perm            :   int, default=0. Number of permutations.
num_split           :   int, default=0. Number of split half permutations.
num_boot            :   int, default=0. Number of bootstrap permutations.
meancentering_type  :   int, default=0. Type of meancentering.
                        0. Remove group condition means from conditon means
                        within each group. Tells us how condition effects
                        are modulated by group membership. (Boost condition
                        differences, remove overall group diffrences).
                        1. Remove grand condition means from each group 
                        condition mean. Tells us how conditions are 
                        modulated by group membership (boost group 
                        differences, remove overall condition diffrences).
                        2. Remove grand mean over all subjects and 
                        conditions. Tells us full spectrum of condition and 
                        group effects.
                        3. Remove all main effects by subtracting condition
                        and group means. This type of analysis will deal
                        with pure group by condition interaction.
cormode             :   int, default=0. Correlation type to use.
                        0. Pearson correlation
                        2. covariance
                        4. cosine angle
                        6. dot product
boot_type           :   string, default = 'strat'. Use 'nonstrat' for 
                        nonstratified boot samples.
clim                :   float, default=95.0. Confidence level between 0.0 
                        and 100.0.
make_script         :   bool, default=True. Whether to make and delete the
                        pls_analysis_py.m file in the working directory.
                        If you have copied this file to the PLS directory
                        or a matlab path folder you can set this to False.

Return
------
res_py              :   Object containing same outputs as original matlab 
                        script, with same names, converted to python native
                        types.
                        Matlab single and double arrays are converted to 
                        numpy ndarrays.
                        Floats used as booleans in matlab (0.0 for False, 
                        1.0 for True) are converted to boolean.
                        Integers or floats being used as integers in matlab
                        converted to int in python.
                        Floats as python floats.
```
