
from __future__ import division
import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt

p2 = lambda theta: 1.5*theta**2-0.5
class Nematic_Liquid_Crystal():
    ''' Code adaptation of the paper Stable disclination lines
         in nematic liquid crystals confined in thin films with 
         periodic-planar surfaces'''    

    def __init__(self,top_layer_bc, bottom_layer_bc, size, K1,K2, K3,grating_length ):

        ''' Generate the initial boundary conditions and intialize the lattice '''
        self.Nx = size[0]
        self.Ny = size[1]
        self.Nz = size[2]
        x = np.linspace(0,grating_length,self.Nx)
        # declare your boundary conditions here: Default is the problem setup for Sasaki et al
        #top_boundary = np.pi/2*np.ones((self.Nz,self.Nx))
        #bottom_boundary = np.repeat([np.pi*x/grating_length],axis=0)

        self.top_boundary = top_layer_bc
        self.bottom_boundary = bottom_layer_bc
        #For molecules rotationally free all aligned with x axis 
        self.config = np.zeros((self.Nz,self.Nx,self.Ny,3)) # The configuration is in the following order [z_axis,x_axis,y_axis,dof]
        # Twist, Bend, Splay constants
        self.Ks = np.array([K1,K2,K3])
       
        
    def calculate_energy(self,config):
        phix,phiy,phiz = config

    ## monte carlo moves
    def mcmove(self, config, N, beta):
        ''' This is to execute the monte carlo moves using 
        Metropolis algorithm such that detailed
        balance condition is satisified'''
        for i in range(self.Nz):
            for j in range(self.Nx):
                    # Randomly select a lattice point           
                    a = np.random.randint(0, self.Nz)
                    b = np.random.randint(0, self.Nx)
                    c = np.random.randint(0, self.Ny)
                    # Calculate the energy of the current configuration
                    
                    # Rotata the molecule randomly 
                    s =  config[a, b,c,:]
                    nb = config[(a+1)%N,b] + config[a,(b+1)%N] + config[(a-1)%N,b] + config[a,(b-1)%N]
                    cost = 2*s*nb
                    if cost < 0:	
                        s *= -1
                    elif rand() < np.exp(-cost*beta):
                        s *= -1
                    config[a, b] = s
        return config
    
    def simulate(self):   
        ''' This module simulates the Ising model'''
        N, temp     = 64, .4        # Initialse the lattice
        config = 2*np.random.randint(2, size=(N,N))-1
        f = plt.figure(figsize=(15, 15), dpi=80);    
        self.configPlot(f, config, 0, N, 1);
        
        msrmnt = 1001
        for i in range(msrmnt):
            self.mcmove(config, N, 1.0/temp)
            if i == 1:       self.configPlot(f, config, i, N, 2);
            if i == 4:       self.configPlot(f, config, i, N, 3);
            if i == 32:      self.configPlot(f, config, i, N, 4);
            if i == 100:     self.configPlot(f, config, i, N, 5);
            if i == 1000:    self.configPlot(f, config, i, N, 6);
                 
                    
    def configPlot(self, f, config, i, N, n_):
        ''' This modules plts the configuration once passed to it along with time etc '''
        X, Y = np.meshgrid(range(N), range(N))
        sp =  f.add_subplot(3, 3, n_ )  
        plt.setp(sp.get_yticklabels(), visible=False)
        plt.setp(sp.get_xticklabels(), visible=False)      
        plt.pcolormesh(X, Y, config, cmap=plt.cm.RdBu);
        plt.title('Time=%d'%i); plt.axis('tight')    
    plt.show()


