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

J01=0
J11=0

t=0
w1=12
w0=9

N_J=100
J01_start=0
J01_end=30
J01_arry=np.linspace(J01_start,J01_end,N_J)
root_loc=path_to_cache+'/data'
for l in range(0,N_J):
    J01=J01_arry[l]
    H=H_sys(V00,V01,V11,J01,J11,t,w0,w1)

    H.index_2e()
    eigen_ref_2=H.get_ref_eigen_val()

    omega_start=-30
    omega_end=-25
    N=10000
    G0x_real_arry, G0x_imag_arry,G0y_real_arry, G0y_imag_arry,G00_real_arry, G00_imag_arry,Gxx_real_arry, Gxx_imag_arry,Gyy_real_arry, Gyy_imag_arry,Gyx_real_arry, Gyx_imag_arry, omega_arry=H.Green_fuc(omega_start,omega_end,N)
    
    width=20
    height=20

    data_=Data_process(row_num=6,column_num=2,root_dir=root_loc,width=width,height=height,letter=False)
    data_.fig_title(fig_name=r'$\omega_0=$'+str(w0)+r' $\omega_1=$'+str(w1)+r' $J_{0 1}=$'+str(np.round(J01,2)),title_size=30)
    data_.add_axis_label(plot_index=1,x_axis_name=r'$\omega$',y_axis_name=r'Re$\{G_{0x}\}$',x_label_loc=0,y_label_loc=0,x_axis_range=[omega_start,omega_end],y_axis_range=[-1.5,1.5],fontsize=16,rotation_x=0,rotation_y=0)
    data_.add_axis_label(plot_index=3,x_axis_name=r'$\omega$',y_axis_name=r'Im$\{G_{0x}\}$',x_label_loc=0,y_label_loc=0,x_axis_range=[omega_start,omega_end],y_axis_range=[-2.5,1.2],fontsize=16,rotation_x=0,rotation_y=0)

    #data_.add_title(plot_index=1,title_name='G0x ',fontsize=20)

    data_.add_axis_label(plot_index=2,x_axis_name=r'$\omega$',y_axis_name=r'Re$\{G_{0 0}\}$',x_label_loc=0,y_label_loc=0,x_axis_range=[omega_start,omega_end],y_axis_range=[-0.5,0.5],fontsize=16,rotation_x=0,rotation_y=0)
    data_.add_axis_label(plot_index=4,x_axis_name=r'$\omega$',y_axis_name=r'Im$\{G_{0 0}\}$',x_label_loc=0,y_label_loc=0,x_axis_range=[omega_start,omega_end],y_axis_range=[0.5,1.5],fontsize=16,rotation_x=0,rotation_y=0)

    data_.add_axis_label(plot_index=5,x_axis_name=r'$\omega$',y_axis_name=r'Re$\{G_{xx}\}$',x_label_loc=0,y_label_loc=0,x_axis_range=[omega_start,omega_end],y_axis_range=[-0.5,0.5],fontsize=16,rotation_x=0,rotation_y=0)
    data_.add_axis_label(plot_index=7,x_axis_name=r'$\omega$',y_axis_name=r'Im$\{G_{xx}\}$',x_label_loc=0,y_label_loc=0,x_axis_range=[omega_start,omega_end],y_axis_range=[0.5,1.5],fontsize=16,rotation_x=0,rotation_y=0)

    data_.add_axis_label(plot_index=6,x_axis_name=r'$\omega$',y_axis_name=r'Re$\{G_{yx}\}$',x_label_loc=0,y_label_loc=0,x_axis_range=[omega_start,omega_end],y_axis_range=[-0.5,0.5],fontsize=16,rotation_x=0,rotation_y=0)
    data_.add_axis_label(plot_index=8,x_axis_name=r'$\omega$',y_axis_name=r'Im$\{G_{yx}\}$',x_label_loc=0,y_label_loc=0,x_axis_range=[omega_start,omega_end],y_axis_range=[0.5,1.5],fontsize=16,rotation_x=0,rotation_y=0)

    data_.add_axis_label(plot_index=9,x_axis_name=r'$\omega$',y_axis_name=r'Re$\{G_{0y}\}$',x_label_loc=0,y_label_loc=0,x_axis_range=[omega_start,omega_end],y_axis_range=[-0.5,0.5],fontsize=16,rotation_x=0,rotation_y=0)
    data_.add_axis_label(plot_index=11,x_axis_name=r'$\omega$',y_axis_name=r'Im$\{G_{0y}\}$',x_label_loc=0,y_label_loc=0,x_axis_range=[omega_start,omega_end],y_axis_range=[0.5,1.5],fontsize=16,rotation_x=0,rotation_y=0)

    data_.add_axis_label(plot_index=10,x_axis_name=r'$\omega$',y_axis_name=r'Re$\{G_{yy}\}$',x_label_loc=0,y_label_loc=0,x_axis_range=[omega_start,omega_end],y_axis_range=[-0.5,0.5],fontsize=16,rotation_x=0,rotation_y=0)
    data_.add_axis_label(plot_index=12,x_axis_name=r'$\omega$',y_axis_name=r'Im$\{G_{yy}\}$',x_label_loc=0,y_label_loc=0,x_axis_range=[omega_start,omega_end],y_axis_range=[0.5,1.5],fontsize=16,rotation_x=0,rotation_y=0)



    data_.simple_scatter(plot_index=3,x_arry=omega_arry,y_arry=G0x_imag_arry,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.4,add_line=True,s=0.1,cbar_=False)
    data_.simple_scatter(plot_index=1,x_arry=omega_arry,y_arry=G0x_real_arry,color_t='green',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.4,add_line=True,s=0.1,cbar_=False)

    data_.simple_scatter(plot_index=4,x_arry=omega_arry,y_arry=G00_imag_arry,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.4,add_line=True,s=0.1,cbar_=False)
    data_.simple_scatter(plot_index=2,x_arry=omega_arry,y_arry=G00_real_arry,color_t='green',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.4,add_line=True,s=0.1,cbar_=False)

    data_.simple_scatter(plot_index=7,x_arry=omega_arry,y_arry=Gxx_imag_arry,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.4,add_line=True,s=0.1,cbar_=False)
    data_.simple_scatter(plot_index=5,x_arry=omega_arry,y_arry=Gxx_real_arry,color_t='green',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.4,add_line=True,s=0.1,cbar_=False)

    data_.simple_scatter(plot_index=8,x_arry=omega_arry,y_arry=Gyx_imag_arry,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.4,add_line=True,s=0.1,cbar_=False)
    data_.simple_scatter(plot_index=6,x_arry=omega_arry,y_arry=Gyx_real_arry,color_t='green',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.4,add_line=True,s=0.1,cbar_=False)

    data_.simple_scatter(plot_index=11,x_arry=omega_arry,y_arry=G0y_imag_arry,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.4,add_line=True,s=0.1,cbar_=False)
    data_.simple_scatter(plot_index=9,x_arry=omega_arry,y_arry=G0y_real_arry,color_t='green',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.4,add_line=True,s=0.1,cbar_=False)

    data_.simple_scatter(plot_index=12,x_arry=omega_arry,y_arry=Gyy_imag_arry,color_t='red',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.4,add_line=True,s=0.1,cbar_=False)
    data_.simple_scatter(plot_index=10,x_arry=omega_arry,y_arry=Gyy_real_arry,color_t='green',marker='s',log_scale_x=False,log_scale_y=False,label_name=' ',twinx=False,alpha=0.4,add_line=True,s=0.1,cbar_=False)

    

    for s in range(1,len(eigen_ref_2)):

        data_.simple_plot(plot_index=1,x_arry=eigen_ref_2[s].real*np.ones(len(omega_arry)),y_arry=np.linspace(-3,3,len(omega_arry)),log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=0.3,lw=1)
        data_.simple_plot(plot_index=2,x_arry=eigen_ref_2[s].real*np.ones(len(omega_arry)),y_arry=np.linspace(-3,3,len(omega_arry)),log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=0.3,lw=1)
        data_.simple_plot(plot_index=3,x_arry=eigen_ref_2[s].real*np.ones(len(omega_arry)),y_arry=np.linspace(-3,3,len(omega_arry)),log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=0.3,lw=1)
        data_.simple_plot(plot_index=4,x_arry=eigen_ref_2[s].real*np.ones(len(omega_arry)),y_arry=np.linspace(-3,3,len(omega_arry)),log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=0.3,lw=1)
        data_.simple_plot(plot_index=5,x_arry=eigen_ref_2[s].real*np.ones(len(omega_arry)),y_arry=np.linspace(-3,3,len(omega_arry)),log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=0.3,lw=1)
        data_.simple_plot(plot_index=6,x_arry=eigen_ref_2[s].real*np.ones(len(omega_arry)),y_arry=np.linspace(-3,3,len(omega_arry)),log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=0.3,lw=1)

        data_.simple_plot(plot_index=1,x_arry=-eigen_ref_2[s].real*np.ones(len(omega_arry)),y_arry=np.linspace(-3,3,len(omega_arry)),log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=0.3,lw=1)
        data_.simple_plot(plot_index=2,x_arry=-eigen_ref_2[s].real*np.ones(len(omega_arry)),y_arry=np.linspace(-3,3,len(omega_arry)),log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=0.3,lw=1)
        data_.simple_plot(plot_index=3,x_arry=-eigen_ref_2[s].real*np.ones(len(omega_arry)),y_arry=np.linspace(-3,3,len(omega_arry)),log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=0.3,lw=1)
        data_.simple_plot(plot_index=4,x_arry=-eigen_ref_2[s].real*np.ones(len(omega_arry)),y_arry=np.linspace(-3,3,len(omega_arry)),log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=0.3,lw=1)
        data_.simple_plot(plot_index=5,x_arry=-eigen_ref_2[s].real*np.ones(len(omega_arry)),y_arry=np.linspace(-3,3,len(omega_arry)),log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=0.3,lw=1)
        data_.simple_plot(plot_index=6,x_arry=-eigen_ref_2[s].real*np.ones(len(omega_arry)),y_arry=np.linspace(-3,3,len(omega_arry)),log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=0.3,lw=1)

        data_.simple_plot(plot_index=7,x_arry=eigen_ref_2[s].real*np.ones(len(omega_arry)),y_arry=np.linspace(-3,3,len(omega_arry)),log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=0.3,lw=1)
        data_.simple_plot(plot_index=8,x_arry=eigen_ref_2[s].real*np.ones(len(omega_arry)),y_arry=np.linspace(-3,3,len(omega_arry)),log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=0.3,lw=1)
        data_.simple_plot(plot_index=9,x_arry=eigen_ref_2[s].real*np.ones(len(omega_arry)),y_arry=np.linspace(-3,3,len(omega_arry)),log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=0.3,lw=1)
        data_.simple_plot(plot_index=10,x_arry=eigen_ref_2[s].real*np.ones(len(omega_arry)),y_arry=np.linspace(-3,3,len(omega_arry)),log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=0.3,lw=1)
        data_.simple_plot(plot_index=11,x_arry=eigen_ref_2[s].real*np.ones(len(omega_arry)),y_arry=np.linspace(-3,3,len(omega_arry)),log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=0.3,lw=1)
        data_.simple_plot(plot_index=12,x_arry=eigen_ref_2[s].real*np.ones(len(omega_arry)),y_arry=np.linspace(-3,3,len(omega_arry)),log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=0.3,lw=1)

        data_.simple_plot(plot_index=7,x_arry=-eigen_ref_2[s].real*np.ones(len(omega_arry)),y_arry=np.linspace(-3,3,len(omega_arry)),log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=0.3,lw=1)
        data_.simple_plot(plot_index=8,x_arry=-eigen_ref_2[s].real*np.ones(len(omega_arry)),y_arry=np.linspace(-3,3,len(omega_arry)),log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=0.3,lw=1)
        data_.simple_plot(plot_index=9,x_arry=-eigen_ref_2[s].real*np.ones(len(omega_arry)),y_arry=np.linspace(-3,3,len(omega_arry)),log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=0.3,lw=1)
        data_.simple_plot(plot_index=10,x_arry=-eigen_ref_2[s].real*np.ones(len(omega_arry)),y_arry=np.linspace(-3,3,len(omega_arry)),log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=0.3,lw=1)
        data_.simple_plot(plot_index=11,x_arry=-eigen_ref_2[s].real*np.ones(len(omega_arry)),y_arry=np.linspace(-3,3,len(omega_arry)),log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=0.3,lw=1)
        data_.simple_plot(plot_index=12,x_arry=-eigen_ref_2[s].real*np.ones(len(omega_arry)),y_arry=np.linspace(-3,3,len(omega_arry)),log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=0.3,lw=1)

            #data_.simple_plot(plot_index=2,x_arry=eigen_ref_2[s]*np.ones(len(J_11_arry)),y_arry=J_11_arry,log_scale_x=False,log_scale_y=False,color_t='black',label_name=' ',alpha=1,lw=1)
    file_loc='/'+str(l) 
    img_loc='/green_scan2'
    data_.save_fig(img_loc,200,file_loc)
    data_.close_fig()
video_series='/w0_'+str(w0)+'_w1_'+str(w1)
img_loc='/green_scan'
out_loc=path_to_cache+'/videos/'+video_series+'/'
width=20
height=20
data_=Data_process(row_num=2,column_num=2,root_dir=root_loc,width=width,height=height,letter=False)
data_.rebuild_dir(file_loc=out_loc)
data_.videos(img_loc=root_loc+img_loc,out_loc=out_loc,out_file_name='test'+'.mp4',N=N_J)
# In[ ]:





# In[390]:


# In[ ]:





# In[ ]:





# In[ ]:




