# Implementação de HashTable com tratamento de colisão por encadeamento
# Autor: Alex Sandro

from typing import List
from ListaEncadeadaOrdenada import Lista
class AbsentKeyException(Exception):
    def __init__(self,msg):
        super().__init__(msg)


class Entry:
    """Uma classe privada utilizada para encapsular os pares chave/valor"""

    def __init__( self, entryKey:any, entryValue:any):
        self.key = entryKey
        self.value = entryValue
        
    def __eq__(self, outroObjeto):
        return self.key == outroObjeto.key
    
    def __ne__(self, outroObjeto):
        return self.key != outroObjeto.key
    
    def __lt__(self, outroObjeto):
        return self.key < outroObjeto.key
    
    def __gt__(self, outro_objeto):
        '''Método que possibilita comparar chaves quando a chave for um objeto de outra classe'''
        return self.key > outro_objeto.key

    def __le__(self, outroObjeto):
        return self.key <= outroObjeto.key
    
    def __ge__(self, outroObjeto):
        return self.key >= outroObjeto.key
    
    def __str__( self )->str:
        return "(" + str( self.key ) + ":" + str( self.value ) + ")"
 
class ChainingHashTable:
    def __init__(self, size=10):
        self.size = size
        # inicializa a tabela de dispersão com uma série de lists vazios
        self.table = list(Lista() for i in range(self.size))


    def __hash(self, key:any):
        ''' Método que retorna a posição na tabela hashing conforme a chave.
            Aplicação do cálculo do hash modular.
        '''
        return hash(key) % self.size

    def put(self, key:any, value:any)->int:
        '''
        Adiciona um par chave/valor à tabela hash
        Se a chave já existir, não insere, pois não é permitido chaves duplicadas 
        '''
        slot = self.__hash( key )
        # print(f'key {key} mapeada ao slot {slot}')

        # varre as entradas da ht para ver se já existe a chave
        if not self.table[slot].estaVazia():
            if self.contains(key):
                return "Chave já existente" #
        
        entry = Entry(key,value)    
        self.table[slot].inserir(entry)
        return slot
            

    def get(self, key:any)->any:
        '''
        Obtem o valor armazenado na entrada referente à chave "key"
        '''
        try:
            
            FoundedKey = self.__getObejctByKey(key)
            return FoundedKey.value
        
        except:
            
            raise AbsentKeyException(f'Chave {key} inexistente na tabela hash')

   
    def __str__(self)->str:
        info = "{ "
        for items in self.table:
            # examina se o slot da tabela hash tem um list com elementos
            if items == None:
                continue
            for entry in items:
                info += str(entry)
        info += " }"
        return info


    def __len__(self)->int:
        count = 0
        for i in self.table:
            count += len(i)
        return count
         

 
    def keys(self)->List[any]:
        """Retorna uma lista com as chaves armazenadas na hashTable.
        """
        result = []
        for lst in self.table:
            if not lst.estaVazia():
                for entry in lst:
                    result.append( entry.key )
        return result
    
    def values(self)->List[any]:
        """Retorna uma lista com as chaves armazenadas na hashTable.
        """
        result = []
        for lst in self.table:
            if not lst.estaVazia():
                for entry in lst:
                    result.append( entry.value )
        return result

    def contains( self, key:any )->bool:
        """Return True se somente se a tabela hash tem uma entrada com a chave passada
           como argumento.
        """
        entry = self.__locate( key )
        return isinstance( entry, Entry )


    def __locate(self, key)->Entry:
        '''
        Método que verifica se uma chave está presente na tabela hash e devolve a
        entrada correspondente quando a busca é realizada com sucesso
        '''
        try:
            
            entry = self.__getObejctByKey(key)    
            return entry
        
        except:
            return None
          
    def remove(self, key:any)->Entry:
        '''
        Método que remove a entrada correspondente à chave passada como argumento
        '''
        try:
            slot = self.__hash(key)
          
            entry = self.__getObejctByKey(key)
            posicao = self.BinarySearch(self.table[slot], entry)
            self.table[slot].remover(posicao)  
            return entry
        
        except:
            raise AbsentKeyException(f'Chave {key} não está presente na tabela hash') 


    def displayTable(self):
        entrada = -1
        for items in self.table:
            entrada += 1
            print(f'Entrada {entrada:2d}: ', end='') 
            if len(items) == 0:
                print(' None')
                continue
            for entry in items:
                print(f'[ {entry.key},{entry.value} ] ',end='')
            print()
    
    
    def BinarySearch(self, lista, chave):
        inicio = 1
        fim = len(lista)
        # Enquanto houver distância entre inicio e fim
        while (inicio <= fim ):

            meio = (inicio + fim)//2
            if ( chave < lista.elemento(meio) ):
                fim = meio - 1 # Ajusta a pos. final
                
            
            elif ( chave > lista.elemento(meio)):
                inicio = meio + 1 # Ajusta a pos. inicial
                
            
            else:
                return meio # elemento foi encontrado!

            # Se finalizar o laço, percorreu todo o lista e
            # não encontrou
        return -1
    
    def __getObejctByKey(self, key):
        """_summary_

        Args:
            key (_any_): _description_

        Returns:
            _type_: _description_
        """
        slot = self.__hash(key)
        
        capsula = Entry(key, None)       
        try:
            
            search = self.BinarySearch(self.table[slot], capsula)
            FoundedKey = self.table[slot].elemento(search)  
            return FoundedKey
        
        except:
            
            raise AbsentKeyException(f"Chave {key} não está presente na tabela hash")
        
    
    
# size = int(input("Enter the Size of the hash table : "))
# table1 = ChainingHashTable(size)
 
# # storing elements in table
# table1.put("Alex",'Alex Objeto')
# table1.displayTable()

# table1.put("alex",'alex Obejto')
# table1.displayTable()

# table1.put("31",'nathan')
# table1.put("90",'alice')

# print('len',len(table1))

# table1.put("28",'matheus')
# table1.put("88",'duda')
# table1.put("17",'jessika')
# table1.put("22",'bruno')
# table1.put("13",'Devyd')

# table1.displayTable()
# print('get():', table1.get("Alex"))
# table1.displayTable()
# print(table1.keys())
# print(table1.values())
# print()
# print(table1)

# table1.put('ed-tsi','Estrutura de Dados')

# table1.displayTable()
# print(table1.remove("31"))
# print(table1.remove("90"))
# print(table1.remove("28"))
# print(table1.remove("88"))
# print(table1.remove("17"))
# print(table1.remove("22"))
# print(table1.contains("Alex"))
# print(table1.contains("alex"))
# print("Devyd é:", table1.contains("13"))



