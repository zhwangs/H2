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

w0_start=0.000001
w0_end=10
N=100
w0_arry=np.linspace(0.4,1,N)
w0_start=0.000001
w0_end=10
w0_arry=np.logspace(w0_start, w0_end,N, base=2.0)
N_w1=1
w1_arry=np.linspace(60,10,N_w1)
 



width=20
height=20
root_loc=path_to_cache+'/data'
data_=Data_process(row_num=1,column_num=1,root_dir=root_loc,width=width,height=height,letter=False)

data_.add_axis_label(plot_index=1,x_axis_name=r'$\omega_0/\omega_1$',y_axis_name=r'$Dif$',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[0],fontsize=16,rotation_x=0,rotation_y=0)
data_.add_title(plot_index=1,title_name='(2e) Energy Spectrum (vary J01) ',fontsize=20)

for j in range(0,N_w1):
    w1= w1_arry[j]
    ratio_arry=[]
    Dif_arry=[]
    for i in range(0,N):
        w0=w0_arry[i]
        H=H_sys(V00,V01,V11,J01,J11,t,w0,w1)
        #print(H.normalize((Eig_1+Eig_2)))
        Ex_dif, E_dif,Dif,ratio=H.get_extion_info()
        ratio_arry.append(ratio)
        Dif_arry.append(Dif)

    data_.simple_scatter(plot_index=1,x_arry=ratio_arry,y_arry=Dif_arry,color_t=5*w1*np.ones(len(ratio_arry)),marker='s',log_scale_x=True,log_scale_y=True,label_name=' ',twinx=False,alpha=1,add_line=False,s=10,cbar_=False)
    file_loc='/exciton_dff_w1_'+str(w1) 

data_.save_fig('',200,file_loc)
data_.close_fig()
print(w0_arry.max())
# In[ ]:





# In[390]:


# In[ ]:





# In[ ]:





# In[ ]:




