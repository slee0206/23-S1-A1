from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
from data_structures.stack_adt import Stack


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

    def __init__(self): #needs a stack, list. / do i need to put layerstore?
        
        self.stack = Stack()
        self.len() = 1 # length

    def add(self, layer: Layer): #
            
        if self.stack.is_empty:
            self.stack.push(layer)
        else:
            self.stack.pop()
            self.stack.push(layer)
    
    def erase(self): # we dont need layer for this 
        
        self.stack.pop()
        
    def special(self):

        
        return 

class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """


    def __init__(self):

        # use array stack 

        self.stack_A = Stack() #stack to store layers
        self.stack_B = Stack() # temporary stack 

    def add(self, layer: Layer): # treating layer as a stack ??
        
        self.stack.push(layer)

    def erase(self):
        
        self.stack_B.push(self.stack_A.pop())


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
