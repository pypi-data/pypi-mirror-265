# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 19:06:49 2023

@author: Hedi
"""

from . import*
import time
from numpy import exp,linspace,concatenate,array,reshape,split,zeros,vectorize,linspace,absolute,argwhere,insert
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve


class res_membrane:
    @property
    def Vr_out(self):
        return self.Vr[-1]
    @property
    def Vp_out(self):
        return self.Vp[-1]
    @property
    def Cr_out(self):
        return self.Cr[:,-1]
    @property
    def Cp_out(self):
        return self.Cp[:,-1]
    @property
    def net_balance(self):
        return self.parent.Vin-self.Vr_out-self.Vp_out
    @property
    def solute_net_balance(self):
        return array(self.parent.Cin)*self.parent.Vin-self.Cp[:,-1]*self.Vp[-1]-self.Cr[:,-1]*self.Vr[-1]
    @property
    def FRV(self):
        return self.parent.Vin/self.Vr
    @property
    def T(self):
        return self.Cp/self.Cr
    @property
    def R(self):
        return 1 - self.T
    @property
    def FRV_out(self):
        return self.FRV[-1]
    @property
    def T_out(self):
        return self.T[:,-1]
    @property
    def R_out(self):
        return self.R[:,-1]
    
class dwsim:
    def __init__(self,parent,**args):
        self.parent=parent
        for k,v in parent.schema.dwsim.__dict__.items():
            setattr(self,k,v)
        for k,v in args.items():
            if k in list(self.__dict__.keys()):
                setattr(self, k, v)
        if self.feed:
            parent.T=self.feed.GetTemperature()-273.15
            parent.Pin=self.feed.GetPressure()/1e5
            parent.Vin=self.feed.GetVolumetricFlow()*3600
            solutes=[]
            Cin=[]
            for i,s in enumerate(self.feed.ComponentIds): 
                if s!="Water":
                    solutes.append(s)
                    Cin.append(self.feed.GetOverallComposition()[i]/self.feed.GetOverallMolecularWeight()*1e6)
            parent.solutes=solutes
            parent.Cin=Cin
    def print(self, Flowsheet,sheetname):
        Spreadsheet = Flowsheet.FormSpreadsheet
        ws = Spreadsheet.Spreadsheet.GetWorksheetByName(sheetname)
        if ws is None:
            ws = Spreadsheet.NewWorksheet(sheetname)
        ws.Reset()
        ws.Cells[0,0].Data="Position [m]"
        ws.Cells[0,1].Data="FRV"
        ws.Cells[0,2].Data="Vp [m3/h]"
        ws.Cells[0,3].Data="Vr [m3/h]"
        ws.Cells[0,4].Data="P [bar]"
        ws.Cells[0,5].Data="Jw [m3/h/m2]"
        i=6
        for j in range(len(self.parent.solutes)):
            ws.Cells[0,i+j].Data= self.parent.solutes[j]+"_ret [mol/m3]"
        i+=len(self.parent.solutes)
        for j in range(len(self.parent.solutes)):
            ws.Cells[0,i+j].Data= self.parent.solutes[j]+"_ret [mol/m3]"
        i+=len(self.parent.solutes)
        for j in range(len(self.parent.solutes)):
            ws.Cells[0,i+j].Data= self.parent.solutes[j]+"_mem [mol/m3]"
        i+=len(self.parent.solutes)
        for j in range(len(self.parent.solutes)):
            ws.Cells[0,i+j].Data= self.parent.solutes[j]+"_PIm [bar]"
        i+=len(self.parent.solutes)
        for j in range(len(self.parent.solutes)):
            ws.Cells[0,i+j].Data= self.parent.solutes[j]+"_PIp [bar]"
        i+=len(self.parent.solutes)
        for j in range(len(self.parent.solutes)):
            ws.Cells[0,i+j].Data= self.parent.solutes[j]+"_Delta PI [bar]"
        for i,x in enumerate(self.parent.res.x):
            ws.Cells[i+1,0].Data=float("{:.2f}".format(x))
            ws.Cells[i+1,1].Data=float("{:.2f}".format(self.parent.res.FRV[i]))  
            ws.Cells[i+1,2].Data=float("{:.3f}".format(self.parent.res.Vr[i]))  
            ws.Cells[i+1,3].Data=float("{:.3f}".format(self.parent.res.Vp[i]))  
            ws.Cells[i+1,4].Data=float("{:.3f}".format(self.parent.res.p[i])) 
            ws.Cells[i+1,5].Data=float("{:.3E}".format(self.parent.res.Jw[i])) 
            j=6
            for k in range(len(self.parent.solutes)):
                ws.Cells[i+1,j+k].Data= float("{:.3E}".format(self.parent.res.Cr[k,i]))
            j+=len(self.parent.solutes)
            for k in range(len(self.parent.solutes)):
                ws.Cells[i+1,j+k].Data= float("{:.3E}".format(self.parent.res.Cp[k,i]))
            j+=len(self.parent.solutes)
            for k in range(len(self.parent.solutes)):
                ws.Cells[i+1,j+k].Data= float("{:.3E}".format(self.parent.res.Cm[k,i]))
            j+=len(self.parent.solutes)
            for k in range(len(self.parent.solutes)):
                ws.Cells[i+1,j+k].Data= float("{:.3E}".format(self.parent.res.PIm[k,i]))
            j+=len(self.parent.solutes)
            for k in range(len(self.parent.solutes)):
                ws.Cells[i+1,j+k].Data= float("{:.3E}".format(self.parent.res.PIp[k,i]))
            j+=len(self.parent.solutes)
            for k in range(len(self.parent.solutes)):
                ws.Cells[i+1,j+k].Data= float("{:.3E}".format(self.parent.res.PI[k,i]))
    def refresh(self):
        if(self.feed and self.ret and self.per):
            self.ret.Clear()
            self.per.Clear()
            self.ret.SetTemperature(self.feed.GetTemperature())
            self.per.SetTemperature(self.feed.GetTemperature())
            self.ret.SetPressure(self.feed.GetPressure()-self.parent.DP*1e5)
            self.per.SetPressure(self.parent.Patm*1e5)
            water_index = argwhere(array(self.feed.ComponentIds)=="Water")[0]
            ret_mass_flow = self.parent.res.Cr_out/1e6
            ret_mass_flow = insert(ret_mass_flow,water_index,1-ret_mass_flow.sum())
            per_mass_flow = self.parent.res.Cp_out/1e6
            per_mass_flow = insert(per_mass_flow,water_index,1-per_mass_flow.sum())
            for i in range(len(self.feed.ComponentIds)):
                self.ret.SetOverallCompoundMassFlow(i,float(ret_mass_flow[i]*self.parent.res.Vr_out*1000/3600))
                self.per.SetOverallCompoundMassFlow(i,float(per_mass_flow[i]*self.parent.res.Vp_out*1000/3600))

class spiral_membrane(cf.__obj__):
    def __init__(self,**args):
        super().__init__(res_membrane)
        self.dwsim=None
        self.__R__ = 8.314 # J/mol/K
        for k,v in args.items():
            if k in list(self.__dict__.keys()):
                setattr(self, k, v)
            if k=="dwsim":
                self.dwsim=dwsim(self, **v)

    def calcul(self,):
        st = time.process_time()
        Cin,Vin,B=self.Cin,self.Vin,self.B
        #T=self.T+273.15
        α=self.S/self.L
        DPL=self.DP/self.L
        n_solutes = Cin.shape[0]
        def sysdiff(t,y):
            p,Vp,Vr,VCp,VCr=*y[0:3],*split(y[3:],2)
            dpdx=-DPL
            Cr=VCr/Vr
            if Vp:
                Cp=VCp/Vp
            else:
                Cp=zeros(n_solutes)
            
            Cm,Jw, = self.mass_layer(p,Cp,Cr,diffusion=t)[0:2]
            dVpdx=Jw*α
            dVrdx=-dVpdx
            dCpdx=B*(Cm-Cp)*α
            dCrdx=-dCpdx
            return concatenate(([dpdx,dVpdx,dVrdx],dCpdx,dCrdx))
        self.res.x=linspace(0,self.L,100)
        sol = solve_ivp(sysdiff, (0,self.L),
                          concatenate(([self.Pin,0.0,Vin],[0]*n_solutes,Vin*Cin)),
                          method="BDF",t_eval=self.res.x )   
        self.res.p,self.res.Vp,self.res.Vr,Cp,Cr=*sol.y[0:3],*split(sol.y[3:],2)
        self.res.Cr=Cr/self.res.Vr
        self.res.Cp=Cp
        self.res.Cp[:,1:]=self.res.Cp[:,1:]/self.res.Vp[1:]
        self.res.Cm=zeros(self.res.Cp.shape)
        self.res.Jw=zeros(self.res.Cp.shape[1])
        self.res.PI=zeros(self.res.Cp.shape)
        self.res.PIm=zeros(self.res.Cp.shape)
        self.res.PIp=zeros(self.res.Cp.shape)
        for i in range(self.res.x.shape[0]):
            self.res.Cm[:,i],self.res.Jw[i],self.res.PIm[:,i],self.res.PIp[:,i],self.res.PI[:,i], = self.mass_layer(self.res.p[i],self.res.Cp[:,i],self.res.Cr[:,i],diffusion=i)
        self.res.calculation_time = time.process_time()-st
        
        if self.dwsim:
            self.dwsim.refresh()
        


    def mass_layer(self,p,Cp,Cr,diffusion=False):
        k=array(self.k)
        T=self.T+273.15
        PIp=self.__R__*T*1e-5*Cp # bar
        if diffusion:
            def fm(c):
                PIm=self.__R__*T*1e-5*c # bar
                DPi=PIm-PIp
                Jw=(p-self.Patm-DPi.sum())*self.Aw
                return abs(c-Cp-(Cr-Cp)*exp(Jw/k))
            Cm=fsolve(fm,Cr)
        else:
            Cm=Cr
        PIm=self.__R__*T*1e-5*Cm # bar
        DPi=PIm-PIp
        Jw=(p-self.Patm-DPi.sum())*self.Aw
        return Cm,Jw,PIm,PIp,DPi
