import numpy as np
import random

class State:
    def __init__(self, size=3):
        self.size = size
        self.faces = np.zeros((6, size, size), dtype=int)
        
        for k in range(6):
            self.faces[k, :, :] = k

        #print(self.faces)

    def front_clock(self):
        temp = self.faces[2, 0, :].copy() 
        #self.faces[2, 0, :] = [0, 0, 0] # Linha superior primeira da minha visao
        #self.faces[3, 2, :] = [0, 0, 0] # linha de baixo primeira da minha visao 
        #self.faces[4, :, 0] = [0, 0, 0] # coluna primeira de minha visao esquerda
        #self.faces[5, :, 2] = [0, 0, 0] #coluna primeira de minha visao direita
        
        self.faces[2, 0, :] = self.faces[4, :, 0] # linha superior 
        self.faces[4, :, 0] = self.faces[3, 2, :][::-1] # linha da parte de baixo, [pegar coluna]
        self.faces[3, 2, :] = self.faces[5, :, 2] # ta pegando ultima linha [pega primeira]
        self.faces[5, :, 2] = temp[::-1] # ta pegando ultima linha [pega coluna]
        
        self.faces[0] = np.rot90(self.faces[0], k=1)
      

    def front_anticlock(self):
      temp = self.faces[2, 0, :].copy()  # Linha superior da face frontal
      # Ajuste das transferências com reversões para manter a orientação correta
      self.faces[2, 0, :] = self.faces[5, :, 2][::-1]  # Coluna direita -> Linha superior (invertida)
      self.faces[5, :, 2] = self.faces[3, 2, :]   # Linha inferior (back) -> Coluna direita (invertida)
      self.faces[3, 2, :] = self.faces[4, :, 0][::-1]   # Coluna esquerda -> Linha inferior (back) (invertida)
      self.faces[4, :, 0] = temp                  # Linha frontal original -> Coluna esquerda (invertida)
      
      # Rotaciona a própria face frontal 90 grados anti-horário
      self.faces[0] = np.rot90(self.faces[0], k=-1)
        

    def back_clock(self):
        temp = self.faces[2, 2, :].copy()  # Superior traseira
        
        self.faces[2, 2, :] = self.faces[5, :, 0][::-1]  # Superior <- Direita
        self.faces[5, :, 0] = self.faces[3, 0, :]  # Direita <- Inferior (invertida)
        self.faces[3, 0, :] = self.faces[4, :, 2][::-1]  # Inferior <- Esquerda (invertida)
        self.faces[4, :, 2] = temp  # Esquerda <- Superior (invertida)
        
        self.faces[1] = np.rot90(self.faces[1], k=1)
        

    def back_anticlock(self):
        temp = self.faces[2, 2, :].copy()  # Superior traseira
        
        self.faces[2, 2, :] = self.faces[4, :, 2]  # Superior <- Esquerda (invertida)
        self.faces[4, :, 2] = self.faces[3, 0, :][::-1]  # Esquerda <- Inferior (invertida)
        self.faces[3, 0, :] = self.faces[5, :, 0]  # Inferior <- Direita (invertida)
        self.faces[5, :, 0] = temp[::-1]  # Direita <- Superior
        # face_copy = self.faces[1].copy()
        
        self.faces[1] = np.rot90(self.faces[1], k=-1)
    # esta rotacionando a parte superior ao contrario
    # rotacoes laterais erradas
    def up_clock(self):
      #self.faces[5, 2, :] = [0, 0, 0]
      #self.faces[1, 2, :] = [0, 0, 0]
      
      temp = self.faces[0, 2, :].copy()  # Salva a linha superior da face da frente
      self.faces[0, 2, :] = self.faces[5, 2, :][::-1]  # Frente recebe Direita (invertida)
      self.faces[5, 2, :] = self.faces[1, 2, :][::-1]   # Direita recebe Traseira (invertida)
      self.faces[1, 2, :] = self.faces[4, 2, :][::-1]   # Traseira recebe Esquerda (invertida)
      self.faces[4, 2, :] = temp[::-1]  # Esquerda recebe Frente (invertida)

      self.faces[2] = np.rot90(self.faces[2], k=1)

    # esta rotacionando a parte superior ao contrario
    def up_anticlock(self):
      temp = self.faces[0, 2, :].copy()  # Salva a linha superior da face da frente
      self.faces[0, 2, :] = self.faces[4, 2, :][::-1]  # Frente recebe Direita (invertida)
      self.faces[4, 2, :] = self.faces[1, 2, :][::-1]   # Direita recebe Traseira (invertida)
      self.faces[1, 2, :] = self.faces[5, 2, :][::-1]   # Traseira recebe Esquerda (invertida)
      self.faces[5, 2, :] = temp[::-1]  # Esquerda recebe Frente (invertida)

      self.faces[2] = np.rot90(self.faces[2], k=-1)

    def down_clock(self):
      temp = self.faces[0, 2, :].copy()  # Frente inferior
      self.faces[0, 2, :] = self.faces[5, 2, :]  # Frente <- Esquerda
      self.faces[5, 2, :] = self.faces[1, 2, :][::-1]  # Esquerda <- Traseira
      self.faces[1, 2, :] = self.faces[4, 2, :]  # Traseira <- Direita
      self.faces[4, 2, :] = temp[::-1]  # Direita <- Frente
      face_copy = self.faces[2].copy()

      self.faces[2] = np.rot90(self.faces[2], k=1)
    
    
    def down_anticlock(self):
        temp = self.faces[0, 2, :].copy()  # Frente inferior
        self.faces[0, 2, :] = self.faces[4, 2, :][::-1]  # Frente <- Direita
        self.faces[4, 2, :] = self.faces[1, 2, :] # Direita <- Traseira
        self.faces[1, 2, :] = self.faces[5, 2, :][::-1]  # Traseira <- Esquerda
        self.faces[5, 2, :] = temp  # Esquerda <- Frente
        face_copy = self.faces[2].copy()
        
        self.faces[2] = np.rot90(self.faces[2], k=-1)

    def left_clock(self):
        temp = self.faces[0, :, 0].copy()  # Frente esquerda
        self.faces[0, :, 0] = self.faces[2, :, 0]  # Frente <- Superior
        self.faces[2, :, 0] = self.faces[1, :, 2][::-1]  # Superior <- Traseira (invertida)
        self.faces[1, :, 2] = self.faces[3, :, 0][::-1]  # Traseira <- Inferior (invertida)
        self.faces[3, :, 0] = temp  # Inferior <- Frente
        face_copy = self.faces[4].copy()
        for i in range(self.size):
            for j in range(self.size):
                self.faces[4, i, j] = face_copy[self.size-1-j, i]

    def left_anticlock(self):
        temp = self.faces[0, :, 0].copy()  # Frente esquerda
        self.faces[0, :, 0] = self.faces[3, :, 0]  # Frente <- Inferior
        self.faces[3, :, 0] = self.faces[1, :, 2][::-1]  # Inferior <- Traseira (invertida)
        self.faces[1, :, 2] = self.faces[2, :, 0][::-1]  # Traseira <- Superior (invertida)
        self.faces[2, :, 0] = temp  # Superior <- Frente
        face_copy = self.faces[4].copy()
        for i in range(self.size):
            for j in range(self.size):
                self.faces[4, i, j] = face_copy[j, self.size-1-i]

    def right_clock(self):
        temp = self.faces[0, :, 2].copy()  # Frente direita
        self.faces[0, :, 2] = self.faces[3, :, 2]  # Frente <- Inferior
        self.faces[3, :, 2] = self.faces[1, :, 0][::-1]  # Inferior <- Traseira (invertida)
        self.faces[1, :, 0] = self.faces[2, :, 2][::-1]  # Traseira <- Superior (invertida)
        self.faces[2, :, 2] = temp  # Superior <- Frente
        face_copy = self.faces[5].copy()
        for i in range(self.size):
            for j in range(self.size):
                self.faces[5, i, j] = face_copy[self.size-1-j, i]

    def right_anticlock(self):
        temp = self.faces[0, :, 2].copy()  # Frente direita
        self.faces[0, :, 2] = self.faces[2, :, 2]  # Frente <- Superior
        self.faces[2, :, 2] = self.faces[1, :, 0][::-1]  # Superior <- Traseira (invertida)
        self.faces[1, :, 0] = self.faces[3, :, 2][::-1]  # Traseira <- Inferior (invertida)
        self.faces[3, :, 2] = temp  # Inferior <- Frente
        face_copy = self.faces[5].copy()
        for i in range(self.size):
            for j in range(self.size):
                self.faces[5, i, j] = face_copy[j, self.size-1-i]

    