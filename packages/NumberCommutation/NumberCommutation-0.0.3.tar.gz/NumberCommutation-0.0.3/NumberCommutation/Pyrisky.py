import numpy as np
import pandas as pd

class TableAnnuity:
    '''Classe voltada para a construção de uma tábua de comutação'''
    
    def __init__(self, lx, taxa, idade_inicio = 0):
        self.lx = lx
        self.taxa = taxa
        self.idade = idade_inicio
        
    def AllTable(self):
        lx = self.lx.to_numpy()
        if self.idade == 0:
            n = np.array(range(0,len(lx)))
        else:
            n = np.array(range(self.idade,len(lx)+self.idade))
        x = n    
        lx1 = lx[1:]
        lx1 = np.append(lx1,0)
        dx = lx -lx1
        lx_clone = lx.copy()
        lx_clone[lx_clone == 0] = 1
        qx = dx/lx_clone
        qx[qx == 0] = 1
        px = 1- qx
        Lx = (lx +lx1)/2
        Tx = np.array([np.sum(Lx[i:]) for i in range(0,len(Lx))])
        ex = Tx/lx_clone  
        Dx = lx/((1+self.taxa)**n)
        Dx_clone = Dx.copy()
        Dx_clone[Dx_clone == 0] = 1
        Nx = np.array([np.sum(Dx[i:]) for i in range(0,len(Dx))])
        Cx = dx/((1+self.taxa)**n)
        Mx = np.array([np.sum(Cx[i:]) for i in range(0,len(Cx))])
        Sx = np.array([np.sum(Nx[i:]) for i in range(0,len(Nx))])
        nx_2 = Nx.copy()
        nx_2 = np.array(nx_2[1:])
        nx_2 = np.append(nx_2,0)
        ax_pos = nx_2/Dx_clone
        ax_ant = Nx/Dx_clone

        tb = pd.DataFrame({"X":x,"lx":lx,"dx":dx, "qx":qx, "px":px, "Lx":Lx, "Tx":Tx,"Ex":ex,"Dx":Dx,"Nx":Nx,"Cx":Cx,"Mx":Mx, "Sx":Sx, "äx":ax_pos, "ax": ax_ant})

        return tb
    
class Commutation:
    '''Classe voltada a cálculos de múmeros de comutação'''
    
    def __init__(self, idade, dados, data_type='q', amostra = 1000000):
        self.idade = idade
        self.dados = dados
        self.data_type = data_type
        self.amostra = amostra    

    def qx(self,X):
        #idade_min = self.dados[self.dados.columns[self.local_idade]].min()
        x = list(self.idade).index(X)
        
        if self.data_type == 'q':
            qx = self.dados.to_numpy()    
            return qx[x]
        
        if self.data_type == 'p':
            ### qx = 1 - px
            
            px = self.dados.to_numpy()
            qx = 1-px

            return qx[x]
    
        if self.data_type == 'l':
            ### qx = lx- lx+1/lx
            
            lx = self.dados.to_numpy()
            qx = (lx[x]-lx[x+1])/lx[x]
            return qx
        
        if self.data_type == 'd':
            ### qx = dx/lx
            
            dx = self.dados.to_numpy()
            qx = dx[x]/(self.amostra - np.sum(dx[0:x]))
            return qx
        
    def px(self,X):
        x = list(self.idade).index(X)

        if self.data_type == 'p':
            px = self.dados.to_numpy()

            return px[x]

        if self.data_type == 'q':
            ### px = 1 - qx
            qx = self.dados.to_numpy()
            px = 1-qx

            return px[x]

        if self.data_type == 'l':
            ### px = lx+1/lx

            lx = self.dados.to_numpy()
            px = lx[x+1]/lx[x]
            return px

        if self.data_type == 'd':
            ### px = 1 - (dx/lx)

            dx = self.dados.to_numpy()
            px = 1-(dx[x]/(self.amostra - np.sum(dx[0:x])))
            return px
    
    def lx(self,X):
        x = list(self.idade).index(X)
        
        if self.data_type == 'l':
            lx = self.dados.to_numpy()

            return lx[x]

        if self.data_type == 'q':
            ### lx = Produtório(1-qx)*Radix

            qx = self.dados.to_numpy()
            px = 1-qx
            lx = np.prod(px[0:x])*self.amostra

            return lx

        if self.data_type == 'p':
            ### lx = Produtório(px)*Radix

            px = self.dados.to_numpy()
            lx = np.prod(px[0:x])*self.amostra
            return lx

        if self.data_type == 'd':
            dx = self.dados.to_numpy()
            lx = (self.amostra - np.sum(dx[0:x]))
            return lx
        
    def dx(self,X):
        x = list(self.idade).index(X)
        
        if self.data_type == 'd':
            dx = self.dados.to_numpy()        
            return dx[x]
        
        if self.data_type == 'q':
            qx = self.dados.to_numpy()
            px = 1-qx
            lx = np.prod(px[0:x])*self.amostra
            lx1 = np.prod(px[0:x+1])*self.amostra
            dx = lx - lx1
            return dx
    
        if self.data_type == 'p':
            px = self.dados.to_numpy()
            lx = np.prod(px[0:x])*self.amostra
            lx1 = np.prod(px[0:x+1])*self.amostra
            dx = lx-lx1
            return dx
        
        if self.data_type == 'l':
            ### dx = lx - lx+1           
            lx = self.dados.to_numpy()
            dx = lx[x] - lx[x+1]
            return dx
        
    ### Lx = (lx + lx+1)/2
    def Lx(self,X):
        x = list(self.idade).index(X)
        if self.data_type == 'l':
            lx = self.dados.to_numpy()
            Lx = (lx[x]+lx[x+1])/2
            return Lx
        
        if self.data_type == 'q':
            ### lx = Produtório(1-qx)*Radix
            
            qx = self.dados.to_numpy()
            px = 1-qx
            lx = np.prod(px[0:x])*self.amostra
            lx = round(lx)
            lx1 = np.prod(px[0:x+1])*self.amostra
            lx1 = round(lx1)
            Lx = (lx+lx1)/2
            return Lx
    
        if self.data_type == 'p':
            ### lx = Produtório(px)*Radix            
            px = self.dados.to_numpy()
            lx = np.prod(px[0:x])*self.amostra
            lx = round(lx)
            lx1 = np.prod(px[0:x+1])*self.amostra
            lx1 = round(lx1)
            Lx = (lx+lx1)/2
            return Lx
            
        
        if self.data_type == 'd':
            dx = self.dados.to_numpy()
            lx = self.amostra - np.sum(dx[0:x])
            lx = round(lx)
            lx1 = self.amostra - np.sum(dx[0:x+1])
            lx1 = round(lx1)
            Lx = (lx+lx1)/2
            return Lx
    
    ### Tx = soma Lx
    def Tx(self,X):
        x = list(self.idade).index(X)
        
        if self.data_type == 'd':
            dx = self.dados.to_numpy()
            lx = [round(self.amostra - np.sum(dx[0:x+i])) for i in list(range(0,len(dx[x:])+1))]
            Lx = (lx+np.hstack([lx[1:],np.zeros(1)]))/2
            Tx = sum(Lx)
            return Tx
        
        if self.data_type == 'l':
            lx = self.dados.to_numpy()
            Lx = (lx+np.hstack([lx[1:],np.zeros(1)]))/2
            Tx = np.sum(Lx[x:])
            return Tx
        
        if self.data_type == 'q':
            ### lx = Produtório(1-qx)*Radix           
            qx = self.dados.to_numpy()
            px = 1-qx
            lx = [round(np.prod(px[:i])*self.amostra) for i in range(0,len(px)+1)]
            Lx = (lx+np.hstack([lx[1:],np.zeros(1)]))/2
            Tx = np.sum(Lx[x:])
            return Tx
        
        if self.data_type == 'p':
            ### lx = Produtório(px)*Radix            
            px = self.dados.to_numpy()
            lx = [round(np.prod(px[:i])*self.amostra) for i in range(0,len(px)+1)]
            Lx = (lx+np.hstack([lx[1:],np.zeros(1)]))/2
            Tx = np.sum(Lx[x:])
            return Tx
    
    def ex(self,X):
        ### Ex = Tx/lx
        x = list(self.idade).index(X)

        if self.data_type == 'd':
            dx = self.dados.to_numpy()
            lx = [round(self.amostra - np.sum(dx[0:x+i])) for i in list(range(0,len(dx[x:])+1))]
            Lx = (lx+np.hstack([lx[1:],np.zeros(1)]))/2
            Tx = sum(Lx)
            ex = Tx/lx[0]
            return ex
        
        if self.data_type == 'l':
            lx = self.dados.to_numpy()
            Lx = (lx+np.hstack([lx[1:],np.zeros(1)]))/2
            Tx = np.sum(Lx[x:])
            ex = Tx/lx[x]
            return ex
        
        if self.data_type == 'q':
            ### lx = Produtório(1-qx)*Radix            
            qx = self.dados.to_numpy()
            px = 1-qx
            lx = [round(np.prod(px[:i])*self.amostra) for i in range(0,len(px)+1)]
            Lx = (lx+np.hstack([lx[1:],np.zeros(1)]))/2
            Tx = np.sum(Lx[x:])
            ex = Tx/lx[x]
            return ex
        
        if self.data_type == 'p':
            ### lx = Produtório(px)*Radix
            px = self.dados.to_numpy()
            lx = [round(np.prod(px[:i])*self.amostra) for i in range(0,len(px)+1)]
            Lx = (lx+np.hstack([lx[1:],np.zeros(1)]))/2
            Tx = np.sum(Lx[x:])
            ex = Tx/lx[x]
            return ex
    
    def Dx(self,X, taxa):
        ### Dx = lx/((1+i)**x)
        x = list(self.idade).index(X)

        if self.data_type == 'd':
            dx = self.dados.to_numpy()
            lx = round(self.amostra - np.sum(dx[0:x]))
            Dx = lx/((1+taxa)**X)
            return Dx            
        if self.data_type == 'l':
            lx = self.dados.to_numpy()
            Dx = lx[x]/((1+taxa)**X)
            return Dx
        
        if self.data_type == 'q':
            ### lx = Produtório(1-qx)*Radix            
            qx = self.dados.to_numpy()
            px = 1-qx
            lx = np.prod(px[0:x])*self.amostra
            lx = round(lx)
            Dx = lx/((1+taxa)**x)
            return Dx
    
        if self.data_type == 'p':
            ### lx = Produtório(px)*Radix            
            px = self.dados.to_numpy()
            lx = np.prod(px[0:x])*self.amostra
            lx = round(lx)
            Dx = lx/((1+taxa)**x)
            return Dx
  
    def Nx(self,X, taxa):
        
        ### Nx = Soma Dx
        ### Dx = lx/((1+i)**x)
        x = list(self.idade).index(X)
        
        if self.data_type == 'd':
            dx = self.dados.to_numpy()
            lx = [round(self.amostra - np.sum(dx[0:i])) for i in list(range(0,len(dx)+1))]
            n = np.array(range(0,len(lx)))
            Dx = lx/((1+taxa)**n)
            Nx = np.sum(Dx[x:])
            return Nx
        
        if self.data_type == 'l':
            lx = self.dados.to_numpy()
            n = np.array(range(0,len(lx)))
            Dx = lx/((1+taxa)**n)
            Nx = np.sum(Dx[x:])
            return Nx
        
        if self.data_type == 'q':
            ### lx = Produtório(1-qx)*Radix            
            qx = self.dados.to_numpy()
            px = 1-qx
            lx = np.array([round(np.prod(px[:i])*self.amostra) for i in range(0,len(px)+1)])
            n = np.array(range(0,len(lx)))
            Dx = lx/((1+taxa)**n)
            Nx = np.sum(Dx[x:])
            return Nx
    
        if self.data_type == 'p':
            ### lx = Produtório(px)*Radix            
            px = self.dados.to_numpy()
            lx = np.array([round(np.prod(px[:i])*self.amostra) for i in range(0,len(px)+1)])
            n = np.array(range(0,len(lx)))
            Dx = lx/((1+taxa)**n)
            Nx = np.sum(Dx[x:])
            return Nx
        
    def Cx(self,X, taxa):
        x = list(self.idade).index(X)
        if self.data_type == 'd':
            dx = self.dados.to_numpy()
            n = np.array(range(0,len(dx)))
            Cx = dx/((1+taxa)**n)
            return Cx[x]
        
        if self.data_type == 'q':
            qx = self.dados.to_numpy()
            px = 1-qx
            lx = np.array([round(np.prod(px[:i])*self.amostra) for i in range(0,len(px)+1)])
            lx1 = lx[1:]
            lx1 = np.append(lx1,0)
            dx = lx - lx1
            n = np.array(range(0,len(dx)))
            Cx = dx/((1+taxa)**n)
            return Cx[x]
    
        if self.data_type == 'p':
            px = self.dados.to_numpy()
            lx = np.array([round(np.prod(px[:i])*self.amostra) for i in range(0,len(px)+1)])
            lx1 = lx[1:]
            lx1 = np.append(lx1,0)
            dx = lx - lx1
            n = np.array(range(0,len(dx)))
            Cx = dx/((1+taxa)**n)
            return Cx[x]
        
        if self.data_type == 'l':
            ### dx = lx - lx+1            
            lx = self.dados.to_numpy()
            lx1 = lx[1:]
            lx1 = np.append(lx1,0)
            dx = lx - lx1
            n = np.array(range(0,len(dx)))
            Cx = dx/((1+taxa)**n)
            return Cx[x]
        
    def Mx(self,X, taxa):
        x = list(self.idade).index(X)
        if self.data_type == 'd':
            dx = self.dados.to_numpy()
            n = np.array(range(0,len(dx)))
            Cx = dx/((1+taxa)**n)
            Mx = np.sum(Cx[x:])
            return Mx
        
        if self.data_type == 'q':
            qx = self.dados.to_numpy()
            px = 1-qx
            lx = np.array([round(np.prod(px[:i])*self.amostra) for i in range(0,len(px)+1)])
            lx1 = lx[1:]
            lx1 = np.append(lx1,0)
            dx = lx - lx1
            n = np.array(range(0,len(dx)))
            Cx = dx/((1+taxa)**n)
            Mx = np.sum(Cx[x:])
            return Mx
    
        if self.data_type == 'p':
            px = self.dados.to_numpy()
            lx = np.array([round(np.prod(px[:i])*self.amostra) for i in range(0,len(px)+1)])
            lx1 = lx[1:]
            lx1 = np.append(lx1,0)
            dx = lx - lx1
            n = np.array(range(0,len(dx)))
            Cx = dx/((1+taxa)**n)
            Mx = np.sum(Cx[x:])
            return Mx
        
        if self.data_type == 'l':
            ### dx = lx - lx+1           
            lx = self.dados.to_numpy()
            lx1 = lx[1:]
            lx1 = np.append(lx1,0)
            dx = lx - lx1
            n = np.array(range(0,len(dx)))
            Cx = dx/((1+taxa)**n)
            Mx = np.sum(Cx[x:])
            return Mx