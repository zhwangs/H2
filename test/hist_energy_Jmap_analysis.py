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
arr = np.loadtxt(root_loc+file_loc+'.csv',
                 delimiter=",", dtype=float)

J01=arr[:,4]
J11=arr[:,5]
ex_with_J_2e=arr[:,6:8]
ex_with_J_3e=arr[:,8:10]
ex_without_J_2e=arr[:,10:12]
ex_without_J_3e=arr[:,12:14]

print(ex_with_J_2e)
print(ex_with_J_3e)
width=20
height=20
data_=Data_process(row_num=2,column_num=2,root_dir=root_loc,width=width,height=height,letter=False)
data_.fig_title(fig_name=r'$\omega_0$: '+str(w0)+r', $\omega_1$: '+str(w1)+', V11 :'+str(V_11)+', V00: '+str(V_00),title_size=30)
data_.add_axis_label(plot_index=1,x_axis_name=r'$J_{01}$',y_axis_name=r'$J_{11}$',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[0],fontsize=16,rotation_x=0,rotation_y=0)
data_.add_title(plot_index=1,title_name='(2e) First Excited State Energy ',fontsize=20)
data_.add_axis_label(plot_index=2,x_axis_name=r'$J_{01}$',y_axis_name=r'$J_{11}$',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[0],fontsize=16,rotation_x=0,rotation_y=0)
data_.add_title(plot_index=2,title_name='(2e) (Second-First) Excited State Energy ',fontsize=20)
data_.add_axis_label(plot_index=3,x_axis_name=r'$J_{01}$',y_axis_name=r'$J_{11}$',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[0],fontsize=16,rotation_x=0,rotation_y=0)
data_.add_title(plot_index=3,title_name='(3e) First Excited State Energy  ',fontsize=20)
data_.add_axis_label(plot_index=4,x_axis_name=r'$J_{01}$',y_axis_name=r'$J_{11}$',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[0],fontsize=16,rotation_x=0,rotation_y=0)
data_.add_title(plot_index=4,title_name='(3e) (Second-First) Excited State Energy ',fontsize=20)
 


data_.simple_scatter(plot_index=1,x_arry=J01,y_arry=J11,color_t=-ex_with_J_2e[:,0]+ex_without_J_2e[:,0],marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=30,cbar_label='Energy')
data_.simple_scatter(plot_index=2,x_arry=J01,y_arry=J11,color_t=(ex_without_J_2e[:,1]-ex_without_J_2e[:,0])-(ex_with_J_2e[:,1]-ex_with_J_2e[:,0]),marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=30,cbar_label='Energy')
data_.simple_scatter(plot_index=3,x_arry=J01,y_arry=J11,color_t=-ex_with_J_3e[:,0]+ex_without_J_3e[:,0],marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=30,cbar_label='Energy')
data_.simple_scatter(plot_index=4,x_arry=J01,y_arry=J11,color_t=(ex_without_J_3e[:,1]-ex_without_J_3e[:,0])-(ex_with_J_3e[:,1]-ex_with_J_3e[:,0]),marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=30,cbar_label='Energy')

data_.save_fig('/images',200,file_loc)
data_.close_fig()