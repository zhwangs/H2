from data_ex import *


def j_sweep(J_val,J_ratio_01,w,V_00,V_01,V_11,J_ratio_11,J_ratio_01_start,J_ratio_11_start,control_p=0,density=100):

    J_01_arry=np.linspace(J_ratio_01_start*J_val,J_val*J_ratio_01,density)
    J_11_arry=np.linspace(J_ratio_11_start*J_val,J_val*J_ratio_11,density)#

    E_opt_1_arry_2e=np.zeros((density,density))

    E_opt_1_arry_3e=np.zeros((density,density))

    Binding_arry_2e=np.zeros((density,density))

    Binding_arry_3e=np.zeros((density,density))
    
    
    
    
    for i in range(0,density):
        for j in range(0,density):
            
            V00=V_00
            V01=V_01
            V11=V_11
            J01=J_01_arry[i]
            J11=J_11_arry[j]
            t=0
 
            
            H=H_sys(V00,V01,V11,J01,J11,t,w,control_p,control_d=1)
            E_opt_1_2e, binding_energy_2e,E_opt_1_3e, binding_energy_3e =H.get_binding()
            #H.print_info_2e(print_=True,print_vector=False,print_coeff=False)
            E_opt_1_arry_2e[i,j]=E_opt_1_2e
            Binding_arry_2e[i,j]=binding_energy_2e
            E_opt_1_arry_3e[i,j]=E_opt_1_3e
            Binding_arry_3e[i,j]=binding_energy_3e
            #$print(binding_energy_2e-binding_energy_3e)
    #Binding_arry_3e[0,98]=-10000
    return J_01_arry/J_val,J_11_arry/J_val,E_opt_1_arry_2e,Binding_arry_2e,E_opt_1_arry_3e,Binding_arry_3e
