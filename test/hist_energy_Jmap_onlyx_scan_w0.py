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
V_11=1
J11=0
V_00_start=0
V_00_end=15
J_01_start=0
J_01_end=15
file_loc='/onlyx_spectrum_V11_'+str(V_11)+'_w1_'+str(w1) 
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
 
N_sample=60
_start=0
_end=10
arry=np.linspace(_start,_end,N_sample)

entangle_sample_V00_index=15
entangle_sample_J01_index=15






for k in tqdm(range(0,N_sample), desc="Sampling"):
    w0=np.round(arry[k],2)
    sample_V00_arry=[]
    sample_J01_arry=[]
    entangle_sample_V00_arry_2e=[]
    entangle_sample_J01_arry_2e=[]

    entangle_sample_V00_arry_3e=[]
    entangle_sample_J01_arry_3e=[]
    for i in range (0,N):

        for j in range(0,N):

            V_00=V_00_arry[i]
            J01=J01_arry[j]
            H_ref=H_sys(V00=0,V01=0,V11=0,J01=0,J11=0,t=0,w0=w0,w=w1)
            info_vector1=H_ref.get_first_two_eigen_info_onlyx(unique_=True)
            Eign_2e_ref,Eign_3e_ref=H_ref.eigen_vec_all()
            
            #print(np.round(info_vector1,2))
        # print('down')
            info_vector2=energy_eigen_map_onlyx(w0,w1,J01,V11=V_11,V00=V_00,V01=V_01,J11=J11)
            #print(np.round(info_vector2,2))
            #print(info_vector2)
            join_info=np.concatenate((info_vector2, info_vector1[6::]), axis=0)
            save(array=np.array(join_info),append_=True,data_file=root_loc+file_loc+'/'+str(k)+'.csv')
            if i==entangle_sample_V00_index:
                sample_J01_arry.append(J01)
                Eign_2e,Eign_3e=energy_eigen_entangle_onlyx(w0,w1,J01,V11=V_11,V00=V_00,V01=V_01,J11=J11)
                # print(J01)
                # print(V_00)
                # print(Eign_2e)
                entangle_sample_J01_arry_2e.append(Eign_2e)
              #  entangle_sample_J01_arry_2e=np.concatenate((entangle_sample_J01_arry_2e, Eign_2e), axis=0)
                entangle_sample_J01_arry_3e.append(Eign_3e)

            if j==entangle_sample_J01_index:
                sample_V00_arry.append(V_00)
                Eign_2e,Eign_3e=energy_eigen_entangle_onlyx(w0,w1,J01,V11=V_11,V00=V_00,V01=V_01,J11=J11)
                entangle_sample_V00_arry_2e.append(Eign_2e)
                entangle_sample_V00_arry_3e.append(Eign_3e)
    
    entangle_sample_V00_arry_2e=np.array(entangle_sample_V00_arry_2e)
    entangle_sample_J01_arry_2e=np.array(entangle_sample_J01_arry_2e)

    entangle_sample_V00_arry_3e=np.array(entangle_sample_V00_arry_3e)
    entangle_sample_J01_arry_3e=np.array(entangle_sample_J01_arry_3e)


    arr = np.loadtxt(root_loc+file_loc+'/'+str(k)+'.csv',
                    delimiter=",", dtype=float)

    J01=arr[:,4]
    V00=arr[:,2]
    #V_11=arry[k]
    ex_with_J_2e=arr[:,6:8]
    ex_with_J_3e=arr[:,8:10]
    ex_without_J_2e=arr[:,10:12]
    ex_without_J_3e=arr[:,12:14]
    A=ex_without_J_2e[:,0]-ex_with_J_2e[:,0]
    B=(ex_without_J_2e[:,1]-ex_without_J_2e[:,0])-(ex_with_J_2e[:,1]-ex_with_J_2e[:,0])
    C=ex_without_J_3e[:,0]-ex_with_J_3e[:,0]
    D=C-B

    J01_grid= np.linspace(np.min(J01),np.max(J01),500)
    V00_grid= np.linspace(np.min(V00),np.max(V00),500)
    A_grid= griddata((J01, V00), A, (J01_grid[None,:], V00_grid[:,None]), method='cubic')
    B_grid= griddata((J01, V00), B, (J01_grid[None,:], V00_grid[:,None]), method='cubic')
    C_grid= griddata((J01, V00), C, (J01_grid[None,:], V00_grid[:,None]), method='cubic')
    D_grid= griddata((J01, V00), D, (J01_grid[None,:], V00_grid[:,None]), method='cubic')
    
    


    #k_min=ex_with_J_2e[:,0][ex_with_J_2e[:,0]<0.01]
    numb_=(ex_with_J_2e[:,0]<0.1).nonzero()[0][0]
    zero_val=ex_without_J_2e[:,0][numb_]-0.1


    width=33
    height=20
    data_=Data_process(row_num=2,column_num=3,root_dir=root_loc,width=width,height=height,letter=False)
    data_.fig_title(fig_name='Green Line: C-B=0, \n Black Line: A=0\n'+r'$\omega_0$: '+str(w0)+r', $\omega_1$: '+str(w1)+', V11 :'+str(np.round(V_11,2)),title_size=30)
    data_.add_axis_label(plot_index=1,x_axis_name=r'$J_{01}$',y_axis_name=r'$V_{00}$',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[0],fontsize=16,rotation_x=0,rotation_y=0)
    data_.add_title(plot_index=1,title_name='(2e) Exciton Binding Energy A',fontsize=20)
    data_.add_axis_label(plot_index=3,x_axis_name=r'$J_{01}$',y_axis_name=r'$V_{00}$',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[0],fontsize=16,rotation_x=0,rotation_y=0)
    data_.add_title(plot_index=3,title_name='(2e) Excition-Exciton Energy B',fontsize=20)
    data_.add_axis_label(plot_index=4,x_axis_name=r'$J_{01}$',y_axis_name=r'$V_{00}$',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[0],fontsize=16,rotation_x=0,rotation_y=0)
    data_.add_title(plot_index=4,title_name='(3e) Exciton Binding Energy C',fontsize=20)
    data_.add_axis_label(plot_index=6,x_axis_name=r'$J_{01}$',y_axis_name=r'$V_{00}$',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[0],fontsize=16,rotation_x=0,rotation_y=0)
    data_.add_title(plot_index=6,title_name=' Difference: C(3e)-B(2e)',fontsize=20)
    

    color_range=[-5,5]
  #  data_.simple_scatter(plot_index=1,x_arry=J01_grid,y_arry=V00_grid,color_t=A_grid,marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=30,cbar_label='Energy',color_range=color_range)
    data_.simple_contour(plot_index=1,x_arry=J01_grid,y_arry=V00_grid,z_arry=A_grid,color_t='black',log_scale_x=False,log_scale_y=False,label_name=' ',alpha=0.3,lw=8,num_of_levels=[zero_val])
    data_.simple_contour(plot_index=3,x_arry=J01_grid,y_arry=V00_grid,z_arry=A_grid,color_t='black',log_scale_x=False,log_scale_y=False,label_name=' ',alpha=0.3,lw=8,num_of_levels=[zero_val])
    data_.simple_contour(plot_index=4,x_arry=J01_grid,y_arry=V00_grid,z_arry=A_grid,color_t='black',log_scale_x=False,log_scale_y=False,label_name=' ',alpha=0.3,lw=8,num_of_levels=[zero_val])
    data_.simple_contour(plot_index=6,x_arry=J01_grid,y_arry=V00_grid,z_arry=A_grid,color_t='black',log_scale_x=False,log_scale_y=False,label_name=' ',alpha=0.3,lw=8,num_of_levels=[zero_val])

    data_.simple_contour_color(plot_index=1,x_arry=J01_grid,y_arry=V00_grid,z_arry=A_grid,log_scale_x=False,log_scale_y=False,alpha=1,cbar_=True,cmap='RdBu',cbar_label='')
    data_.simple_contour_color(plot_index=3,x_arry=J01_grid,y_arry=V00_grid,z_arry=B_grid,log_scale_x=False,log_scale_y=False,alpha=1,cbar_=True,cmap='RdBu',cbar_label='')
    data_.simple_contour_color(plot_index=4,x_arry=J01_grid,y_arry=V00_grid,z_arry=C_grid,log_scale_x=False,log_scale_y=False,alpha=1,cbar_=True,cmap='RdBu',cbar_label='')
    data_.simple_contour_color(plot_index=6,x_arry=J01_grid,y_arry=V00_grid,z_arry=D_grid,log_scale_x=False,log_scale_y=False,alpha=1,cbar_=True,cmap='RdBu',cbar_label='',color_range=[-5,5])

    #data_.simple_scatter(plot_index=1,x_arry=J01,y_arry=V00,color_t=A,marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=30,cbar_label='Energy',color_range=color_range)
    #data_.simple_scatter(plot_index=2,x_arry=J01,y_arry=V00,color_t=B,marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=30,cbar_label='Energy',color_range=color_range)
    #data_.simple_scatter(plot_index=3,x_arry=J01,y_arry=V00,color_t=C,marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=30,cbar_label='Energy',color_range=color_range)
    #data_.simple_scatter(plot_index=4,x_arry=J01,y_arry=V00,color_t=D,marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=30,cbar_label='Energy',color_range=color_range)

    
    x=J01[np.abs((ex_with_J_2e[:,0]))-0.1<0]
    y=V00[np.abs((ex_with_J_2e[:,0]))-0.1<0]
    param = np.linspace(0, 1, x.size)
    spl = make_interp_spline(param, np.c_[x,y], k=3) #(1)
    xnew, y_smooth = spl(np.linspace(0, 1, x.size * 20)).T #(2)

#    data_.simple_plot(plot_index=1,x_arry=xnew,y_arry=y_smooth,color_t='black',log_scale_x=False,log_scale_y=False,label_name=' ',alpha=0.8,lw=2)
#    data_.simple_plot(plot_index=2,x_arry=xnew,y_arry=y_smooth,color_t='black',log_scale_x=False,log_scale_y=False,label_name=' ',alpha=0.8,lw=2)
#    data_.simple_plot(plot_index=3,x_arry=xnew,y_arry=y_smooth,color_t='black',log_scale_x=False,log_scale_y=False,label_name=' ',alpha=0.8,lw=2)
#    data_.simple_plot(plot_index=4,x_arry=xnew,y_arry=y_smooth,color_t='black',log_scale_x=False,log_scale_y=False,label_name=' ',alpha=0.8,lw=2)

   # data_.simple_scatter(plot_index=1,x_arry=J01[np.abs((ex_with_J_2e[:,0]))-0.1<0],y_arry=V00[np.abs((ex_with_J_2e[:,0]))-0.1<0],color_t='black',marker='o',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.6,add_line=False,s=30,cbar_label='Energy',cbar_=False)
    # data_.simple_scatter(plot_index=2,x_arry=J01[np.abs((ex_with_J_2e[:,0]))-0.1<0],y_arry=V00[np.abs((ex_with_J_2e[:,0]))-0.1<0],color_t='black',marker='o',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.6,add_line=False,s=30,cbar_label='Energy',cbar_=False)
    # data_.simple_scatter(plot_index=3,x_arry=J01[np.abs((ex_with_J_2e[:,0]))-0.1<0],y_arry=V00[np.abs((ex_with_J_2e[:,0]))-0.1<0],color_t='black',marker='o',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.6,add_line=False,s=30,cbar_label='Energy',cbar_=False)
    # data_.simple_scatter(plot_index=4,x_arry=J01[np.abs((ex_with_J_2e[:,0]))-0.1<0],y_arry=V00[np.abs((ex_with_J_2e[:,0]))-0.1<0],color_t='black',marker='o',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.6,add_line=False,s=30,cbar_label='Energy',cbar_=False)

    x=J01[np.abs((ex_without_J_3e[:,0]-ex_with_J_3e[:,0])-((ex_without_J_2e[:,1]-ex_without_J_2e[:,0])-(ex_with_J_2e[:,1]-ex_with_J_2e[:,0])))-0.1<0]
    y=V00[np.abs((ex_without_J_3e[:,0]-ex_with_J_3e[:,0])-((ex_without_J_2e[:,1]-ex_without_J_2e[:,0])-(ex_with_J_2e[:,1]-ex_with_J_2e[:,0])))-0.1<0]
    
    #data_.simple_plot(plot_index=4,x_arry=xnew,y_arry=y_smooth,color_t='cyan',log_scale_x=False,log_scale_y=False,label_name=' ',alpha=0.8,lw=2)


    data_.simple_scatter(plot_index=6,x_arry=x,y_arry=y,color_t='seagreen',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.5,add_line=False,s=30,cbar_label='Energy',cbar_=False)

    # setup subplots 
    sub_axis_arry,sub_axis_arry_index=data_.add_subplot_sub_non_uniform_grid_row(plot_index=2,size_x_array=[4,1,4,1,4,1,4],y_ratio_array=[0,0.2,0.05,0.2,0.05,0.2,0.05,0.2])
#    data_.axis_off(plot_index=5)
#    data_.axis_off(plot_index=sub_axis_arry_index[4])
#    data_.axis_off(plot_index=sub_axis_arry_index[9])
#    data_.axis_off(plot_index=sub_axis_arry_index[14])
#    data_.remove_y_ticks(plot_index=sub_axis_arry_index[1])
#    data_.remove_y_ticks(plot_index=sub_axis_arry_index[4])
#    data_.remove_y_ticks(plot_index=sub_axis_arry_index[7])
#    data_.remove_y_ticks(plot_index=sub_axis_arry_index[10])


#    data_.simple_scatter(plot_index=6,x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,0].real**2,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.5,add_line=False,s=10,cbar_label='Energy',cbar_=False)
#    data_.simple_scatter(plot_index=sub_axis_arry_index[1],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,0].imag**2,color_t='red',marker='s',log_scale_x=False,log_scale_y=False ,label_name=' ',twinx=False,alpha=1,add_line=False,s=10,cbar_label='Energy',cbar_=False)

#    data_.simple_scatter(plot_index=6,x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,1].real**2,color_t='blue',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.5,add_line=False,s=10,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[0],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,0].real**2,color_t='orange',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.2,add_line=False,s=60,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[0],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,3].real**2,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=1,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[0],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,1].real**2,color_t='blue',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.5,add_line=False,s=10,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[0],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,2].real**2,color_t='cyan',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.1,add_line=False,s=60,cbar_label='Energy',cbar_=False)
    data_.add_x_ticks(plot_index=sub_axis_arry_index[0],x_ticks_range=sample_J01_arry,density=20)

    data_.simple_scatter(plot_index=sub_axis_arry_index[1],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,0].imag**2,color_t='orange',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.2,add_line=False,s=60,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[1],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,3].imag**2,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=1,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[1],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,1].imag**2,color_t='blue',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.5,add_line=False,s=10,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[1],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,2].imag**2,color_t='cyan',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.2,add_line=False,s=60,cbar_label='Energy',cbar_=False)

    data_.add_x_ticks(plot_index=sub_axis_arry_index[1],x_ticks_range=sample_J01_arry,density=20)

    data_.simple_scatter(plot_index=sub_axis_arry_index[5],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,4].real**2,color_t='orange',marker='s',log_scale_x=False,log_scale_y=False,label_name=r'$0\uparrow$,$0\downarrow$',twinx=False,alpha=0.2,add_line=False,s=60,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[5],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,7].real**2,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=r'$x\uparrow$,$x\downarrow$',twinx=False,alpha=1,add_line=False,s=1,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[5],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,5].real**2,color_t='blue',marker='s',log_scale_x=False,log_scale_y=False,label_name=r'$x\uparrow$,$0\downarrow$',twinx=False,alpha=0.5,add_line=False,s=10,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[5],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,6].real**2,color_t='cyan',marker='s',log_scale_x=False,log_scale_y=False,label_name=r'$0\uparrow$,$x\downarrow$',twinx=False,alpha=0.1,add_line=False,s=60,cbar_label='Energy',cbar_=False)

    data_.add_x_ticks(plot_index=sub_axis_arry_index[5],x_ticks_range=sample_J01_arry,density=20)

    data_.simple_scatter(plot_index=sub_axis_arry_index[6],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,4].imag**2,color_t='orange',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.2,add_line=False,s=60,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[6],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,7].imag**2,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=1,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[6],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,5].imag**2,color_t='blue',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.5,add_line=False,s=10,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[6],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,6].imag**2,color_t='cyan',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.1,add_line=False,s=60,cbar_label='Energy',cbar_=False)

    data_.add_x_ticks(plot_index=sub_axis_arry_index[6],x_ticks_range=sample_J01_arry,density=20)

    data_.simple_scatter(plot_index=sub_axis_arry_index[10],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,8].real**2,color_t='orange',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.2,add_line=False,s=60,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[10],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,11].real**2,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=1,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[10],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,9].real**2,color_t='blue',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.5,add_line=False,s=10,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[10],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,10].real**2,color_t='cyan',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.1,add_line=False,s=60,cbar_label='Energy',cbar_=False)


    data_.add_x_ticks(plot_index=sub_axis_arry_index[10],x_ticks_range=sample_J01_arry,density=20)

    data_.simple_scatter(plot_index=sub_axis_arry_index[11],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,8].imag**2,color_t='orange',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.2,add_line=False,s=60,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[11],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,11].imag**2,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=1,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[11],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,9].imag**2,color_t='blue',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.5,add_line=False,s=10,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[11],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,10].imag**2,color_t='cyan',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.1,add_line=False,s=60,cbar_label='Energy',cbar_=False)

    data_.add_x_ticks(plot_index=sub_axis_arry_index[11],x_ticks_range=sample_J01_arry,density=20)

    data_.simple_scatter(plot_index=sub_axis_arry_index[15],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,12].real**2,color_t='orange',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.2,add_line=False,s=60,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[15],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,15].real**2,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=1,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[15],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,13].real**2,color_t='blue',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.5,add_line=False,s=10,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[15],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,14].real**2,color_t='cyan',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.1,add_line=False,s=60,cbar_label='Energy',cbar_=False)
    data_.add_x_ticks(plot_index=sub_axis_arry_index[15],x_ticks_range=sample_J01_arry,density=20)

    data_.simple_scatter(plot_index=sub_axis_arry_index[16],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,12].imag**2,color_t='orange',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.2,add_line=False,s=60,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[16],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,15].imag**2,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=1,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[16],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,13].imag**2,color_t='blue',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.5,add_line=False,s=10,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[16],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_2e[:,14].imag**2,color_t='cyan',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.1,add_line=False,s=60,cbar_label='Energy',cbar_=False)

    data_.add_x_ticks(plot_index=sub_axis_arry_index[16],x_ticks_range=sample_J01_arry,density=20)
    data_.add_title(plot_index=sub_axis_arry_index[15],title_name='(2e) Re/Im, ',fontsize=20)
    data_.add_title(plot_index=sub_axis_arry_index[16],title_name=r'at $V_{00}=$'+str(np.round(V_00_arry[entangle_sample_V00_index],2)),fontsize=20)
    data_.add_axis_label(plot_index=sub_axis_arry_index[0],x_axis_name=r'$J_{01}$',y_axis_name=r'',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[0],fontsize=16,rotation_x=0,rotation_y=0)
    data_.add_axis_label(plot_index=sub_axis_arry_index[1],x_axis_name=r'$J_{01}$',y_axis_name=r'',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[0],fontsize=16,rotation_x=0,rotation_y=0)




# Vary V00
    data_.simple_scatter(plot_index=sub_axis_arry_index[2],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,0].real**2,color_t='orange',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.2,add_line=False,s=60,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[2],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,3].real**2,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=1,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[2],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,1].real**2,color_t='blue',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.5,add_line=False,s=10,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[2],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,2].real**2,color_t='cyan',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.1,add_line=False,s=60,cbar_label='Energy',cbar_=False)
    data_.add_x_ticks(plot_index=sub_axis_arry_index[2],x_ticks_range=sample_V00_arry,density=20)

    data_.simple_scatter(plot_index=sub_axis_arry_index[3],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,0].imag**2,color_t='orange',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.2,add_line=False,s=60,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[3],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,3].imag**2,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=1,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[3],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,1].imag**2,color_t='blue',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.5,add_line=False,s=10,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[3],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,2].imag**2,color_t='cyan',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.1,add_line=False,s=60,cbar_label='Energy',cbar_=False)
    data_.add_x_ticks(plot_index=sub_axis_arry_index[3],x_ticks_range=sample_V00_arry,density=20)

    data_.simple_scatter(plot_index=sub_axis_arry_index[7],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,4].real**2,color_t='orange',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.2,add_line=False,s=60,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[7],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,7].real**2,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=1,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[7],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,5].real**2,color_t='blue',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.5,add_line=False,s=10,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[7],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,6].real**2,color_t='cyan',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.1,add_line=False,s=60,cbar_label='Energy',cbar_=False)
    data_.add_x_ticks(plot_index=sub_axis_arry_index[7],x_ticks_range=sample_V00_arry,density=20)

    data_.simple_scatter(plot_index=sub_axis_arry_index[8],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,4].imag**2,color_t='orange',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.2,add_line=False,s=60,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[8],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,7].imag**2,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=1,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[8],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,5].imag**2,color_t='blue',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.5,add_line=False,s=10,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[8],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,6].imag**2,color_t='cyan',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.1,add_line=False,s=60,cbar_label='Energy',cbar_=False)
    data_.add_x_ticks(plot_index=sub_axis_arry_index[8],x_ticks_range=sample_V00_arry,density=20)

    data_.simple_scatter(plot_index=sub_axis_arry_index[12],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,8].real**2,color_t='orange',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.2,add_line=False,s=60,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[12],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,11].real**2,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=1,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[12],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,9].real**2,color_t='blue',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.5,add_line=False,s=10,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[12],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,10].real**2,color_t='cyan',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.1,add_line=False,s=60,cbar_label='Energy',cbar_=False)
    data_.add_x_ticks(plot_index=sub_axis_arry_index[12],x_ticks_range=sample_V00_arry,density=20)

    data_.simple_scatter(plot_index=sub_axis_arry_index[13],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,8].imag**2,color_t='orange',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.2,add_line=False,s=60,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[13],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,11].imag**2,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=1,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[13],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,9].imag**2,color_t='blue',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.5,add_line=False,s=10,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[13],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,10].imag**2,color_t='cyan',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.1,add_line=False,s=60,cbar_label='Energy',cbar_=False)
    data_.add_x_ticks(plot_index=sub_axis_arry_index[13],x_ticks_range=sample_V00_arry,density=20)

    data_.simple_scatter(plot_index=sub_axis_arry_index[17],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,12].real**2,color_t='orange',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.2,add_line=False,s=60,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[17],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,15].real**2,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=1,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[17],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,13].real**2,color_t='blue',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.5,add_line=False,s=10,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[17],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,14].real**2,color_t='cyan',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.1,add_line=False,s=60,cbar_label='Energy',cbar_=False)
    data_.add_x_ticks(plot_index=sub_axis_arry_index[17],x_ticks_range=sample_V00_arry,density=20)

    data_.simple_scatter(plot_index=sub_axis_arry_index[18],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,12].imag**2,color_t='orange',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.2,add_line=False,s=60,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[18],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,15].imag**2,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=1,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[18],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,13].imag**2,color_t='blue',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.5,add_line=False,s=10,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[18],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_2e[:,14].imag**2,color_t='cyan',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.1,add_line=False,s=60,cbar_label='Energy',cbar_=False)
    data_.add_x_ticks(plot_index=sub_axis_arry_index[18],x_ticks_range=sample_V00_arry,density=20)


    data_.add_title(plot_index=sub_axis_arry_index[17],title_name='(2e) Re/Im, ',fontsize=20)
    data_.add_title(plot_index=sub_axis_arry_index[18],title_name=r'at $J_{01}=$'+str(np.round(J01_arry[entangle_sample_J01_index],2)),fontsize=20)
    data_.add_axis_label(plot_index=sub_axis_arry_index[2],x_axis_name=r'$V_{00}$',y_axis_name=r'',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[0],fontsize=16,rotation_x=0,rotation_y=0)
    data_.add_axis_label(plot_index=sub_axis_arry_index[3],x_axis_name=r'$V_{00}$',y_axis_name=r'',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[0],fontsize=16,rotation_x=0,rotation_y=0)

    for s in range(0,len(sub_axis_arry_index)):
        if s==4 or s==9 or s==14:
            pass
        else:
            data_.add_axis_label(plot_index=sub_axis_arry_index[s],x_axis_name=r'',y_axis_name=r'',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[-0.1,1.1],fontsize=16,rotation_x=0,rotation_y=0)
            data_.hline(plot_index=sub_axis_arry_index[s],y0=0.25,x_min=J_01_start,x_max=J_01_end,color='gray',linewidth=1,alpha=0.5)
            data_.hline(plot_index=sub_axis_arry_index[s],y0=0.5,x_min=J_01_start,x_max=J_01_end,color='gray',linewidth=1,alpha=0.5)
            data_.hline(plot_index=sub_axis_arry_index[s],y0=0.75,x_min=J_01_start,x_max=J_01_end,color='gray',linewidth=1,alpha=0.5)



    data_.hline(plot_index=1,y0=np.round(V_00_arry[entangle_sample_V00_index],2),x_min=J_01_start,x_max=J_01_end,color='white',linewidth=2)
    data_.vline(plot_index=1,x0=np.round(J01_arry[entangle_sample_J01_index],2),y_min=V_00_start,y_max=V_00_end,color='white',linewidth=2)

    data_.hline(plot_index=3,y0=np.round(V_00_arry[entangle_sample_V00_index],2),x_min=J_01_start,x_max=J_01_end,color='white',linewidth=2)
    data_.vline(plot_index=3,x0=np.round(J01_arry[entangle_sample_J01_index],2),y_min=V_00_start,y_max=V_00_end,color='white',linewidth=2)
    data_.hline(plot_index=4,y0=np.round(V_00_arry[entangle_sample_V00_index],2),x_min=J_01_start,x_max=J_01_end,color='white',linewidth=2)
    data_.vline(plot_index=4,x0=np.round(J01_arry[entangle_sample_J01_index],2),y_min=V_00_start,y_max=V_00_end,color='white',linewidth=2)
    data_.hline(plot_index=6,y0=np.round(V_00_arry[entangle_sample_V00_index],2),x_min=J_01_start,x_max=J_01_end,color='white',linewidth=2)
    data_.vline(plot_index=6,x0=np.round(J01_arry[entangle_sample_J01_index],2),y_min=V_00_start,y_max=V_00_end,color='white',linewidth=2)

    data_.show_legend(plot_index=sub_axis_arry_index[5],loc='upper left', bbox_to_anchor=(-0.9, 4.2),fontsize=15)
    data_.add_text(plot_index=sub_axis_arry_index[0],x=2*J_01_start-1*np.max(sample_J01_arry),y=0,s=r'$|\Omega_0>\rightarrow $: ',bg_color='white',fontsize=20, alpha=0.5)
    data_.add_text(plot_index=sub_axis_arry_index[5],x=2*J_01_start-1*np.max(sample_J01_arry),y=0,s=r'$|\mathrm{Ex}_1>\rightarrow $: ',bg_color='white',fontsize=20, alpha=0.5)
    data_.add_text(plot_index=sub_axis_arry_index[10],x=2*J_01_start-1*np.max(sample_J01_arry),y=0,s=r'$|\mathrm{Ex}_2>\rightarrow $: ',bg_color='white',fontsize=20, alpha=0.5)
    data_.add_text(plot_index=sub_axis_arry_index[15],x=2*J_01_start-1*np.max(sample_J01_arry),y=0,s=r'$|\mathrm{Ex}_3>\rightarrow $: ',bg_color='white',fontsize=20, alpha=0.5)
# For three Electrons

    sub_axis_arry,sub_axis_arry_index=data_.add_subplot_sub_non_uniform_grid_row(plot_index=5,size_x_array=[4,1,4],y_ratio_array=[0,0.45,0.05,0.45])

    data_.simple_scatter(plot_index=sub_axis_arry_index[0],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_3e[:,0].real**2,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=r'$0\uparrow$,$0\downarrow$,$x\uparrow$ ',twinx=False,alpha=1,add_line=False,s=0.5,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[0],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_3e[:,1].real**2,color_t='blue',marker='s',log_scale_x=False,log_scale_y=False,label_name=r'$0\uparrow$,$x\downarrow$,$x\uparrow$ ',twinx=False,alpha=0.5,add_line=False,s=10,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[1],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_3e[:,0].imag**2,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=0.5,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[1],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_3e[:,1].imag**2,color_t='blue',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.5,add_line=False,s=10,cbar_label='Energy',cbar_=False)


    data_.simple_scatter(plot_index=sub_axis_arry_index[5],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_3e[:,2].real**2,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=0.5,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[5],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_3e[:,3].real**2,color_t='blue',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.5,add_line=False,s=10,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[6],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_3e[:,2].imag**2,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=0.5,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[6],x_arry=sample_J01_arry,y_arry=entangle_sample_J01_arry_3e[:,3].imag**2,color_t='blue',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.5,add_line=False,s=10,cbar_label='Energy',cbar_=False)

    data_.add_x_ticks(plot_index=sub_axis_arry_index[0],x_ticks_range=sample_J01_arry,density=20)
    data_.add_x_ticks(plot_index=sub_axis_arry_index[1],x_ticks_range=sample_J01_arry,density=20)
    data_.add_x_ticks(plot_index=sub_axis_arry_index[2],x_ticks_range=sample_J01_arry,density=20)
    data_.add_x_ticks(plot_index=sub_axis_arry_index[3],x_ticks_range=sample_J01_arry,density=20)

    data_.simple_scatter(plot_index=sub_axis_arry_index[2],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_3e[:,0].real**2,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=0.5,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[2],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_3e[:,1].real**2,color_t='blue',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.5,add_line=False,s=10,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[3],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_3e[:,0].imag**2,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=0.5,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[3],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_3e[:,1].imag**2,color_t='blue',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.5,add_line=False,s=10,cbar_label='Energy',cbar_=False)


    data_.simple_scatter(plot_index=sub_axis_arry_index[7],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_3e[:,2].real**2,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=0.5,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[7],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_3e[:,3].real**2,color_t='blue',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.5,add_line=False,s=10,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[8],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_3e[:,2].imag**2,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=1,add_line=False,s=0.5,cbar_label='Energy',cbar_=False)
    data_.simple_scatter(plot_index=sub_axis_arry_index[8],x_arry=sample_V00_arry,y_arry=entangle_sample_V00_arry_3e[:,3].imag**2,color_t='blue',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.5,add_line=False,s=10,cbar_label='Energy',cbar_=False)

    data_.add_x_ticks(plot_index=sub_axis_arry_index[7],x_ticks_range=sample_V00_arry,density=20)
    data_.add_x_ticks(plot_index=sub_axis_arry_index[8],x_ticks_range=sample_V00_arry,density=20)
    data_.add_x_ticks(plot_index=sub_axis_arry_index[5],x_ticks_range=sample_V00_arry,density=20)
    data_.add_x_ticks(plot_index=sub_axis_arry_index[6],x_ticks_range=sample_V00_arry,density=20)


    data_.add_axis_label(plot_index=sub_axis_arry_index[2],x_axis_name=r'$V_{00}$',y_axis_name=r'',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[0],fontsize=16,rotation_x=0,rotation_y=0)
    data_.add_axis_label(plot_index=sub_axis_arry_index[3],x_axis_name=r'$V_{00}$',y_axis_name=r'',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[0],fontsize=16,rotation_x=0,rotation_y=0)
    data_.add_axis_label(plot_index=sub_axis_arry_index[0],x_axis_name=r'$J_{01}$',y_axis_name=r'',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[0],fontsize=16,rotation_x=0,rotation_y=0)
    data_.add_axis_label(plot_index=sub_axis_arry_index[1],x_axis_name=r'$J_{01}$',y_axis_name=r'',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[0],fontsize=16,rotation_x=0,rotation_y=0)

    data_.add_title(plot_index=sub_axis_arry_index[5],title_name='(3e) Re/Im, ',fontsize=20)
    data_.add_title(plot_index=sub_axis_arry_index[6],title_name=r'at $V_{00}=$'+str(np.round(V_00_arry[entangle_sample_V00_index],2)),fontsize=20)
    data_.add_title(plot_index=sub_axis_arry_index[7],title_name='(3e) Re/Im, ',fontsize=20)
    data_.add_title(plot_index=sub_axis_arry_index[8],title_name=r'at $J_{01}=$'+str(np.round(J01_arry[entangle_sample_J01_index],2)),fontsize=20)
    data_.add_title(plot_index=2,title_name=r'(2e) State Coefficients',fontsize=20)
    data_.add_title(plot_index=5,title_name=r'(3e) State Coefficients',fontsize=20)
    
    data_.show_legend(plot_index=sub_axis_arry_index[0],loc='upper left', bbox_to_anchor=(-0.9, 2.5),fontsize=15)
    data_.add_text(plot_index=sub_axis_arry_index[0],x=2*J_01_start-1*np.max(sample_J01_arry),y=0,s=r'$|\Omega_0>\rightarrow $: ',bg_color='white',fontsize=20, alpha=0.5)
    data_.add_text(plot_index=sub_axis_arry_index[5],x=2*J_01_start-1*np.max(sample_J01_arry),y=0,s=r'$|\mathrm{Ex}_1>\rightarrow $: ',bg_color='white',fontsize=20, alpha=0.5)

    for s in range(0,len(sub_axis_arry_index)):
        if s==4 or s==9 or s==14:
            pass
        else:
            data_.add_axis_label(plot_index=sub_axis_arry_index[s],x_axis_name=r'',y_axis_name=r'',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[-0.1,1.1],fontsize=16,rotation_x=0,rotation_y=0)
            data_.hline(plot_index=sub_axis_arry_index[s],y0=0.25,x_min=V_00_start,x_max=V_00_end,color='gray',linewidth=1,alpha=0.5)
            data_.hline(plot_index=sub_axis_arry_index[s],y0=0.5,x_min=V_00_start,x_max=V_00_end,color='gray',linewidth=1,alpha=0.5)
            data_.hline(plot_index=sub_axis_arry_index[s],y0=0.75,x_min=V_00_start,x_max=V_00_end,color='gray',linewidth=1,alpha=0.5)


    data_.save_fig(out_dir,200,str(k))
    data_.close_fig()

video_series='/heatmap_V11_'+str(V_11)+'_w1_'+str(w1)

out_loc=path_to_cache+'/videos/'+video_series+'/'
width=20
height=20
data_=Data_process(row_num=2,column_num=2,root_dir=root_loc,width=width,height=height,letter=False)
data_.rebuild_dir(file_loc=out_loc)
data_.videos(img_loc=root_loc+out_dir,out_loc=out_loc,out_file_name='V11_'+str(V_11)+'_w1_'+str(w1)+'_N_'+str(N_sample)+'.mp4',N=N_sample)