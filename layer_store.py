from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
from data_structures.stack_adt import Stack
from data_structures.stack_adt import ArrayStack


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

        # start = starting colour
        # timestamp

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
        self.stack.__len__(1)  # limits len as 1
        

        self.special_active = False # status of special form 

    def add(self, layer: Layer)-> bool:#
            
        if self.stack.is_empty:
            self.stack.push(layer)
        else:
            self.stack.pop()
            self.stack.push(layer)

        return True
    
    #self.layer = layer
    
    
    def erase(self, layer: Layer)-> bool: # we dont need layer for this 
        
        
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


    def __init__(self):

        # use array stack 

        self.stack_A = ArrayStack() #stack to store layers
        self.stack_B = ArrayStack() # temporary stack 

    def add(self, layer: Layer): # treating layer as a stack ??
        
        self.stack_A.push(layer)

    def erase(self):
        
        for i in range():
            return self.stack_B.push(self.stack_A.pop())


    def special(self, layer: Layer):
        # make a another contianer to temporarily store colour
        i = 2 # start from two since reversing

        for items in layer: # or stack
            self.stack.push(self.stack.pop(layer)) # appending the item to a new stack
            i -= 1
        
        return self.stack # do i need to return the new one ?

class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """

    pass
