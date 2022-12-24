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

root_loc=path_to_cache+'/images'
V11_max=10
N=80
V11_arry=np.linspace(0,V11_max,N)
w0=9
w1=12
V_00=0
V_01=0
img_loc='/energy_spectrum_w0_'+str(w0)+'_w1_'+str(w1)+'_V11_max_'+str(V11_max)+'_V00_'+str(V_00)+'_N_'+str(N)


for i in tqdm (range (0,N), desc="Process"):
    

    J11=0
    V_11=V11_arry[i]
    H_ref=H_sys(V00=V_00,V01=V_01,V11=V_11,J01=0,J11=0,t=0,w0=w0,w=w1)
    eigen_ref_2,eigen_ref_3=H_ref.get_ref_val()
    eigen_ref_2=eigen_ref_2-np.min(eigen_ref_2)
    eigen_ref_3=eigen_ref_3-np.min(eigen_ref_3)
 
    J_01_start=0
    J_01_end=20
    gaussian_broadening=0.2
   # trial_run=5
    J_01_arry,E__2e_J01,E__3e_J01,Hist_2e_01,Hist_3e_01,Hit_arry=energy_sweep_J01(w0,w1,J_01_start,J_01_end,V_11,V_00,V_01,J11,bin_density=1000,low_energy_reso=0.2,density=1000,gaussian_broadening=gaussian_broadening)

    gaussian_broadening=0.2
    #trial_run=5
    J01=0
    J_11_start=0
    J_11_end=20
    J_11_arry,E__2e_J11,E__3e_J11,Hist_2e_11,Hist_3e_11,Hit_arry=energy_sweep_J11(w0,w1,J_11_start,J_11_end,V_11,V_00,V_01,J01,bin_density=1000,low_energy_reso=0.2,density=1000,gaussian_broadening=gaussian_broadening)






    width=20
    height=20
    data_=Data_process(row_num=2,column_num=2,root_dir=root_loc,width=width,height=height,letter=False)
    
    data_.add_axis_label(plot_index=1,x_axis_name=r'Energies',y_axis_name=r'$J_{01}$',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[0],fontsize=16,rotation_x=0,rotation_y=0)
    data_.add_title(plot_index=1,title_name='(2e) Energy Spectrum (vary J01) ',fontsize=20)
    data_.p_plot(plot_index=1,x=Hit_arry,y=J_01_arry,cl=Hist_2e_01,cbar_label='Intensity',vmin=0,vmax=3,type=0)
    for s in range(len(eigen_ref_2)):
        if eigen_ref_2[s]<=Hit_arry[-1]:
            data_.simple_plot(plot_index=1,x_arry=eigen_ref_2[s]*np.ones(len(J_01_arry)),y_arry=J_01_arry,log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=1,lw=1)
            data_.simple_plot(plot_index=2,x_arry=eigen_ref_2[s]*np.ones(len(J_11_arry)),y_arry=J_11_arry,log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=1,lw=1)
        else:
            pass
    data_.add_text(plot_index=1,x=Hit_arry[0]*3,y=0,s=r'$V_{11}$: '+str(np.round(V_11,2)),bg_color='white',fontsize=20, alpha=0.5)
  #  data_.add_text(plot_index=1,x=Hit_arry[0]*3,y=-J_01_end*3/50,s=r'$V_{01}$: '+str(np.round(V_01,2)),bg_color='white',fontsize=20, alpha=0.5)
    data_.add_text(plot_index=1,x=Hit_arry[0]*3,y=-J_01_end*3/50,s=r'$V_{00}$: '+str(np.round(V_00,2)),bg_color='white',fontsize=20, alpha=0.5)
    data_.add_text(plot_index=1,x=Hit_arry[0]*3,y=-J_01_end*6/50,s=r'$J_{11}$: '+str(np.round(J11,2)),bg_color='white',fontsize=20, alpha=0.5)
    data_.add_text(plot_index=1,x=Hit_arry[0]*3,y=-J_01_end*9/50,s=r'$\omega_0$: '+str(w0),bg_color='white',fontsize=20, alpha=0.5)
    data_.add_text(plot_index=1,x=Hit_arry[0]*3,y=-J_01_end*12/50,s=r'$\omega_1$: '+str(w1),bg_color='white',fontsize=20, alpha=0.5)



    data_.add_axis_label(plot_index=2,x_axis_name=r'Energies',y_axis_name=r'$J_{11}$',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[0],fontsize=16,rotation_x=0,rotation_y=0)
    data_.add_title(plot_index=2,title_name='(2e) Energy Spectrum (vary J11) ',fontsize=20)
    data_.p_plot(plot_index=2,x=Hit_arry,y=J_11_arry,cl=Hist_2e_11,cbar_label='Intensity',vmin=0,vmax=3,type=0)
    for s in range(len(eigen_ref_3)):
         
        if eigen_ref_3[s]<=Hit_arry[-1]:
            data_.simple_plot(plot_index=3,x_arry=eigen_ref_3[s]*np.ones(len(J_01_arry)),y_arry=J_01_arry,log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=1,lw=1)
            data_.simple_plot(plot_index=4,x_arry=eigen_ref_3[s]*np.ones(len(J_11_arry)),y_arry=J_11_arry,log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=1,lw=1)
        else:
            pass
    data_.add_axis_label(plot_index=3,x_axis_name=r'Energies',y_axis_name=r'$J_{01}$',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[0],fontsize=16,rotation_x=0,rotation_y=0)
    data_.add_title(plot_index=3,title_name='(3e) Energy Spectrum (vary J01) ',fontsize=20)
    data_.p_plot(plot_index=3,x=Hit_arry,y=J_01_arry,cl=Hist_3e_01,cbar_label='Intensity',vmin=0,vmax=3,type=0)


    """    
    data_.add_text(plot_index=2,x=-Hit_arry[-1]*1.1,y=0,s=r'$V_{11}$: '+str(np.round(V_11,2)),bg_color='white',fontsize=20, alpha=0.5)
    data_.add_text(plot_index=2,x=-Hit_arry[-1]*1.1,y=-J_11_end*3/50,s=r'$V_{01}$: '+str(np.round(V_01,2)),bg_color='white',fontsize=20, alpha=0.5)
    data_.add_text(plot_index=2,x=-Hit_arry[-1]*1.1,y=-J_11_end*6/50,s=r'$V_{00}$: '+str(np.round(V_00,2)),bg_color='white',fontsize=20, alpha=0.5)
    data_.add_text(plot_index=2,x=-Hit_arry[-1]*1.1,y=-J_11_end*9/50,s=r'$J_{01}$: '+str(np.round(J01,2)),bg_color='white',fontsize=20, alpha=0.5)
    data_.add_text(plot_index=2,x=-Hit_arry[-1]*1.1,y=-J_11_end*12/50,s=r'$\omega_1$: '+str(w1),bg_color='white',fontsize=20, alpha=0.5)

    """


    data_.add_axis_label(plot_index=4,x_axis_name=r'Energies',y_axis_name=r'$J_{11}$',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[0],fontsize=16,rotation_x=0,rotation_y=0)
    data_.add_title(plot_index=4,title_name='(3e) Energy Spectrum (vary J11) ',fontsize=20)
    data_.p_plot(plot_index=4,x=Hit_arry,y=J_11_arry,cl=Hist_3e_11,cbar_label='Intensity',vmin=0,vmax=3,type=0)

    
    data_.save_fig(img_loc,200,str(i))
    data_.close_fig()

video_series='/Energy_spectrum_J01_series_V00_'+str(V_00)+'V11_max_'+str(V11_max)

out_loc=path_to_cache+'/videos/'+video_series+'/'
width=20
height=20
data_=Data_process(row_num=2,column_num=2,root_dir=root_loc,width=width,height=height,letter=False)
data_.rebuild_dir(file_loc=out_loc)
data_.videos(img_loc=root_loc+img_loc,out_loc=out_loc,out_file_name='energy_spectrum_V11_max_'+str(V11_max)+'_w1_'+str(w1)+'_w0_'+str(V_01)+'_N_'+str(N)+'.mp4',N=N)