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
        
        self.stack = Stack
        self.csize = 2

    def add(self, layer: Layer): # do i need layer? 
            
        if layer is_empty # ask
            return False
        else:
            self.stack.append(layer)
            self.csize += 1
            return True
    
    def erase(self, layer: Layer):
        
        self.pop([self.container.index[layer]-1])

        return 
    
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
        self.stack = Stack #stack to store layers

    def add(self, layer: Layer): # treating layer as a stack ??
        
        self.stack.push(layer)

    def erase(self):

        self.stack.pop(0) # the first layer is always at index 0

    def special(self, layer: layer):
        # make a another contianer to temporarily store colour
        i = 2 # start from two since reversing

        for items in layer: # or stack
            self.stack.append(self.stack.pop(i)) # appending the item to a new stack
            i -= 1
        
        return self.stack # do i need to return the new one ?


        self.tempcontainer

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
