import numpy as np
import pandas as pd

class Priors:
    
    def __init__(self,bern_p,mean0,var0):
        
        self.bern_p = bern_p
        self.mean0  = mean0
        self.var0   = var0
        
    
    def __bernoulli(self):
        
        if np.random.random() < self.bern_p:
            
            return True
        
        
    def __gaussian(self):
        
        return np.random.normal(self.mean0, self.var0)


class Data(Priors):
    
    def __init__(self, bern_p=1/100,mean0=1,var0=3, file_name = "_",data_type =  "real"):
        super().__init__(bern_p,mean0,var0)
        
        self.data_type = data_type
        self.file_name = file_name
        self.data      = []
        self.cps       = []
        
    
    def update_data(self):
        
        if self.data_type == "sim":
            
            return self.__sim_data()
        
        if self.data_type == "real":
            
            return self.__real_data()
        
    
    def __sim_data(self,var = 1, rho = 0.3, T = 500):

        mean = super().__gaussian()
        self.data.append(np.random.normal(mean,var))
        
        for t in range(1,self.T): 
            
            if super().__bernoulli():
                
                mean = super().__gaussian()
                self.cps.append(t)
                self.data.append(np.random.normal(mean,var))
                
                continue
            
            self.data.append(np.random.normal(mean+rho*(self.data[t-1]-mean),var*(1-rho**2)))
        
        return self.data
    
    
    def __real_data(self):

        data_df = pd.read_csv(self.file_name,delimiter =',',header = 0)
        data = list(data_df[data_df.columns[0]])

        return data
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            