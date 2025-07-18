import numpy as np
import matplotlib.pyplot as plt

class linhaElastica:
    """
    Implementação da solução analítica da linha elástica em vigas.
    Seguindo a teoria presente em:
    HIBBELER, R. C. Resistência dos materiais. São Paulo (Sp): Pearson Education Do Brasil, 2010.
    Implementado por Vinicius Miranda Rodrigues
    contato: (41)99987-3264 ou vini142@hotmail.com
    """
    def __init__(self, L, E, I=0):
        """
        Inicializando o objeto
        
        Parâmetros
        ----------
        L : float
            Comprimento da viga (m)
        E : float
            Módulo de elasticidade (Pa)
        I : float
            Momento de inécia (m⁴)
        """
        self.L = L      # comprimento
        self.E = E      # módulo de elasticidade
        self.I = I      # momento de inércia
        self.P = None   # carregamento em N em cada ponto (array)
        self.x = None   # posição de cada força P (array)
    
    def set_P (self, P, x):
        """
        Atualiza o carregamento, para não precisar reiniciar o objeto
        
        Parâmetros
        ----------
        P : array_like
            Forças ao longo da longarina (N)
        x : array_like
            Posição das forças (m)
        
        Retorna
        ----------
        self : linha elástica
            Retorna self para uso intuitivo do código
        """
        self.P = P
        self.x = x
        return self
    
    def set_I (self, I):
        """
        Atualiza o momento de inércia, para não precisar reiniciar o objeto
        
        Parâmetros
        ----------
        I : float
            Momento de inércia (m⁴)
        
        Retorna
        ----------
        self : linha elástica
            Retorna self para uso intuitivo do código
        """
        self.I = I
        return self

    def plot(self):
        """
        Plota a deflexão, momento fletor e esforço cortante da viga
        
        Retorna
        ----------
        self : linha elástica
            Retorna self para uso intuitivo do código
        """
        x = np.linspace(0, self.L)
        y = self.get_y(x)
        y = np.hstack((y[::-1], y))
        x = np.hstack((-1*x[::-1],x))
        plt.plot(x, y, label="Deflection Curve")
        plt.xlabel("Beam Length (m)")
        plt.ylabel("Deflection (m)")
        plt.title("Beam Deflection")
        # plt.axis('equal')
        plt.legend()
        plt.grid()
        plt.show()
        return self
    
    def get_y(self, x):
        """
        Calcula a deflexão em metros para determinada posição x, dado um I
        
        Parâmetros
        ----------
        x : array_like
            Posição de interesse (m)
        
        Retorna
        ----------
        result : array_like
            Array de deflexão referente a cada posição (m)
        """
        result = np.zeros_like(x) # um resultado para cada posição 
        if self.I:
            try:
                for i in range(len(x)):
                    for j, P in enumerate(self.P):   # utilizando o método de sobreposição e calculando a deflexão para cada força separadamente
                        if x[i] < self.x[j]:         # função definida por partes, caso a posição de interesse seja anterior à força aplicada
                            result[i] += (P*x[i]**3)/6/self.E/self.I - (P*self.x[j]*x[i]**2)/2/self.E/self.I
                        else:                        # função definida por partes, caso a posição de interesse seja posterior à força aplicada
                            result[i] += (P*self.x[j]**3)/6/self.E/self.I - (P*x[i]*self.x[j]**2)/2/self.E/self.I
            except:
                print("Houve um erro, o carregamento foi definido?")
        else:
            print("Houve um erro, o momento de inércia foi definido?")

        return result
    
    def get_I(self, y, x):
        """
        Calcula o momento de inércia em metros⁴, dado uma deflexão para determinada posição x
        Usando o mesmo método de get_y, mas isolando o I
        
        Parâmetros
        ----------
        x : float
            Posição de interesse (m)
        y : float
            Deflexão desejada (m)

        Retorna
        ----------
        result : float
            Momento de inércia obtido (m⁴)
        """
        result = 0
        try:
            for j, P in enumerate(self.P):
                if x < self.x[j]:
                    result += (P*x**3)/6/self.E/y - (P*self.x[j]*x**2)/2/self.E/y
                else:
                    result += (P*self.x[j]**3)/6/self.E/y - (P*x*self.x[j]**2)/2/self.E/y
        except:
            print("Houve um erro, o carregamento foi definido?")
        
        return result

if __name__ == '__main__':
    E = 19011e6
    I = 4.22558e-8
    L = 1.25 - 0.09
    #P = np.array([15])
    #x = np.array([L])
    #P = np.array([18.56503315, 17.24157816, 15.03882724, 13.51931243, 13.96669049, 13.9400739, 10.57152585, 3.999898588]) # Caso 1 VA
    P = np.array([17.5188914, 17.84647437, 16.88513205, 16.29786822, 18.02258577, 19.2583944, 15.46861829, 6.026100479])  # Caso 2 VA
    x = np.array([0.094, 0.282, 0.448, 0.601, 0.748, 0.931, 1.111, 1.248])
    test = linhaElastica(L=L,E=E,I=I)
    test.set_P(P,x)
    #test.plot()
    #print(f"valor do livro: {-P*L**3/3/E/I}")  # valor do livro para uma forca pontual aplicada em L
    print(f"Valor calculado: {test.get_y([L])[0]}")
    #print(f"I obtido: {test.get_I(-0.02868102303873683, L)}")