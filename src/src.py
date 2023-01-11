import numpy as np
from scipy import linalg
import seaborn as sns
import os 
import string 
import shutil
import matplotlib.pyplot as plt
import os
import cv2 
from scipy.interpolate import make_interp_spline, BSpline
from scipy.interpolate import griddata

class Data_process:
    ''' Process the gmesh file into data array, and export into a .dat format'''
    def __init__(self,row_num=2,column_num=2,root_dir='../cache/data',width=30,height=30,letter=True):
        self.fig = plt.figure()
        self.fig.suptitle('')
        self.fig.set_figheight(height)
        self.fig.set_figwidth(width)
        self.row_num=row_num
        self.column_num=column_num
        self.total_num=row_num*column_num
        self.axes={"total_num":self.total_num}
        self.root_dir=root_dir
        self.lc_string='abcdefghijklmnopqrstuvwxyz'
        self.fig.tight_layout()

        for i in range(1,self.total_num+1):
            current_plot_num=int(str(self.row_num)+str(self.column_num)+str(i))
           # print(i)
            self.axes[str(i)] = self.fig.add_subplot(self.row_num, self.column_num,i)
 
            #self.axes[str(i)].set_xlabel('x (xi)')
            #self.axes[str(i)].set_ylabel('y (xi)') 
            #self.axes[str(i)].set_xlim(self.min_array[0],self.max_array[0] )
            #self.axes[str(i)].set_ylim(self.min_array[1],self.max_array[1] )
            #self.axes[str(i)].set_zlim(self.min_array[2],self.max_array[2] )

            #self.axes[str(i)].set_xlim(min_x,max_x)
            #self.axes[str(i)].set_ylim(min_x,max_x )
            #self.axes[str(i)].set_aspect('auto')
            self.axes[str(i)].set_aspect('auto')
            if letter:
                self.axes[str(i)].text(-0.1, 1.1, string.ascii_uppercase[int(i-1)]+')', transform=self.axes[str(i)].transAxes, 
                        size=8, weight='bold')


        #self.mesh_cood=np.array([full_mesh_cood,def_loc_mesh,Dir_mesh],dtype='object') # 0 is the inner region and 1 is the side region

    def red_csv(self,csv_path,sub_path_loc='/raw_data'):
        #sub_path_loc='/phase_raw_data'
        cur_root=self.root_dir+sub_path_loc
        
        csv_data = np.genfromtxt(cur_root+csv_path, delimiter=',')

        return csv_data


    def fig_title(self,fig_name='',title_size=30):
        self.fig.suptitle(fig_name,fontsize=title_size)
    
    def fig_caption(self,txt=''):
        self.fig.text(0.5, 0.01, txt, wrap=True, horizontalalignment='center', fontsize=25)



    def rebuild_dir(self,file_loc='/name'):
        try:
            os.mkdir(file_loc)
        except:
            shutil.rmtree(file_loc)
            os.mkdir(file_loc)

    def add_subplot_axes(self,ax,rect=[0.7,0.7,0.3,0.3],axisbg='black',axis_on=True,bg_off=False,grid_in=True):
        fig = plt.gcf()
        box = ax.get_position()
        width = box.width
        height = box.height
        inax_position  = ax.transAxes.transform(rect[0:2])
        transFigure = fig.transFigure.inverted()
        infig_position = transFigure.transform(inax_position)    
        x = infig_position[0]
        y = infig_position[1]
        width *= rect[2]
        height *= rect[3]  # <= Typo was here
        #subax = fig.add_axes([x,y,width,height],facecolor=facecolor)  # matplotlib 2.0+

        subax = fig.add_axes([x,y,width,height],facecolor=axisbg)
        if axis_on:
            x_labelsize = subax.get_xticklabels()[0].get_size()
            y_labelsize = subax.get_yticklabels()[0].get_size()
            x_labelsize *= rect[2]**0.5
            y_labelsize *= rect[3]**0.5
            subax.xaxis.set_tick_params(labelsize=x_labelsize)
            subax.yaxis.set_tick_params(labelsize=y_labelsize)
            subax.xaxis.set_tick_params(labelsize=x_labelsize)
        else:
            pass
        if bg_off:
            subax.grid(False)
            #plt.axis('off')
            subax.set_xticks([])
            subax.set_yticks([])
            subax.set(facecolor = "white")
            #subax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
            #subax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
            #subax.w_xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
            #subax.w_yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))

        if grid_in:
            return subax
        else:
            return np.array([subax])
    def add_subsub_plot(self,plot_index,rect=[0.7,0.7,0.3,0.3],axisbg='white',axis_on=True,bg_off=False,grid_in=True):
        ax_1= self.axes[str(plot_index)]
        sub_axis1=self.add_subplot_axes(ax=ax_1,rect=rect,axisbg=axisbg,axis_on=axis_on,bg_off=bg_off,grid_in=True)
        return sub_axis1

    # Save with alpha
        Image.fromarray(npImage).save(out_path)
    def append_subsub_axis(self,axis):
        tot_axis_len=len(self.axes)
        self.axes[str(tot_axis_len)]=axis
        return tot_axis_len

    def add_subplot_sub_grid(self,plot_index,size_x=2,size_y=2):
        ax_1= self.axes[str(plot_index)]
        size_inv_x=1/size_x
        size_inv_y=1/size_y
        sub_axis_arry=[]
        sub_axis_arry_index=[]
        for i in range(0,size_x):

            for j in range(0,size_y):
                print(i*size_inv_x)
                print(size_inv_y)
                subax=self.add_subplot_axes(ax=ax_1,rect=[i*size_inv_x,j*size_inv_y,size_inv_x,size_inv_y],axisbg='white',axis_on=False,bg_off=True)
                sub_axis_arry_index.append(len(self.axes))
                sub_axis_arry.append(subax)
                self.axes[str(len(self.axes))]=subax
                #self.axes.append(subax)
        return sub_axis_arry,sub_axis_arry_index

    def add_subplot_sub_non_uniform_grid_row(self,plot_index,size_x_array=[2,2],y_ratio_array=[0,0.6,0.4]):
        # size_x_array indicates the number of axis in each row, and y_ratio_array represents the size_ratio between each row (the ratio array should sum to 1, first term must be 0)
        ax_1= self.axes[str(plot_index)]
        self.axis_off(plot_index=plot_index)
        size_y=len(size_x_array)
        sub_axis_arry=[]
        sub_axis_arry_index=[]
        current_y_loc=0
        for j in range(0,size_y):
            size_x=size_x_array[j]
            size_inv_x=1/size_x
            current_y_loc=current_y_loc+y_ratio_array[j]
            for i in range(0,size_x):
              #  print(i*size_inv_x)
                subax=self.add_subplot_axes(ax=ax_1,rect=[i*size_inv_x,current_y_loc,size_inv_x,y_ratio_array[j+1]],axisbg='white',axis_on=False,bg_off=False)
                sub_axis_arry_index.append(len(self.axes))
                sub_axis_arry.append(subax)
                self.axes[str(len(self.axes))]=subax
        for i in range(len(sub_axis_arry_index)):
            self.axis_off(plot_index=sub_axis_arry_index[i])
                #self.axes.append(subax)
        return sub_axis_arry,sub_axis_arry_index


    def add_subplot_sub_non_uniform_grid_column(self,plot_index,size_y_array=[2,2],x_ratio_array=[0,0.6,0.4]):
        # size_x_array indicates the number of axis in each row, and y_ratio_array represents the size_ratio between each row (the ratio array should sum to 1, first term must be 0)
        ax_1= self.axes[str(plot_index)]
        size_y=len(size_y_array)
        sub_axis_arry=[]
        sub_axis_arry_index=[]
        current_y_loc=0
        for j in range(0,size_y):
            size_x=size_y_array[j]
            size_inv_x=1/size_x
            current_y_loc=current_y_loc+x_ratio_array[j]
            for i in range(0,size_x):
                print(i*size_inv_x)
                subax=self.add_subplot_axes(ax=ax_1,rect=[current_y_loc,i*size_inv_x,x_ratio_array[j+1],size_inv_x],axisbg='white',axis_on=False,bg_off=False)
                sub_axis_arry_index.append(len(self.axes))
                sub_axis_arry.append(subax)
                self.axes[str(len(self.axes))]=subax
                #self.axes.append(subax)
        return sub_axis_arry,sub_axis_arry_index



 
    def sline(self,plot_index,x_arry,y_arry1,y_arry2, color='blue',log_scale_x=False,log_scale_y=False,alpha=0.1):
        x_arry_arg=np.argsort(x_arry)
        x_arry=np.sort(x_arry)
        y_arry1=y_arry1[x_arry_arg]
        y_arry2=y_arry2[x_arry_arg]
        xnew = np.linspace(x_arry[0],x_arry[-1],200)       
       # tck1 = sp.interpolate.splrep(x_arry, y_arry1, s=0)
       # tck2 = sp.interpolate.splrep(x_arry, y_arry2, s=0)
       # ynew1= sp.interpolate.splev(xnew, tck1, der=0)
       # ynew2= sp.interpolate.splev(xnew, tck2, der=0)
        ynew=np.interp(xnew, x_arry, y_arry1)
        ynew2=np.interp(xnew, x_arry, y_arry2)
        #f1 =  UnivariateSpline(x_arry, y_arry1, k = 5)
        #f2 = UnivariateSpline(x_arry, y_arry2, k = 5)

        ax_1= self.axes[str(plot_index)]
        ax_1.plot(xnew,ynew,color=color, alpha=alpha)
        ax_1.plot(xnew,ynew2,color=color, alpha=alpha)


        ax_1.fill_between(xnew, ynew, ynew2, color=color, alpha=alpha)

        if log_scale_y:
            ax_1.set_yscale('log')
        if log_scale_x:
            ax_1.set_xscale('log')
    def add_arrow(self,plot_index,start_point=[0,0],end_point=[1,1],log_scale_x=False,log_scale_y=False,color="black",alpha=1):
        ax_1= self.axes[str(plot_index)]
        style = "Simple, tail_width=2, head_width=4, head_length=2"
        kw = dict(arrowstyle=style, color=color,alpha=alpha)

        a = patches.FancyArrowPatch((start_point[0], start_point[1]), (end_point[0], end_point[1]), **kw)
        ax_1.add_patch(a)
        if log_scale_y:
            ax_1.set_yscale('log')
        if log_scale_x:
            ax_1.set_xscale('log')

    def add_line(self,plot_index,start_point=[0,0],end_point=[1,1],log_scale_x=False,log_scale_y=False,color="black",alpha=1):
        ax_1= self.axes[str(plot_index)]
        style = "Simple, tail_width=2, head_width=2, head_length=0.1"
        kw = dict(arrowstyle=style, color=color,alpha=alpha)

        a = patches.FancyArrowPatch((start_point[0], start_point[1]), (end_point[0], end_point[1]), **kw)
        ax_1.add_patch(a)
        if log_scale_y:
            ax_1.set_yscale('log')
        if log_scale_x:
            ax_1.set_xscale('log')

    def grid(self,plot_index):
        ax_1= self.axes[str(plot_index)]
        ax_1.grid()

    def simple_poly_fit(self,degree,log_axis,plot_index,x_arry,y_arry,log_scale=True,label=False,log_x=True):
        ax_1= self.axes[str(plot_index)]
        parameter_list=[]


        c_arry=y_arry 
        arry_=x_arry 

        x_=np.linspace(min(arry_),max(arry_),100)
        if log_axis:
            arry_=np.log(arry_)
            
            c_arry=np.log(c_arry)
            if log_x==False:
                arry_=x_arry
    
        poly_ceff=np.polyfit(arry_,c_arry,degree)
        poly= np.poly1d(poly_ceff)
        parameter_list.append(poly_ceff)

        if log_axis:
            y_ = lambda x: np.exp(poly(np.log(x)))
            if log_x==False:
                y_ = lambda x: np.exp(poly(x))
            curr_plot=ax_1.plot(x_,y_(x_) ,zorder=1 ,label=('power/coeff: '+str(round(poly_ceff[0],2))+'/'+str(round(np.exp(poly_ceff[1]),2)))) 

        else:
            y_=poly_ceff[0]*x_+poly_ceff[1]
            curr_plot=ax_1.plot(x_,y_,zorder=1 ,label=('power/coeff: '+str(round(poly_ceff[0],2))+'/'+str(round(poly_ceff[1],2)))) 


            
        if log_scale:
            ax_1.set_yscale('log')
            ax_1.set_xscale('log')
        print('Done')
    
        if label:
            ax_1.legend(loc='upper right', bbox_to_anchor=(1, 1))
            
            return np.array(parameter_list)
    def show_legend(self,plot_index,loc='upper left', bbox_to_anchor=(0, 1),fontsize=10):
        ax_1= self.axes[str(plot_index)]
        ax_1.legend( loc=loc, bbox_to_anchor=bbox_to_anchor,fontsize=fontsize)



    def set_x_range(self,plot_index,x_range=[0,1]):
        ax_1= self.axes[str(plot_index)]
        ax_1.set_xlim([x_range[0], x_range[1]])


    def set_y_range(self,plot_index,y_range=[0,1]):
        ax_1= self.axes[str(plot_index)]
        ax_1.set_ylim([y_range[0], y_range[1]])


    def line(self,plot_index,x,y,log_axis=True):
        ax_1= self.axes[str(plot_index)]
        ax_1.plot(x,y)
        if log_axis:
            ax_1.set_yscale('log')
            ax_1.set_xscale('log')
        
    def hline(self,plot_index,y0,x_min,x_max,color='red',linewidth=2,alpha=0.6):
        x=np.linspace(x_min,x_max,500)
        y0=y0*np.ones(x.shape)
        ax_1= self.axes[str(plot_index)]
        ax_1.plot(x,y0,'--',linewidth=linewidth,color=color,alpha=alpha)

    def vline(self,plot_index,x0,y_min,y_max,color='red',linewidth=2,alpha=0.6):
        y=np.linspace(y_min,y_max,100)
        x0=x0*np.ones(y.shape)
        ax_1= self.axes[str(plot_index)]
        ax_1.scatter(x0,y,marker='s',s=linewidth,color=color,alpha=alpha)
    def add_text(self,plot_index,x,y,s,bg_color='white',fontsize=20, alpha=0.5):
        ax_1= self.axes[str(plot_index)]
        ax_1.text(x, y, s, bbox=dict(facecolor=bg_color, alpha=alpha,edgecolor='none'), fontsize=fontsize)

    def add_title(self,plot_index=1,title_name='Test',fontsize=20):
        ax_1= self.axes[str(plot_index)]
        ax_1.set_title(title_name, fontsize=fontsize)

    def add_axis_label(self,plot_index=1,x_axis_name='Test',y_axis_name='Test',x_label_loc=0,y_label_loc=0,x_axis_range=[0],y_axis_range=[0],fontsize=8,rotation_x=0,rotation_y=0):
        ax_1= self.axes[str(plot_index)]
        #ax_1.set_title(title_name, fontsize=fontsize)

        ax_1.set_xlabel(x_axis_name,fontsize=fontsize, rotation=rotation_x,labelpad=x_label_loc)
        #ax_1.set_ylabel(y_axis_name,rotation='horizontal',fontsize=fontsize)
        ax_1.set_ylabel(y_axis_name,fontsize=fontsize, rotation=rotation_y, ha='right',labelpad=y_label_loc)
        if len(x_axis_range)>1:
            ax_1.set_xlim(x_axis_range[0],x_axis_range[1])
        if len(y_axis_range)>1:
            ax_1.set_ylim(y_axis_range[0],y_axis_range[1])

    def tick_size(self,plot_index=1,fontsize=20):
        ax_1= self.axes[str(plot_index)]
        ax_1.tick_params(axis='both', which='major', labelsize=fontsize)
        ax_1.tick_params(axis='both', which='minor', labelsize=fontsize)

    def xtick_rotate(self,plot_index=1, rotation=-45, ha="left"):
        ax_1= self.axes[str(plot_index)]
        plt.setp( ax_1.xaxis.get_majorticklabels(), rotation=rotation, ha=ha )


    def move_y_ticks(self,plot_index=1,position='right'):
        ax_1= self.axes[str(plot_index)]
        if position=='right':
            ax_1.yaxis.tick_right()
 
        else:
            ax_1.yaxis.tick_left()  

    def remove_x_ticks(self,plot_index=1):
        ax_1= self.axes[str(plot_index)]
        ax_1.set_xticks([])
    def remove_y_ticks(self,plot_index=1):
        ax_1= self.axes[str(plot_index)]
        ax_1.set_yticks([])

    def move_x_ticks(self,plot_index=1,position='bottom'):
        ax_1= self.axes[str(plot_index)]
        if position=='bottom':
            ax_1.xaxis.tick_bottom ()
 
        else:
            ax_1.xaxis.tick_top()  

    def img_show(self,img,sub_axis,sub_ax_loc=1,main_ax=False,axpect='auto'):
        if main_ax:
            ax_1= self.axes[str(sub_axis)]
        else:
            ax_1= sub_axis[sub_ax_loc]
        ax_1.imshow(img, interpolation='nearest', aspect=axpect)
        ax_1.axis('off')
        ax_1.grid(False)
        #plt.axis('off')
        ax_1.set_xticks([])
        ax_1.set_yticks([])
        #ax_1.set(facecolor = "white")
       # ax_1.set_facecolor('pink')
    def axis_off(self,plot_index):
        ax_1= self.axes[str(plot_index)]
       # ax_1.axis('off')
        ax_1.grid(False)
        #plt.axis('off')
        ax_1.set_xticks([])
        ax_1.set_yticks([])


        #ax_1.set(facecolor = "white")
    def fig_size(self,w,h):
        self.fig.set_size_inches(w, h)


    def save_fig(self,sub_path_loc,dpi_num,name,svg=False):
        try:
            cur_root=self.root_dir+sub_path_loc
            if svg:
                plt.savefig(cur_root+'/'+name+'.svg', dpi=dpi_num)
            else:
                plt.savefig(cur_root+'/'+name+'.png', dpi=dpi_num)
            plt.close()
        except: 
            
            #self.rebuild_dir(sub_path_loc)
            cur_root=self.root_dir+sub_path_loc
            try:
                os.mkdir(cur_root)
            except:
                pass
            if svg:
                plt.savefig(cur_root+'/'+name+'.svg', dpi=dpi_num)
            else:
                plt.savefig(cur_root+'/'+name+'.png', dpi=dpi_num)
            plt.close()

    def close_fig(self):
        plt.close()
    
    def videos(self,img_loc,out_loc,out_file_name,N=100):
        img_array=[]
        for i in range(0,N):
            fig_loc=img_loc+'/'+str(i)+'.png'
            img = cv2.imread(fig_loc)
            print(img.shape)
            height, width, layers = img.shape
            size = (width,height)
            img_array.append(img)
        print(img_array)

        out = cv2.VideoWriter(out_loc+out_file_name,cv2.VideoWriter_fourcc(*'DIVX'), 10, size)

        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
                

    def heat_map(self,plot_index,Map_arry,x_ticks=[],y_ticks=[]):
        ax1= self.axes[str(plot_index)]
        hm=sns.heatmap(Map_arry,ax=ax1, linewidth=0, cbar=True,alpha=1)
        ax1.set_xticks(range(0,100,10))
        ax1.set_yticks(range(0,100,10))
        ax1.set(xticklabels=np.round(x_ticks[::10],2))
        ax1.set(yticklabels=np.round(y_ticks[::10],2))
        ax1.xaxis.set_tick_params(labeltop=True)
        ax1.xaxis.tick_top()
        ax1.xaxis.set_label_position('top') 
        
    def p_plot(self,plot_index,x,y,cl,cbar_label='',vmin=0,vmax=1,type=0,cbar_=True):#  orientation=, anchor=(0, 0.3), shrink=0.7, pad=0.2,cbar_label=''
        ax1= self.axes[str(plot_index)]
        x_gr,y_gr=np.meshgrid(x,y)
 #, 
        if type==2:
            ax1.set_xticks([0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5], minor=False)
            ax1.xaxis.grid(True, color ="black",zorder=10)
        elif type==3:
            ax1.set_xticks([0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5], minor=False)
            ax1.xaxis.grid(True, color ="black",zorder=10)
        else: 
            pass 

        if vmax==vmin:
            pos=ax1.pcolormesh(x_gr, y_gr, cl, cmap ='GnBu',shading='auto',alpha=1)

        else:
            pos=ax1.pcolormesh(x_gr, y_gr, cl, cmap ='GnBu',shading='auto',alpha=1,vmin=vmin, vmax=vmax)

        if cbar_:
            cbar=self.fig.colorbar(pos,ax=ax1)
            cbar.ax.tick_params(labelsize=8)
            cbar.ax.xaxis.set_ticks_position("top")
            cbar.ax.set_title(cbar_label,fontsize=8)
        
    #def hist_plot(self,plot_index,cl)


    def add_x_ticks(self,plot_index,x_ticks_range=[],density=25):
        ax1= self.axes[str(plot_index)]
        ax1.set_xticks(x_ticks_range[::density])
        ax1.set(xticklabels=np.round(x_ticks_range[::density],1))
    #    ax1.xaxis.set_tick_params(labeltop=True)
    #    ax1.xaxis.tick_top()
        ax1.grid('on')

        #ax1.set_yticks(x_ticks_range[::density])
        #ax1.yaxis.grid(True)
        #plt.grid(True)
        ax1.xaxis.set_label_position('bottom') 
        #ax1.xaxis.grid(True)

    def simple_scatter(self,plot_index,x_arry,y_arry,color_t='red',marker='s',log_scale_x=True,log_scale_y=True,label_name=' ',twinx=False,alpha=0.1,add_line=False,s=20,cbar_label='',cbar_=True,color_range=[0]):
        ax_1= self.axes[str(plot_index)]
        if color_range[0]==0:
            pos=ax_1.scatter(x_arry,y_arry, s=s, c=color_t, marker=marker,cmap='RdBu',zorder=1,label=label_name,alpha=alpha  )
        else:
            pos=ax_1.scatter(x_arry,y_arry, s=s, c=color_t, marker=marker,cmap='RdBu',zorder=1,label=label_name,alpha=alpha , vmin=color_range[0], vmax=color_range[1] )
        if add_line:
            ax_1.plot(x_arry,y_arry, c=color_t,zorder=1,alpha=alpha  )

        if log_scale_y:
            ax_1.set_yscale('log')
        if log_scale_x:
            ax_1.set_xscale('log')
        #ax_1.legend(loc='upper right', bbox_to_anchor=(1, 1))
        if cbar_:
            cbar=self.fig.colorbar(pos,ax=ax_1)
            cbar.ax.tick_params(labelsize=8)
            cbar.ax.xaxis.set_ticks_position("top")
            cbar.ax.set_title(cbar_label,fontsize=8)
    def simple_plot(self,plot_index,x_arry,y_arry,color_t='red',log_scale_x=True,log_scale_y=True,label_name=' ',alpha=0.1,lw=1):
        ax_1= self.axes[str(plot_index)]
        ax_1.plot(x_arry,y_arry,   c=color_t ,zorder=5,label=label_name,alpha=alpha, linestyle='dashed',lw=lw  )
  
        if log_scale_y:
            ax_1.set_yscale('log')
        if log_scale_x:
            ax_1.set_xscale('log')
        #ax_1.legend(loc='upper right', bbox_to_anchor=(1, 1))
 
    def simple_contour(self,plot_index,x_arry,y_arry,z_arry,color_t='red',log_scale_x=True,log_scale_y=True,label_name=' ',alpha=0.1,lw=1,num_of_levels=10):
        ax_1= self.axes[str(plot_index)]
        CS=ax_1.contour(x_arry,y_arry,z_arry,levels=num_of_levels,linewidths=lw,colors=color_t,linestyle='dashed',alpha=alpha,label=label_name)
        if log_scale_y:
            ax_1.set_yscale('log')
        if log_scale_x:
            ax_1.set_xscale('log')
        #plt.clabel(CS, inline=1, fontsize=10)


    def simple_contour_color(self,plot_index,x_arry,y_arry,z_arry,log_scale_x=True,log_scale_y=True,alpha=0.1,cbar_=True,cmap=10,cbar_label='',color_range=[0]):
        ax_1= self.axes[str(plot_index)]
        if color_range[0]==0:
            pos=ax_1.contourf(x_arry,y_arry,z_arry,cmap=cmap,alpha=alpha,levels=550)
        else:
            pos=ax_1.contourf(x_arry,y_arry,z_arry,cmap=cmap,alpha=alpha, vmin=color_range[0], vmax=color_range[1],levels=150)


        if log_scale_y:
            ax_1.set_yscale('log')
        if log_scale_x:
            ax_1.set_xscale('log')
        if cbar_:
            cbar=self.fig.colorbar(pos,ax=ax_1)
            cbar.ax.tick_params(labelsize=8)
            cbar.ax.xaxis.set_ticks_position("top")
            cbar.ax.set_title(cbar_label,fontsize=8)