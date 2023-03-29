from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
import layers
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList


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

    def __init__(self): #needs a stack, list. 
        
        self.layer = None
        self.special_active = False # status of special form 

    def add(self, layer: Layer)-> bool:
        self.layer = layer
        return True 
    
    
    def erase(self, layer: Layer)-> bool: # we dont need layer for this 
        self.layer = None
        return True

        
    def special(self):
        # in order to apply inversion, (255-R, 255-G, 255-B)
        
        if self.special_active is False:
            self.special_active = True

        else:
            self.special_active = False

    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:

        cur_color = self.layer

        # if the layer is empty, return start (the original code)
        if cur_color is None:
            return start
        #activating special depends on the situation
        elif self.special_active is True:
            cur_color = cur_color.apply(start, timestamp, x, y)
            new_color = ()
            for i in cur_color:
                new_color += (255 - i, )
            
            cur_color = new_color
            return cur_color

            #return cur_color.apply(255-cur_color[0], 255 - cur_color[1], 255 - cur_color[2])
        #if the user didnt activate special, just return the original conditions
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

 
        # use circular queue and array stack
        self.queue_A = CircularQueue()
        self.stack_A = ArrayStack() #set limitations
        self.isspecial = False


    def add(self, layer: Layer)->bool: 
        
        self.queue_A.append(layer)

        return True


    def erase(self)->bool:

        self.queue_A.serve() #removing the "oldest" element in the queue
    
        return True
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        
        #checks colour existance
        #for loop
        #circularqueue
        #add element into array

        #checking if the queue is empty

        tempqueue = self.queue_A


        if not self.queue_A.is_empty():
        
            if self.isspecial is not True:
                for i in range(0, self.queue_A.__len__):
                    new_lay = self.queue_A.serve()
                    new_lay.apply(start, timestamp, x, y) # it should produce colour 
            
            else: 

        else:
            return start
        
        #check if the colour is inverted
    

        pass
        


    def special(self)-> bool:

        queue_len = self.queue_A.__len__
        stack_len = self.stack_A.__len__

        for i in range(0, queue_len):
            self.stack_A.push(self.queue_A.serve())

        for i in range(0, stack_len):
            self.queue_A.append(self.stack_A.pop())
        
        self.isspecial = True
        return True

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
        self.srt_list = ArraySortedList()
        pass
    
    def add(self, layer: Layer) -> bool: # makes the layer "applying"
        self.srt_list.add(layer)
        
        return True # or "applying"

    def erase(self, layer: Layer) -> bool: # makes the layer not "applying"
        self.srt_list.delete_at_index(layer.index) # delete the layer at that index

        return False # or "not applying"
    
    def special(self,layer) -> bool:

        #self.srt_list = sorted(self.srt_list, key=str.lower) #create a list into lexicographic order
        # if number of element is even 
        #if len(self.srt_list % 2) == 0:
        #    self.srt_list.delete_at_index((len(self.srt_list))/2) # deletes a median item

        # if number of element is odd
        #else:
        #    len(self.srt_list % 2) == 1:


        #create sorted copy of original list
        lexi_list = sorted(self.srt_list, key=str.lower)
        mid = len(lexi_list) // 2

        if len(lexi_list) % 2: # if odd
            return lexi_list[mid]
        
        else: # if even
            return lexi_list[mid-1]+lexi_list[mid])/2


    def lexicographic_Order(txt):
        tup_lst = []
        for word in txt.split():
            for ch in word:
                if ch in "0123456789":
                    tup_lst.append((ch, word))
        return sorted(tup_lst)
    
    pass