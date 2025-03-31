import numpy as np
import random

CUBE_SIZE = 3
current_layer = 0

class State:
    def __init__(self, size=3):
        self.size = size
        self.faces = np.zeros((6, size, size), dtype=int)
        
        for k in range(6):
          self.faces[k, :, :] = k

    def front_clock(self, layer=0):
      temp = np.zeros(self.size, dtype=int)
    
      # rotacionar 
      for i in range(self.size):
        temp[i] = self.faces[2, self.size-1-layer, i]  # Salvar parte da face superior

        self.faces[2, self.size-1-layer, i] = self.faces[4, self.size-1-i, self.size-1-layer]  # Superior recebe Esquerda
        
        self.faces[4, self.size-1-i, self.size-1-layer] = self.faces[3, layer, self.size-1-i]  # Esquerda recebe Inferior
        
        self.faces[3, layer, self.size-1-i] = self.faces[5, i, layer]  # Inferior recebe Direita
        
        self.faces[5, i, layer] = temp[i]  # Direita recebe Superior (guardado em temp)
      
      if layer == 0:
        face_copy = self.faces[0].copy()
        for i in range(self.size):
            for j in range(self.size):
                self.faces[0, i, j] = face_copy[j, self.size-1-i]
    
    def front_anticlock(self, layer=0):
      temp = np.zeros(self.size, dtype=int)
      
      for i in range(self.size):
          temp[i] = self.faces[2, self.size-1-layer, self.size-1-i]  # Salvar parte da face superior

          self.faces[2, self.size-1-layer, self.size-1-i] = self.faces[5, i, layer]  # Superior recebe Direita
          
          self.faces[5, i, layer] = self.faces[3, layer, i]  # Direita recebe Inferior
          
          self.faces[3, layer, i] = self.faces[4, self.size-1-i, self.size-1-layer]  # Inferior recebe Esquerda
          
          self.faces[4, self.size-1-i, self.size-1-layer] = temp[i]  # Esquerda recebe Superior
      
      if layer == 0:
          face_copy = self.faces[0].copy()
          for i in range(self.size):
              for j in range(self.size):
                  self.faces[0, j, self.size-1-i] = face_copy[i, j]