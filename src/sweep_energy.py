from data_ex import *



def energy_sweep_V01(w,V_01_start,V_01_end,V_11,V_00,J01,J11,low_energy_reso=10,bin_density=100,control_p=0,density=100,gaussian_broadening=100,trial_run=100):



    V_01_arry=np.linspace(V_01_start,V_01_end,density)

    E__2e=np.zeros((density,9))
    E__3e=np.zeros((density,9))
   # Hist_2e=np.zeros((density,bin_density-1)) this is for the noise case 
   # Hist_3e=np.zeros((density,bin_density-1))this is for the noise case 
    Hist_2e=np.zeros((density,bin_density))
    Hist_3e=np.zeros((density,bin_density))
    
    
    for i in range(0,density):
        
        V00=V_00
        V01=V_01_arry[i]
        V11=V_11
        J01=J01
        J11=J11
        t=0

        
        H=H_sys(V00,V01,V11,J01,J11,t,w,control_p,control_d=1)
        smooth_2e_val,smooth_3e_val=H.energy_level(low_energy_reso)
        E__2e[i]=np.array(smooth_2e_val)
        E__3e[i]=np.array(smooth_3e_val)
        #H_t=H.energy_hist_info(bin_density=100,gaussian_broadening=gaussian_broadening,trial_run=trial_run)
        H_t=H.energy_gaussian(bin_density=bin_density,gaussian_broadening=gaussian_broadening)
        Hist_2e[i]=H_t[0]
        Hist_3e[i]=H_t[1]

        #print(Hist_[i])
    Hit_arry=H_t[2] 
   # print(Hist_2e)

    return V_01_arry,E__2e,E__3e,Hist_2e,Hist_3e,Hit_arry


def energy_sweep_V00(w,V_00_start,V_00_end,V_11,V_01,J01,J11,low_energy_reso=10,bin_density=100,control_p=0,density=100,gaussian_broadening=100,trial_run=100):



    V_00_arry=np.linspace(V_00_start,V_00_end,density)

    E__2e=np.zeros((density,9))
    E__3e=np.zeros((density,9))
   # Hist_2e=np.zeros((density,bin_density-1)) this is for the noise case 
   # Hist_3e=np.zeros((density,bin_density-1))this is for the noise case 
    Hist_2e=np.zeros((density,bin_density))
    Hist_3e=np.zeros((density,bin_density))
    
    for i in range(0,density):
        
        V00=V_00_arry[i]
        V01=V_01
        V11=V_11
        J01=J01
        J11=J11
        t=0

        
        H=H_sys(V00,V01,V11,J01,J11,t,w,control_p,control_d=1)
        smooth_2e_val,smooth_3e_val=H.energy_level(low_energy_reso)
        E__2e[i]=np.array(smooth_2e_val)
        E__3e[i]=np.array(smooth_3e_val)
        #H_t=H.energy_hist_info(bin_density=100,gaussian_broadening=gaussian_broadening,trial_run=trial_run)
        H_t=H.energy_gaussian(bin_density=bin_density,gaussian_broadening=gaussian_broadening)

        Hist_2e[i]=H_t[0]
        Hist_3e[i]=H_t[1]

        #print(Hist_[i])
    Hit_arry=H_t[2] 
   # print(Hist_2e)

    return V_00_arry,E__2e,E__3e,Hist_2e,Hist_3e,Hit_arry



def energy_sweep_J01(w0,w1,J_01_start,J_01_end,V_11,V_00,V01,J11,low_energy_reso=10,bin_density=100,density=100,gaussian_broadening=100):



    J_01_arry=np.linspace(J_01_start,J_01_end,density)

    E__2e=np.zeros((density,9))
    E__3e=np.zeros((density,9))
   # Hist_2e=np.zeros((density,bin_density-1)) this is for the noise case 
   # Hist_3e=np.zeros((density,bin_density-1))this is for the noise case 
    Hist_2e=np.zeros((density,bin_density))
    Hist_3e=np.zeros((density,bin_density))
    
    
    for i in range(0,density):
        
        V00=V_00
        V01=V01#V_01_arry[i]
        V11=V_11
        J01=J_01_arry[i]
        J11=J11
        t=0

        
        H=H_sys(V00,V01,V11,J01,J11,t,w0,w1)
        smooth_2e_val,smooth_3e_val=H.energy_level(low_energy_reso)
        E__2e[i]=np.array(smooth_2e_val)
        E__3e[i]=np.array(smooth_3e_val)
        #H_t=H.energy_hist_info(bin_density=100,gaussian_broadening=gaussian_broadening,trial_run=trial_run)
        H_t=H.energy_gaussian(bin_density=bin_density,gaussian_broadening=gaussian_broadening)
        Hist_2e[i]=H_t[0]
        Hist_3e[i]=H_t[1]

        #print(Hist_[i])
    Hit_arry=H_t[2] 
   # print(Hist_2e)

    return J_01_arry,E__2e,E__3e,Hist_2e,Hist_3e,Hit_arry

def energy_sweep_J11(w0,w1,J_11_start,J_11_end,V_11,V_00,V01,J01,low_energy_reso=10,bin_density=100,density=100,gaussian_broadening=100):



    J_11_arry=np.linspace(J_11_start,J_11_end,density)

    E__2e=np.zeros((density,9))
    E__3e=np.zeros((density,9))
   # Hist_2e=np.zeros((density,bin_density-1)) this is for the noise case 
   # Hist_3e=np.zeros((density,bin_density-1))this is for the noise case 
    Hist_2e=np.zeros((density,bin_density))
    Hist_3e=np.zeros((density,bin_density))
    
    
    for i in range(0,density):
        
        V00=V_00
        V01=V01#V_01_arry[i]
        V11=V_11
        J01=J01
        J11=J_11_arry[i]
        t=0

        
        H=H_sys(V00,V01,V11,J01,J11,t,w0,w1)
        smooth_2e_val,smooth_3e_val=H.energy_level(low_energy_reso)
        E__2e[i]=np.array(smooth_2e_val)
        E__3e[i]=np.array(smooth_3e_val)
        #H_t=H.energy_hist_info(bin_density=100,gaussian_broadening=gaussian_broadening,trial_run=trial_run)
        H_t=H.energy_gaussian(bin_density=bin_density,gaussian_broadening=gaussian_broadening)
        Hist_2e[i]=H_t[0]
        Hist_3e[i]=H_t[1]

        #print(Hist_[i])
    Hit_arry=H_t[2] 
   # print(Hist_2e)

    return J_11_arry,E__2e,E__3e,Hist_2e,Hist_3e,Hit_arry




def energy_eigen_map(w0,w1,J01,V11,V00,V01,J11):
    t=0
    H=H_sys(V00,V01,V11,J01,J11,t,w0,w1)
    info_vector1=H.get_first_two_eigen_info()

    return info_vector1

def save(array,append_=True,data_file='peak_data.csv'):
    if append_:
        with open(data_file, "a") as f:
            np.savetxt(f, np.column_stack(array), fmt='%f', delimiter=',')
    else:
        with open(data_file, "w+") as f:
            np.savetxt(f, np.column_stack(array), fmt='%f', delimiter=',')
