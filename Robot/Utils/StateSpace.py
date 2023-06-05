import numpy as np
import math
from matplotlib import pyplot as plt
import time
import scipy as sp

from termcolor import colored

def GetErrorLimits(K,max_input,min_input):
        max_error=np.array(np.matrix(K).I@max_input)[0]
        min_error=np.array(np.matrix(K).I@min_input)[0]
        return max_error,min_error

def InputLimit(u,max_input,min_input,max_error,min_error):
    if(u > max_input or u < min_input):
        # print("Original",u)
        for k in range(len(e)):
            # print(min_error[k],e[k],max_error[k])
            e[k] = min(e[k], max_error[k])
            # print(e[k])
            e[k] = max(e[k], min_error[k])
        u = K@e
        # print("Shifted",u)
    return u

def PointAtAngleAndDistance(distance,degrees):
    x = distance * math.cos(math.radians(degrees))
    y = distance * math.sin(math.radians(degrees))
    return (x,y)

class StateSpaceSystem():
    p = 0 # Number of inputs
    q = 0 # Number of outputs
    n = 0 # Number of states

    x = None # State vector
    y = None # Output vector
    u = None # Input Vector

    A = None # System Matrix
    B = None # Input Matrix
    C = None # Output Matrix
    D = None # Feedthrough Matrix

    def __init__(self, p, q, n, A = None, B = None, C = None, D = None):
        self.p = p
        self.q = q
        self.n = n

        if(self.A is None):
            if(A is None):
                self.A = np.zeros((n,n)) # System Matrix
            elif (A.shape == (n,n)):
                self.A = A
            else:
                raise Exception(colored("Matrix A must be of shape (n,n) ["+str(n)+","+str(n)+"]","red"))
        else:
            self.A = np.array(self.A)

        if(self.B is None):
            if(B is None):
                self.B = np.zeros((n,p)) # Input Matrix
            elif (B.shape == (n,p)):
                self.B = B
            else:
                raise Exception(colored("Matrix B must be of shape (n,p) ["+str(n)+","+str(p)+"]","red"))
        else:
            self.B = np.array(self.B)

        if(self.C is None):
            if(C is None):
                self.C = np.zeros((q,n)) # Output Matrix
            elif (C.shape == (q,n)):
                self.C = C
            else:
                raise Exception(colored("Matrix C must be of shape (q,n) ["+str(q)+","+str(n)+"]","red"))
        else:
            self.C = np.array(self.C)

        if(self.D is None):    
            if(D is None):
                self.D = np.zeros((q,p)) # Feedthrough Matrix
            elif (D.shape == (q,p)):
                self.D = D
            else:
                raise Exception(colored("Matrix D must be of shape (q,p) ["+str(q)+","+str(p)+"]","red"))
        else:
            self.D = np.array(self.D)

        if(self.x is None):
            self.x = np.zeros((self.n))
        else:
            self.x = np.array(self.x)

        if(self.y is None):
            self.y = np.zeros((self.q))
        else:
            self.y = np.array(self.y)
        
        if(self.u is None):
            self.u = np.zeros((self.p))
        else:
            self.u = np.array(self.u)

    def Set_u(self,u):
        if (u.shape == (self.p,)):
            self.u = u
        else:
            raise Exception(colored("u (input) must be a vector of len p ["+str(self.p)+"]","red"))

    def Set_x(self,x):
        if (x.shape == (self.n,)):
            self.x = x
        else:
            raise Exception(colored("x (input) must be a vector of len n ["+str(self.n)+"]","red"))

    def Get_x(self):
        return self.x

    def Get_ẋ(self,u = None):
        if(u is None):
            u = self.u
        if (u.shape == (self.p,)):
            return np.matmul(self.A,self.x)+np.matmul(self.B,u)
        else:
            raise Exception(colored("u (input) must be a vector of len p ["+str(self.p)+"]","red"))

    def Get_y(self,u = None):
        if(u is None):
            u = self.u
        if (u.shape == (self.p,)):
            return self.Get_C() @ self.Get_x() + self.Get_D() @ u 
        else:
            raise Exception(colored("u (input) must be a vector of len p ["+str(self.p)+"]","red"))

    def Get_u(self):
        return self.u

    def Get_A(self):
        return self.A

    def Get_B(self):
        return self.B

    def Get_C(self):
        return self.C

    def Get_D(self):
        return self.D

    def Show_Phase_Portrait(self,state_variable_1_idx = 0,state_variable_2_idx = 1,xscale=10,yscale=10):
        original_state = self.x

        y1 = np.linspace(-xscale/2, xscale/2, 20)
        y2 = np.linspace(-yscale/2, yscale/2, 20)

        Y1, Y2 = np.meshgrid(y1, y2)

        u, v = np.zeros(Y1.shape), np.zeros(Y2.shape)

        NI, NJ = Y1.shape

        for i in range(NI):
            for j in range(NJ):
                x = Y1[i, j]
                y = Y2[i, j]
                
                input = np.zeros_like(self.Get_x())
                input[state_variable_1_idx] = x
                input[state_variable_2_idx] = y

                self.Set_x(input)
                state = self.Get_ẋ()

                u[i,j] = state[state_variable_1_idx]
                v[i,j] = state[state_variable_2_idx]
            
        self.Set_x(original_state)

        plt.quiver(Y1, Y2, u, v, color='b')

        plt.xlabel("x["+str(state_variable_1_idx)+"]")
        plt.ylabel("x["+str(state_variable_2_idx)+"]")
        plt.xlim([-xscale/2-1, xscale/2+1])
        plt.ylim([-yscale/2-1, yscale/2+1])
        plt.show()

    def LQR(self,Q,R):
        X = sp.linalg.solve_continuous_are(self.Get_A(), self.Get_B(), Q, R)
        return np.array(sp.linalg.inv(R)* (self.Get_B().T @ X))

    def dLQR(self,Q,R):
        X = sp.linalg.solve_discrete_are(self.Get_A(), self.Get_B(), Q, R)
        return np.array(sp.linalg.inv(self.Get_B().T@X@self.Get_B()+R)@(self.Get_B().T@X@self.Get_A()))

    def Calculate_u(self,K,r,x = None):
        if x is None:
            x = self.x
        return (K @ (r-x))

    def isControllable(self):
        M = []
        for i in range(self.n):
            a = self.Get_A()
            for amount in range(i):
                a = self.Get_A() @ a
            sequence = a @ self.Get_B()
            M.append(sequence)
        return len(np.linalg.matrix_rank(np.array(M))) <= self.n


if __name__ == "__main__":
    # raise Exception(colored("You are not supposed to run the file statespace.py, the main function is only here to give an example program.","red"))

    class PositionControlledFlywheel(StateSpaceSystem): # Override the default Time-Invariant method to use ΔT
        I = 0.0002633
        I = 0.01713

        A = [[0,0.9],[0,0.0]]
        B = [[0.],[1/I]]
        C = [[(180/math.pi)/360,0]]
        D = [[0]]

        def Get_ẋ(self, u = None, dt = None):
            if(dt is None): # Assume dt of 1 if not specified
                dt = 1
            if(u is None):
                u = self.u
            if (u.shape == (self.p,)):
                return np.multiply(self.A,dt) @ self.x + np.multiply(self.B,dt) @ u
            else:
                raise Exception(colored("u (input) must be a vector of len p ["+str(self.p)+"]","red"))

    Position_Controlled_Flywheel = PositionControlledFlywheel(1,1,2)
    
    Q = np.array([
        [1.0,0.0],
        [0.0,0.7],])
    R = np.array([[1]])

    start = time.time()
    K = Position_Controlled_Flywheel.LQR(Q,R)
    print("LQR Calculation Time:",time.time() - start)

    print("Gains,",K)

    step = 0.01
    horizon = 50

    # MATPLOTLIB VISUALIZATION
    x = []
    inputs = []
    nonliminputs = []
    errors = []
    angles = []
    # MATPLOTLIB VISUALIZATION

    max_input = np.array([4])
    min_input = np.array([-4])
    max_error, min_error = GetErrorLimits(K,max_input,min_input)

    r = np.array([math.radians(360*10),0.0]) 
    
    # MATPLOTLIB VISUALIZATION
    e=(r-Position_Controlled_Flywheel.Get_x())
    u = InputLimit(K@e,max_input,min_input,max_error,min_error)
    # MATPLOTLIB VISUALIZATION

    for i in range(0,int(horizon*(1/step)),1):
        # MATPLOTLIB VISUALIZATION
        x.append(i*step)
        inputs.append(u)
        errors.append(np.linalg.norm(e))
        angles.append(Position_Controlled_Flywheel.Get_y(u))
        nonliminputs.append(K@(r-Position_Controlled_Flywheel.Get_x()))
        # MATPLOTLIB VISUALIZATION

        e=(r-Position_Controlled_Flywheel.Get_x())
        u = InputLimit(K@e,max_input,min_input,max_error,min_error)

        Position_Controlled_Flywheel.Set_x(Position_Controlled_Flywheel.Get_x() + Position_Controlled_Flywheel.Get_ẋ(u,step)) # UPDATE STATE
        if(np.linalg.norm(Position_Controlled_Flywheel.Get_x()-r) <= 0.1): # END CONDITION
            print("Settling Time:",i*step)
            break

    # MATPLOTLIB VISUALIZATION
    fig, axs = plt.subplots(4)
    axs[0].plot(x,inputs,color="blue")
    axs[1].plot(x,nonliminputs,color="purple")
    axs[2].plot(x,errors,color="red")
    axs[3].plot(x,angles,color="green")
    axs[3].axhline(r[0]*(180/math.pi)/360)
    axs[0].set_title("Settling Time: " + str(i*step))
    plt.show()
    # MATPLOTLIB VISUALIZATION