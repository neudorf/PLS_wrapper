import matlab.engine
import numpy as np
import os

class Dict2Object:
    def __init__(self, dict=None):
        if dict is not None:
            for key, value in dict.items():
                setattr(self, key, value)

def perm_result_values_conversion(res_dict_value):
    """Decides how to convert inner values from dict valued PLS result `perm_result`
    """
    matlab_double_arrays = [
        'sp',
        'sprob',
        'persamp'
    ]
    new_dict = {}
    for key, value in res_dict_value.items():
        if key in matlab_double_arrays:
            new_value = np.array(value)
        elif key == 'num_perm':
            new_value = int(value)
        elif key == 'is_perm_splithalf':
            new_value = bool(int(value))
        new_dict[key] = new_value
    return new_dict

def boot_result_values_conversion(res_dict_value):
    """Decides how to convert inner values from dict valued PLS result `boot_result`
    """
    float_to_int = [
        'num_boot',
        'countnewtotal'
    ]
    float_to_bool = [
        'nonrotated_boot',
    ]
    matlab_double_arrays_to_float_numpy = [
        'num_LowVariability_behav_boots',
        'ulcorr',
        'llcorr',
        'ulcorr_adj',
        'llcorr_adj',
        'badbeh',
        'prop',
        'distrib',
    ]
    matlab_double_arrays_to_int_numpy = [
        'bootsamp_4beh',
        'bootsamp',
    ]
    matlab_single_arrays = [
        'orig_corr',
        'compare_u',
        'u_se',
    ]
    new_dict = {}
    for key, value in res_dict_value.items():
        if key in float_to_int:
            new_value = int(value)
        elif key in float_to_bool:
            new_value = bool(int(value))
        elif key in matlab_double_arrays_to_float_numpy or matlab_single_arrays:
            new_value = np.array(value)
        elif key in matlab_double_arrays_to_int_numpy:
            new_value = np.array(value,dtype=np.int64)
        new_dict[key] = new_value
    return new_dict

def other_input_values_conversion(res_dict_value):
    """Decides how to convert inner values from dict valued PLS result `other_input`
    """
    new_dict = {}
    for key, value in res_dict_value.items():
        if key == 'meancentering_type':
            new_value = bool(value)
        elif key == 'cormode':
            new_value = bool(int(value))
        new_dict[key] = new_value
    return new_dict

def PLS_matlab_2_python(res):
    """Take a result from pls_analysis_py.m and convert it to an object with only python native types
    """
    matlab_single_arrays = [
        'u',
        'v',
        's',
        'lvcorrs',
        'usc',
        'vsc',
        'stacked_behavdata'
    ]
    res_new = {}
    if res is not None:
        for key, value in res.items():
            if key == 'is_struct':
                new_value = bool(int(value))
            elif key == 'datamatcorrs_lst':
                new_value = np.array(value[0])
            elif key in matlab_single_arrays:
                new_value = np.array(value)
            elif key in 'perm_result':
                new_value = perm_result_values_conversion(value)
                new_value = Dict2Object(new_value)
            elif key in 'boot_result':
                new_value = boot_result_values_conversion(value)
                new_value = Dict2Object(new_value)
            elif key in 'other_input':
                new_value = other_input_values_conversion(value)
                new_value = Dict2Object(new_value)
            else:
                new_value = value
            res_new[key] = new_value
    return Dict2Object(res_new)

def pls_analysis(datamat_lst,num_subj_lst,num_cond,stacked_behavdata,
    num_perm=0,
    num_split=0,
    num_boot=0,
    meancentering_type=0,
    cormode=0,
    boot_type='strat',
    clim=95.0
    ):
    """Python wrapper for matlab implementation of pls_analysis.
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
                            condition
                            mean. Tells us how conditions are modulated by 
                            group 
                            membership (Boost group differences, remove overall
                            condition diffrences).
                            2. Remove grand mean over all subjects and 
                            conditions.
                            Tells us full spectrum of condition and group 
                            effects.
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
    clim                :   float, default=95.0. Confidence level between 0 and
                            100.

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
    """
    eng = matlab.engine.start_matlab()

    # Matlab script for calling pls_analysis.m and removing 'field_descrip'
    temp_script =    'function result = pls_analysis_py(datamat_lst, num_subj_lst, k, opt)\n' \
                '    result_tmp = pls_analysis(datamat_lst, num_subj_lst, k, opt);\n' \
                '    result = rmfield(result_tmp,"field_descrip");'

    with open('pls_analysis_py.m','w+') as f:
        f.write(temp_script)

    if type(datamat_lst) is np.ndarray:
        datamat_lst = [datamat_lst.copy()]
    
    if type(num_subj_lst) is list:
        num_subj_lst = [matlab.double(x) for x in num_subj_lst.copy()]
        num_subj_lst = [num_subj_lst]
    elif type(num_subj_lst) is int:
        num_subj_lst = [matlab.double(num_subj_lst)]

    stacked_behavdata = matlab.double(stacked_behavdata.copy())

    num_cond = matlab.double(num_cond)

    option = {}
    option['method'] = 3
    option['num_perm'] = matlab.double(num_perm)
    option['num_split'] = matlab.double(num_split)
    option['num_boot'] = matlab.double(num_boot)
    option['stacked_behavdata'] = stacked_behavdata
    option['meancentering_type'] = meancentering_type
    option['cormode'] = cormode
    option['boot_type'] = boot_type
    option['clim'] = matlab.double(clim)

    res = eng.pls_analysis_py(datamat_lst,num_subj_lst,num_cond,option)
    res_py = PLS_matlab_2_python(res)

    os.remove('pls_analysis_py.m')

    return res_py
