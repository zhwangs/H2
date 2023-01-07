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
w0=1
w1=4
V_00=0
V_01=0
V_11=0
J11=0
V_00_start=0
V_00_end=5
J_01_start=0
J_01_end=5
file_loc='/onlyx_spectrum_w0_'+str(w0)+'_w1_'+str(w1) 
try:
    os.mkdir(root_loc+file_loc)
except:
    shutil.rmtree(root_loc+file_loc)
    os.mkdir(root_loc+file_loc)
out_dir=file_loc+'_img'
try:
    os.mkdir(root_loc+out_dir)
except:
    shutil.rmtree(root_loc+out_dir)
    os.mkdir(root_loc+out_dir)
V_00_arry=np.linspace(V_00_start,V_00_end,N)
J01_arry=np.linspace(J_01_start,J_01_end,N)
 
N_sample=10
_start=0
_end=10
arry=np.linspace(_start,_end,N_sample)
for k in tqdm(range(0,N_sample), desc="Sampling"):
    V_11=arry[k]
    for i in range (0,N):
        for j in range(0,N):
            V_00=V_00_arry[i]
            J01=J01_arry[j]
            H_ref=H_sys(V00=0,V01=0,V11=0,J01=0,J11=0,t=0,w0=w0,w=w1)
            info_vector1=H_ref.get_first_two_eigen_info_onlyx(unique_=True)
        # print(np.round(info_vector1,2))
        # print('down')
            info_vector2=energy_eigen_map_onlyx(w0,w1,J01,V11=V_11,V00=V_00,V01=V_01,J11=J11)
            #print(np.round(info_vector2,2))
        #$ print(info_vector2)
            join_info=np.concatenate((info_vector2, info_vector1[6::]), axis=0)
            save(array=np.array(join_info),append_=True,data_file=root_loc+file_loc+'/'+str(k)+'.csv')

    arr = np.loadtxt(root_loc+file_loc+'/'+str(k)+'.csv',
                    delimiter=",", dtype=float)

    J01=arr[:,4]
    V00=arr[:,2]
    V_11=arry[k]
    ex_with_J_2e=arr[:,6:8]
    ex_with_J_3e=arr[:,8:10]
    ex_without_J_2e=arr[:,10:12]
    ex_without_J_3e=arr[:,12:14]

    width=20
    height=20
    data_=Data_process(row_num=2,column_num=2,root_dir=root_loc,width=width,height=height,letter=False)
    data_.fig_title(fig_name='Cyan Line: C-B=0, \n Black Line: A=0\n'+r'$\omega_0$: '+str(w0)+r', $\omega_1$: '+str(w1)+', V11 :'+str(np.round(V_11,2)),title_size=30)
    data_.add_axis_label(plot_index=1,x_axis_name=r'$J_{01}$',y_axis_name=r'$V_{00}$',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[0],fontsize=16,rotation_x=0,rotation_y=0)
    data_.add_title(plot_index=1,title_name='(2e) Exciton Binding Energy A',fontsize=20)
    data_.add_axis_label(plot_index=2,x_axis_name=r'$J_{01}$',y_axis_name=r'$V_{00}$',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[0],fontsize=16,rotation_x=0,rotation_y=0)
    data_.add_title(plot_index=2,title_name='(2e) Excition-Exciton Energy B',fontsize=20)
    data_.add_axis_label(plot_index=3,x_axis_name=r'$J_{01}$',y_axis_name=r'$V_{00}$',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[0],fontsize=16,rotation_x=0,rotation_y=0)
    data_.add_title(plot_index=3,title_name='(3e) Exciton Binding Energy C',fontsize=20)
    data_.add_axis_label(plot_index=4,x_axis_name=r'$J_{01}$',y_axis_name=r'$V_{00}$',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[0],fontsize=16,rotation_x=0,rotation_y=0)
    data_.add_title(plot_index=4,title_name=' Difference: C(3e)-B(2e)',fontsize=20)
    

    color_range=[-5,5]
    data_.simple_scatter(plot_index=1,x_arry=J01,y_arry=V00,color_t=ex_without_J_2e[:,0]-ex_with_J_2e[:,0],marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=30,cbar_label='Energy',color_range=color_range)
    data_.simple_scatter(plot_index=2,x_arry=J01,y_arry=V00,color_t=(ex_without_J_2e[:,1]-ex_without_J_2e[:,0])-(ex_with_J_2e[:,1]-ex_with_J_2e[:,0]),marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=30,cbar_label='Energy',color_range=color_range)
    data_.simple_scatter(plot_index=3,x_arry=J01,y_arry=V00,color_t=ex_without_J_3e[:,0]-ex_with_J_3e[:,0],marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=30,cbar_label='Energy',color_range=color_range)
    data_.simple_scatter(plot_index=4,x_arry=J01,y_arry=V00,color_t= (ex_without_J_3e[:,0]-ex_with_J_3e[:,0])-((ex_without_J_2e[:,1]-ex_without_J_2e[:,0])-(ex_with_J_2e[:,1]-ex_with_J_2e[:,0])),marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=30,cbar_label='Energy',color_range=color_range)

    data_.simple_scatter(plot_index=1,x_arry=J01[np.abs((ex_with_J_2e[:,0]))-0.1<0],y_arry=V00[np.abs((ex_with_J_2e[:,0]))-0.1<0],color_t='black',marker='o',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.6,add_line=False,s=30,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=2,x_arry=J01[np.abs((ex_with_J_2e[:,0]))-0.1<0],y_arry=V00[np.abs((ex_with_J_2e[:,0]))-0.1<0],color_t='black',marker='o',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.6,add_line=False,s=30,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=3,x_arry=J01[np.abs((ex_with_J_2e[:,0]))-0.1<0],y_arry=V00[np.abs((ex_with_J_2e[:,0]))-0.1<0],color_t='black',marker='o',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.6,add_line=False,s=30,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=4,x_arry=J01[np.abs((ex_with_J_2e[:,0]))-0.1<0],y_arry=V00[np.abs((ex_with_J_2e[:,0]))-0.1<0],color_t='black',marker='o',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.6,add_line=False,s=30,cbar_label='Energy',cbar_=False)

    data_.simple_scatter(plot_index=4,x_arry=J01[np.abs((ex_without_J_3e[:,0]-ex_with_J_3e[:,0])-((ex_without_J_2e[:,1]-ex_without_J_2e[:,0])-(ex_with_J_2e[:,1]-ex_with_J_2e[:,0])))-0.1<0],y_arry=V00[np.abs((ex_without_J_3e[:,0]-ex_with_J_3e[:,0])-((ex_without_J_2e[:,1]-ex_without_J_2e[:,0])-(ex_with_J_2e[:,1]-ex_with_J_2e[:,0])))-0.1<0],color_t='cyan',marker='o',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.6,add_line=False,s=30,cbar_label='Energy',cbar_=False)

    data_.save_fig(out_dir,200,str(k))
    data_.close_fig()

 