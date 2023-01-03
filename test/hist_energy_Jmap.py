import os
import sys
  
path_this_script = os.path.realpath(sys.argv[0])
# add the ./src/ path to the search path
path_this_script_splitted = os.path.split(path_this_script)
this_script_filename = path_this_script_splitted[1]
path_this_script_splitted = os.path.split(path_this_script_splitted[0])
path_to_src = os.path.join(path_this_script_splitted[0], 'src')
print(path_to_src)
sys.path.append(path_to_src)  # I could have used sys.path.append('../src/'), but it didn't work with the debugger
path_to_cache = os.path.join(path_this_script_splitted[0], 'cache')

from sweep_energy import *
from tqdm import tqdm
from data_ex import *

root_loc=path_to_cache+'/data'
N=80
#V11_arry=np.linspace(0,V11_max,N)
w0=9
w1=12
V_00=0
V_01=0
V_11=5
J_11_start=0
J_11_end=30
J_01_start=0
J_01_end=30
file_loc='/spectrum_w0_'+str(w0)+'_w1_'+str(w1)+'_V11_'+str(V_11)+'_V00_'+str(V_00)+'_N_'+str(N)+'_J_11_end_'+str(J_11_end)+'_J_01_end_'+str(J_01_end)

J11_arry=np.linspace(J_11_start,J_11_end,N)
J01_arry=np.linspace(J_01_start,J_01_end,N)
for i in tqdm (range (0,N), desc="Process"):
    for j in range(0,N):
        J11=J11_arry[i]
        J01=J01_arry[j]
        H_ref=H_sys(V00=V_00,V01=V_01,V11=V_11,J01=0,J11=0,t=0,w0=w0,w=w1)
        info_vector1=H_ref.get_first_two_eigen_info()
        info_vector2=energy_eigen_map(w0,w1,J01,V11=V_11,V00=V_00,V01=V_01,J11=J11)
        join_info=np.concatenate((info_vector2, info_vector1[6::]), axis=0)
        save(array=np.array(join_info),append_=True,data_file=root_loc+file_loc+'.csv')

