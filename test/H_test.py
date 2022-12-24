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


from data_ex import *
from sweep_energy import *
V11=0

V00=0
V01=0

J01=28
J11=0

t=0
w1=12
w0=6
H=H_sys(V00,V01,V11,J01,J11,t,w0,w1)
smooth_2e_val,smooth_3e_val=H.energy_level(low_energy_reso=0.1)
H.print_info_2e(print_=True,print_vector=True,print_coeff=False,bare_vec=True)
H.print_info_3e(print_=True,print_vector=True,print_coeff=False,bare_vec=True)
info_vector1=H.get_first_two_eigen_info()
join_info=np.concatenate((info_vector1, info_vector1[6::]), axis=0)
print(info_vector1)
save(array=np.array(join_info),append_=True,data_file='text.csv')
#print(H.normalize((Eig_1+Eig_2)))
 
# In[ ]:





# In[390]:


# In[ ]:





# In[ ]:





# In[ ]:




