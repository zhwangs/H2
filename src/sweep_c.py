from data_ex_onlyx import *



def c_sweep(V_ratio_01,w,V_11,V_ratio_00,V_ratio_00_start,V_ratio_01_start,J01,J11,control_p=0,density=100,coeff_on=False,coeff_index=0,sweep_row=-1,sweep_col=-1):

    V_01_arry=np.linspace(V_ratio_01_start*V_11,V_11*V_ratio_01,density)
    V_00_arry=np.linspace(V_ratio_00_start*V_11,V_11*V_ratio_00,density)#

    E_opt_1_arry_2e=np.zeros((density,density))

    E_opt_1_arry_3e=np.zeros((density,density))

    Binding_arry_2e=np.zeros((density,density))

    Binding_arry_3e=np.zeros((density,density))
    
    
    
    
    for i in range(0,density):
        for j in range(0,density):
            
            V00=V_00_arry[j]
            V01=V_01_arry[i]
            V11=V_11
            J01=J01
            J11=J11
            t=0
 
            
            H=H_sys(V00,V01,V11,J01,J11,t,w,control_p,control_d=1)
            E_opt_1_2e, binding_energy_2e,E_opt_1_3e, binding_energy_3e =H.get_binding()
            #H.print_info_2e(print_=True,print_vector=False,print_coeff=False)
            E_opt_1_arry_2e[i,j]=E_opt_1_2e
            Binding_arry_2e[i,j]=binding_energy_2e
            E_opt_1_arry_3e[i,j]=E_opt_1_3e
            Binding_arry_3e[i,j]=binding_energy_3e

            coeff_array_2e=[]
            coeff_index_array_2e=[]

            coeff_array_3e=[]
            coeff_index_array_3e=[]
            # Coeff gets
            if coeff_on:
                if sweep_row==-1 &sweep_row!=-1 :
                    if i==sweep_col:

                        coeff_2e,coeff_index_2e=H.get_coeff_2e(coeff_index)
                        print(coeff_index_2e)
                        print(len(coeff_index_2e))
                        #coeff_array_2e.append(coeff_2e)

                        coeff_3e,coeff_index_3e=H.get_coeff_3e(coeff_index)
                        print(coeff_index_3e)
                        print(len(coeff_index_3e))


            #$print(binding_energy_2e-binding_energy_3e)
    #print(Binding_arry_3e-Binding_arry_2e)
    return V_01_arry/V_11,V_00_arry/V_11,E_opt_1_arry_2e,Binding_arry_2e,E_opt_1_arry_3e,Binding_arry_3e

def c_sweep_coeff(V_ratio_01,w,V_11,V_ratio_00,V_ratio_00_start,control_p=0,density=100,index=0):

    V_01_arry=np.linspace(0,V_11*V_ratio_01,density)
    V_00_arry=np.linspace(V_ratio_00_start*V_11,V_11*V_ratio_00,density)#

    E_opt_1_arry_2e=np.zeros((density,density))

    E_opt_1_arry_3e=np.zeros((density,density))

    Binding_arry_2e=np.zeros((density,density))

    Binding_arry_3e=np.zeros((density,density))
    
    
    
    
    for i in range(0,density):
        for j in range(0,density):
            
            V00=V_00_arry[j]
            V01=V_01_arry[i]
            V11=V_11
            J01=0
            J11=0
            t=0
 
            
            H=H_sys(V00,V01,V11,J01,J11,t,w,control_p,control_d=1)
            E_opt_1_2e, binding_energy_2e,E_opt_1_3e, binding_energy_3e =H.get_binding()
            E_opt_1_arry_2e[int(density-i-1),j]=E_opt_1_2e
            Binding_arry_2e[int(density-i-1),j]=binding_energy_2e
            E_opt_1_arry_3e[int(density-i-1),j]=E_opt_1_3e
            Binding_arry_3e[int(density-i-1),j]=binding_energy_3e
            #$print(binding_energy_2e-binding_energy_3e)
    print(Binding_arry_3e-Binding_arry_2e)
    return V_01_arry/V_11,V_00_arry/V_11,E_opt_1_arry_2e,Binding_arry_2e,E_opt_1_arry_3e,Binding_arry_3e

