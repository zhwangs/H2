from src import *
class H_sys:
    def __init__(self,V00,V01,V11,J01,J11,t,w0,w):
        self.w=w
        self.V00=V00
        self.V11=V11
        self.V01=V01
        self.J01=J01
        self.J11=J11
        self.t=t
        self.w0=w0

        # For two electrons 
        A_0= V00-4/3*w
        A_1= V01-1/3*w
        A_2= V11+2/3*w
        matrix_H=np.array([
        [A_0, -1j*w0, -1j*w0,-1j*w0, -1j*w0, 0, 0, 0, 0],
        [1j*w0, A_1,  J01,-t, 0,-1j*w0, 0,-1j*w0, 0],
        [1j*w0,  J01, A_1, 0, -t, -1j*w0,-1j*w0, 0, 0],
        [1j*w0, -t, 0, A_1, J01, 0,-1j*w0, 0, -1j*w0],
        [1j*w0, 0, -t,   J01, A_1, 0, 0, -1j*w0, -1j*w0],
        [0, 1j*w0, 1j*w0, 0, 0, A_2, -t, -t, 0],
        [0, 0, 1j*w0, 1j*w0, 0, -t, A_2,   J11, -t],
        [0, 1j*w0, 0, 0, 1j*w0, -t,  J11, A_2,-t],
        [0, 0, 0, 1j*w0, 1j*w0, 0, -t, -t,A_2]])
        self.Val_1=linalg.eig(matrix_H)





        #print(matrix_H)
       # print(np.round(self.Val_1[1],2))
        # For three electron 
        B_0=2*V01+V00-w
        B_1=2*V01+V11
        B_2=3*V11+w
        matrix_H=np.array([
        [B_0, -t, -1j*w0,0, -1j*w0, 0, -1j*w0, 0, 0],
        [-t, B_0, 0,-1j*w0, -1j*w0,-1j*w0, 0,0, 0],
        [1j*w0, 0, B_1, 0, 0, -t,-t,-1j*w0, 0],
        [0, 1j*w0, 0, B_1, 0, -t,-t, 0, -1j*w0],
        [1j*w0, 1j*w0, 0, 0, B_1, J01, J01, -1j*w0, -1j*w0],
        [0, 1j*w0, -t, -t, J01,  B_1,J11, -1j*w0,0],
        [1j*w0, 0, -t, -t, J01, J11, B_1, 0,  -1j*w0],
        [0, 0, 1j*w0, 0, 1j*w0, 1j*w0, 0, B_2,-t],
        [0, 0, 0, 1j*w0, 1j*w0, 0, 1j*w0, -t,B_2]])
        self.Val_2=linalg.eig(matrix_H)
     #   print(np.round(self.Val_2[0],2))
     #   print(np.round(self.Val_2[1],2).T)
        sum_val=J01+J11+t

        if sum_val==0:
            self.Two_zero_ref_val=self.Val_1[0]
            self.Three_zero_ref_val=self.Val_2[0]
        self.get_unique_eigenstate()
        self.sort_eigen_value()
        self.coeff_2e()
        self.coeff_3e()
       # self.mag_phase_eigen_vector()
        
    def get_ref_val(self):
        return self.Two_zero_ref_val, self.Three_zero_ref_val

    def get_unique_eigenstate(self):
        eigen_value_arry=np.round(self.Val_1[0],15)
        eigen_vector_list=np.round(self.Val_1[1],15)
        values_, index_ = np.unique(eigen_value_arry, return_index=True)
        self.unique_eigen_states_2e=eigen_vector_list[index_]

        self.unique_eigen_states_len_2e=len(self.unique_eigen_states_2e)

        eigen_value_arry=np.round(self.Val_2[0],15)
        eigen_vector_list=np.round(self.Val_2[1],15)

        values_, index_ = np.unique(eigen_value_arry, return_index=True)

        self.unique_eigen_states_3e=eigen_vector_list[index_]
        self.unique_eigen_states_len_3e=len(self.unique_eigen_states_2e)

    def sort_eigen_value(self):
        bare_eignval=self.Val_1[0]
        bare_eignvec=self.Val_1[1]
        inde_arry=np.argsort(bare_eignval)
        self.order_eigen_vec_2e=np.round((bare_eignvec.T[inde_arry]),5)
        self.order_eigen_val_2e=np.round((bare_eignval[inde_arry]),5)
        self.unique_eigen_val_2e, self.eigen_degen_2e = np.unique(self.order_eigen_val_2e, return_counts=True)
        self.E_opt_1_2e=self.unique_eigen_val_2e[1]-self.unique_eigen_val_2e[0]
        self.binding_energy_2e=-self.E_opt_1_2e+self.w

        bare_eignval=self.Val_2[0]
        bare_eignvec=self.Val_2[1]
        inde_arry=np.argsort(bare_eignval)
        self.order_eigen_vec_3e=np.round((bare_eignvec.T[inde_arry]),5)
        self.order_eigen_val_3e=np.round((bare_eignval[inde_arry]),5)
        self.unique_eigen_val_3e, self.eigen_degen_3e = np.unique(self.order_eigen_val_3e, return_counts=True)
        self.E_opt_1_3e=self.unique_eigen_val_3e[1]-self.unique_eigen_val_3e[0]
        self.binding_energy_3e=-self.E_opt_1_3e+self.w

    def get_eigen_coeff(self,sort_eignvec,index):
        index_ = np.nonzero(sort_eignvec[index])

        return sort_eignvec[index][index_], index_
    def return_eigen_vec(self,index=0):
        return np.around(self.order_eigen_vec_2e,4)[index]
    def normalize(self,vec):
        return vec/np.sqrt(np.sum(vec**2))
    def general_first_excited_state_2e(self):
        Eig_1=self.return_eigen_vec(index=1)
        Eig_2=self.return_eigen_vec(index=2)
        #print( (Eig_1))
        #DSa=0.5*(Eig_1+Eig_2)/(Eig_1+Eig_2)[-2]
        DSa=self.normalize(Eig_1+Eig_2)

        #Vla=DSa[1:5]/(np.sqrt(2*np.sum(DSa[1:5]**2)))
        #DSa[1:5]=Vla
 
        
        Eig_1=self.return_eigen_vec(index=1)
        Eig_2=self.return_eigen_vec(index=2)
        #print((Eig_2))
        DSa=self.normalize(Eig_1-Eig_2)
         
       # print(DSa[1:5])
        
        #phi_1=np.arctan2(Vla[2].real,Vla[0].real)
        #phi_2=np.arctan2(Vla2[3].real,Vla2[1].real)
       # return phi_1,phi_2
    def get_first_two_eigen_info(self):
        info_vector=[self.w,self.w0,self.V00,self.V11,self.J01,self.J11]
        
        E_opt_1_2e=self.unique_eigen_val_2e[1]-self.unique_eigen_val_2e[0]
        E_opt_2_2e=self.unique_eigen_val_2e[2]-self.unique_eigen_val_2e[0]
        E_opt_1_3e=self.unique_eigen_val_3e[1]-self.unique_eigen_val_3e[0]
        E_opt_2_3e=self.unique_eigen_val_3e[2]-self.unique_eigen_val_3e[0]
        info_vector.append(E_opt_1_2e.real)
        info_vector.append(E_opt_2_2e.real)
        info_vector.append(E_opt_1_3e.real)
        info_vector.append(E_opt_2_3e.real)
 
        return info_vector
    def print_info_2e(self,print_=True,print_vector=True,print_coeff=True,bare_vec=True):
        if print_: 
            print('Two Electrons--------------')
            print('V00: '+str(np.around(self.V00,2)))
            print('V01: '+str(np.around(self.V01,2)))
            print('V11: '+str(np.around(self.V11,2)))
            print('J01: '+str(np.around(self.J01,2)))
            print('J11: '+str(np.around(self.J11,2)))
            print('t: '+str(np.around(self.t,2)))

            print(np.around(self.unique_eigen_val_2e,4))
            print(self.eigen_degen_2e)
            print('opt_gap')
            print(self.E_opt_1_2e)
            print('binding energy')
            print(self.binding_energy_2e)
            

        if print_vector:
            print('eigen_vectors')
            if bare_vec:
                print(np.around(self.order_eigen_vec_2e,4))
            else:
                print(self.mag_2e)
                print(self.phase_angle_2e)
            print('eigen_values')
            if bare_vec:
                print(np.around(self.order_eigen_val_2e,4))
            else:
                print(self.mag_2e_val)
                print(self.phase_angle_2e_val)

        if print_coeff:
            print('eigen_vector Coeff')
            print(self.coeff_2e)
            print('eigen_vector Index')
            print(self.coeff_index_2e)
    def mag_phase_eigen_vector(self):
        real_part=self.order_eigen_vec_2e.real
        imag_part=self.order_eigen_vec_2e.imag

        self.mag_2e=np.round(np.sqrt(real_part**2+imag_part**2),4)

        self.phase_angle_2e=np.round(np.arctan2(imag_part,real_part)/np.pi,4)

        real_part=self.order_eigen_val_2e.real
        imag_part=self.order_eigen_val_2e.imag

        self.mag_2e_val=np.round(np.sqrt(real_part**2+imag_part**2),4)
        self.phase_angle_2e_val=np.round(np.arctan2(imag_part,real_part)/np.pi,4)


        real_part=self.order_eigen_vec_3e.real
        imag_part=self.order_eigen_vec_3e.imag

        self.mag_3e=np.round(np.sqrt(real_part**2+imag_part**2),4)
        self.phase_angle_3e=np.round(np.arctan2(imag_part,real_part)/np.pi,4)

        real_part=self.order_eigen_val_3e.real
        imag_part=self.order_eigen_val_3e.imag

        self.mag_3e_val=np.round(np.sqrt(real_part**2+imag_part**2),4)
        self.phase_angle_3e_val=np.round(np.arctan2(imag_part,real_part)/np.pi,4)



    def print_info_3e(self,print_=True,print_vector=True,print_coeff=True,bare_vec=True):
        if print_: 
            print('Three Electrons--------------')
            print(np.around(self.unique_eigen_val_3e,2))
            print(self.eigen_degen_3e)
            print('opt_gap')
            print(self.E_opt_1_3e)
            print('binding energy')
            print(self.binding_energy_3e)
            
        if print_vector:
            print('eigen_vectors')
            if bare_vec:
                print(np.around(self.order_eigen_vec_3e,4))
            else:
                print(self.mag_3e)
                print(self.phase_angle_3e)
            print('eigen_values')
            if bare_vec:
                print(np.around(self.order_eigen_val_3e,4))
            else:
                print(self.mag_3e_val)
                print(self.phase_angle_3e_val)
        if print_coeff:
            print('eigen_vector Coeff')
            print(self.coeff_3e)
            print('eigen_vector Index')
            print(self.coeff_index_3e)
    
    def coeff_2e(self):
        order_size=len(self.order_eigen_vec_2e)
        self.coeff_2e={}
        self.coeff_index_2e={}
        for i in range(0,order_size):
            eigen_ary,eigen_inde=self.get_eigen_coeff(sort_eignvec=self.order_eigen_vec_2e,index=i)
            self.coeff_2e[str(i)]=eigen_ary
            self.coeff_index_2e[str(i)]=eigen_inde

    def eigen_val_2e(self,index):
        print( self.order_eigen_val_2e[index])
        return self.order_eigen_val_2e[index]
    def eigen_val_3e(self,index):
        print( self.order_eigen_val_3e[index])
        return self.order_eigen_val_3e[index]
    def coeff_3e(self):
        order_size=len(self.order_eigen_vec_3e)
        self.coeff_3e={}
        self.coeff_index_3e={}
        for i in range(0,order_size):
            eigen_ary,eigen_inde=self.get_eigen_coeff(sort_eignvec=self.order_eigen_vec_3e,index=i)
            self.coeff_3e[str(i)]=eigen_ary
            self.coeff_index_3e[str(i)]=eigen_inde
    
    def get_coeff_2e(self,index):
        print(self.coeff_2e[str(index)])
        print(self.coeff_index_2e[str(index)])
        return self.coeff_2e[str(index)],self.coeff_index_2e[str(index)]

    def get_coeff_3e(self,index):
        print(self.coeff_3e[str(index)])
        print(self.coeff_index_3e[str(index)])
        return self.coeff_3e[str(index)],self.coeff_index_3e[str(index)]
    
    def get_binding(self):
        return self.E_opt_1_2e, self.binding_energy_2e,self.E_opt_1_3e,self.binding_energy_3e
    def energy_level(self,low_energy_reso):
        eigen_degen_2e=self.eigen_degen_2e
        unique_eigen_val_2e=self.unique_eigen_val_2e
        diff_2e_val=np.abs(unique_eigen_val_2e[0:int(len(unique_eigen_val_2e[0::])-1)]-unique_eigen_val_2e[1::])
        val_2e_loc=(diff_2e_val<low_energy_reso)
        self.smooth_2e_val=[0]*eigen_degen_2e[0]
        for i in range(0,len(val_2e_loc)):
            if val_2e_loc[i]:
                state_next=[(unique_eigen_val_2e[i]-unique_eigen_val_2e[0])]*eigen_degen_2e[i+1]
                self.smooth_2e_val.extend(state_next)
            else: 
                state_next=[(unique_eigen_val_2e[i+1]-unique_eigen_val_2e[0])]*eigen_degen_2e[i+1]
                self.smooth_2e_val.extend(state_next)

        eigen_degen_3e=self.eigen_degen_3e
        unique_eigen_val_3e=self.unique_eigen_val_3e
        diff_3e_val=np.abs(unique_eigen_val_3e[0:int(len(unique_eigen_val_3e[0::])-1)]-unique_eigen_val_3e[1::])
        val_3e_loc=(diff_3e_val<low_energy_reso)
        self.smooth_3e_val=[0]*eigen_degen_3e[0]
        for i in range(0,len(val_3e_loc)):
            if val_3e_loc[i]:
                state_next=[(unique_eigen_val_3e[i]-unique_eigen_val_3e[0])]*eigen_degen_3e[i+1]
                self.smooth_3e_val.extend(state_next)
            else: 
                state_next=[(unique_eigen_val_3e[i+1]-unique_eigen_val_3e[0])]*eigen_degen_3e[i+1]
                self.smooth_3e_val.extend(state_next)

        return self.smooth_2e_val,self.smooth_3e_val


    def noise_enrich(self,gaussian_broadening=30,trial_run=1000):
        self.enriched_2e_val=np.zeros((trial_run,len(self.smooth_2e_val)))
        for i in range(0,trial_run):
            for j in range(0,len(self.smooth_2e_val)):
                current_noise_mean=self.smooth_2e_val[j]
                self.enriched_2e_val[i,j]=np.random.normal(current_noise_mean,gaussian_broadening,1)

        self.enriched_3e_val=np.zeros((trial_run,len(self.smooth_3e_val)))
        for i in range(0,trial_run):
            for j in range(0,len(self.smooth_3e_val)):
                current_noise_mean=self.smooth_3e_val[j]
                self.enriched_3e_val[i,j]=np.random.normal(current_noise_mean,gaussian_broadening,1)

    def gaussian(self,mean,x,std):
        return np.exp(-0.5*(x-mean)**2/(std**2))

    def gaussian_enrich(self,bin_array,gaussian_broadening=30):
        self.enriched_2e_val=np.zeros(len(bin_array))
        for j in range(0,len(self.smooth_2e_val)):
            current_noise_mean=self.smooth_2e_val[j]
            self.enriched_2e_val=self.enriched_2e_val+self.gaussian(current_noise_mean,bin_array,gaussian_broadening)

        self.enriched_3e_val=np.zeros(len(bin_array))
        for j in range(0,len(self.smooth_3e_val)):
            current_noise_mean=self.smooth_3e_val[j]
            self.enriched_3e_val=self.enriched_3e_val+self.gaussian(current_noise_mean,bin_array,gaussian_broadening)
        return self.enriched_2e_val, self.enriched_3e_val
    def energy_gaussian(self,bin_density=100,gaussian_broadening=100):
        bin_size=np.linspace(-0.5*self.w,3.5*self.w, bin_density) 
        enriched_hist_2e,enriched_hist_3e=self.gaussian_enrich(bin_array=bin_size,gaussian_broadening=gaussian_broadening)

        return enriched_hist_2e,enriched_hist_3e,bin_size

    def energy_hist_info(self,bin_density=100,gaussian_broadening=100,trial_run=1000):
        bin_size=np.linspace(-0.5*self.w,2.5*self.w, bin_density) 
        self.noise_enrich(gaussian_broadening=gaussian_broadening,trial_run=trial_run)
        #self.gaussian_enrich(bin_array=bin_size,gaussian_broadening=gaussian_broadening)

        (full_hist, bins2, patches)=plt.hist(self.enriched_2e_val, bins=bin_size)
        enriched_hist_2e=np.sum(full_hist.T,axis=1)

        bin_size=np.linspace(-0.5*self.w,2.5*self.w, bin_density)#np.arange(-10*binwidth, 2*self.w+10*binwidth, binwidth)
        (full_hist, bins2, patches)=plt.hist(self.enriched_3e_val, bins=bin_size)
        enriched_hist_3e=np.sum(full_hist.T,axis=1)
        print(bin_size)
        print(bins2)

        return enriched_hist_2e,enriched_hist_3e,bins2
 

        