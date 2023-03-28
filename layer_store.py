from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.abstract_list import List


class LayerStore(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass

class SetLayerStore(LayerStore):
    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """

    def __init__(self, max_capacity: int): #needs a stack, list. 
        
        self.stack = ArrayStack()
        self.stack.__len__(max_capacity)  # limits len as 1

        self.special_active = False # status of special form 

    def add(self, layer: Layer)-> bool:
            
        if self.stack.is_empty:
            self.stack.push(layer)
        else:
            self.stack.pop()
            self.stack.push(layer)

        return True
    
    #self.layer = layer
    
    
    def erase(self)-> bool: # we dont need layer for this 
        
        
        self.stack.pop()

        return True

        
    def special(self):
        # in order to apply inversion, (255-R, 255-G, 255-B)
        
        if self.special_active is False:
            self.special_active = True

        else:
            self.special_active = True

    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:

        cur_color = self.stack.pop() 

        # if the layer is empty, return start (the original code)
        if cur_color is None:
            return start
        #activating special depends on the situation
        elif self.special_active is True:
            rtrn_color = cur_color.apply(start, timestamp, x, y)
            return rtrn_color.apply(255-rtrn_color[0], 255 - rtrn_color[1], 255 - rtrn_color[2])

        else: 
            return cur_color.apply(start, timestamp, x, y)
    




        
class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """


    def __init__(self) -> None:

        # use array stack 

        self.stack_A = ArrayStack() # stack to store layers
        self.stack_B = ArrayStack() # temporary stack 

        # or use circular queue
        self.queue_A = CircularQueue()
        self.queue_B = CircularQueue()

        # or use list

        self.list_A = list()
        self.list_B = List()



    def add(self, layer: Layer)->: 
        
        #self.queue_A.push(layer)
        self.list_A.append(layer)

    def erase(self)->:
        
        #for i in range(1, ):
        #    return self.stack_B.push(self.stack_A.pop())

        #self.queue_A.serve() #removing the "oldest" element in the queue

        return self.list_A(0)



    def special(self)->:
        # make a another contianer to temporarily store colour
        #i = 2 # start from two since reversing

        #for items in stack_A:
             # or stack
        #if i >= 0: 
            #self.stack_B.push(self.stack_A.pop()) # appending the item to a new stack
            #i -= 1
        
        #return self.stack_B # do i need to return the new one ?

        len_A = self.list_A.__len__

        for i in range(0, len_A):
            self.list_B.append(self.list_A.index([i]))
        
        return self.list_B # the new reversed list

class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """

    def __init__(self) -> None:
    
    def add(self, layer: Layer) -> bool: # makes the layer "applying"



    def erase(self, layer: Layer) -> bool:
    
    def special()

    def lexicographic_Order(txt):
        tup_lst = []
        for word in txt.split():
            for ch in word:
                if ch in "0123456789":
                    tup_lst.append((ch, word))
        return sorted(tup_lst)