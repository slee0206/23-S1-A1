from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
import layers
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem

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

    def __init__(self): 

        """

        Initialises a layer to be none to start
        while initialising an indication of whether the special has been activated

        :complexity: O(1)
        
        """

        self.layer = None
        self.special_active = False # status of special 

    def add(self, layer: Layer)-> bool:
        
        """

        Takes a layer as an input and set it as the layer

        input: layer
        output: boolean

        :complexity: O(1)
        
        """

        self.layer = layer
        return True 
    
    
    def erase(self, layer: Layer)-> bool: # we dont need layer for this 

        """

        Erases the saved single layer
        
        input: layer
        output: boolean

        :complexity: O(1)
        
        """        

        self.layer = None
        return True

        
    def special(self):

        """

        Checks if special has been activated and if its not active, make it active

        True = active
        False = Not activate
    
        :complexity: O(1)
        
        """
        
        if self.special_active is False:
            self.special_active = True

        else:
            self.special_active = False

    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:

        """

        Inverts the colour output by deducting the given layer tuple from 255.
        (255-R, 255-G, 255-B)

        input:  reference to instance (self)
                Start, timestamp, x, y

        output: tuple[int, int, int] : inverted layer OR original layer OR starting layer
        
        :complexity: O(n)
        
        """
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

        """

        Initialises a circualr queue, arraystack with the length of 1000. 
        This is because the length requirements are over 999.

        circular queue was selected as it provides flexibility in length and memory use.
        array stack was selected as a suitable container to reverse the element order.


        :complexity: O(1)
        
        """
 
        # use circular queue and array stack
        self.queue_A = CircularQueue(1000)
        self.stack_A = ArrayStack(1000) #set limitations
        self.isspecial = False


    def add(self, layer: Layer)->bool: 
        """

        adds a layer to the circular queue created earlier.

        input: reference to instances (self), layer
        output: boolean

        :complexity: O(1)
        
        """
     
        self.queue_A.append(layer)

        return True


    def erase(self, layer:Layer)->bool:

        """

        erases a layer from the circular queue created earlier.

        input: reference to instances (self), as it will be oldest element anyways.
        output: boolean 

        :complexity: O(1)
        
        """
        self.queue_A.serve() #removing the "oldest" element in the queue
    
        return True
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """

        checks if special has been activated 

        input: reference to instances (self)

        output: tuple[int, int, int] : original layer, reversed layer.

        :complexity: O(n)
        
        """

        if not self.queue_A.is_empty(): #checks colour existance
            current = start
            for i in range(0, len(self.queue_A)):
                new_lay = self.queue_A.serve()
                current = new_lay.apply(current, timestamp, x, y) # produce colour 
                self.queue_A.append(new_lay)
            return current
        return start
       

    def special(self)-> bool:

        """

        reverses the order of current layers with the use of ciruclar queue and stack.
        The logic involves: push the elements from the queue to stack and dequeue 

        input: reference to instances (self)

        output: boolean

        :complexity: O(n)
        
        """
        queue_len = len(self.queue_A)  
        stack_len = len(self.queue_A) 

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
        """

        initialising arraysorted list with the length of 1000
        initialising another arraysorted list with the length of 1000
        -> array sorted list provides automatic soring system which makes it easier for special to be implemented. 

        input: reference to instances (self)

        :complexity: O(1)

        """
        
        self.srt_list = ArraySortedList(1000)
        self.lexi_list = ArraySortedList(1000) 
        
    
    def add(self, layer: Layer) -> bool:
    
        """

        adds the given layer to the arraysorted list in the ListItem form, while setting the layer as "applying" status.
    

        input: reference to instances (self), layer
        output: boolean

        :complexity: O(1)
        
        """
     
        if self.srt_list.is_empty() is False:
            item = ListItem(layer, layer.index)
            self.srt_list.add(item)

            l_item = ListItem(layer, layer.name)
            self.lexi_list.add(l_item)
            return True 

        else:
            return False

    def erase(self, layer: Layer) -> bool: # makes the layer not "applying"

        """

    
        input: reference to instances (self), layer
        output: boolean

        :complexity: O(n)
        
        """

        if self.srt_list.is_empty() is False:
            item = ListItem(layer, layer.index)
            srt_idx = self.srt_list.index(item)
            self.srt_list.delete_at_index(srt_idx)

            l_item = ListItem(layer, layer.index)
            lex_idx = self.lexi_list.index(l_item)
            self.lexi_list.delete_at_index(lex_idx)

            return True
        
        else:
            return False
    
    def special(self) -> bool:

        """

        Of all currently applied layers, remove the one with median name, not the position.
        In order to complete this, the elements needs to be in lexicographical order.
        
        we will also consider the case of the number of element being even and odd where we pick the smaller name when its between two names.

        logic: 

        - assume that the elements are already in sorted order through the import of sorted array list.
        - it first sets the mid value of the element
        - it checks if the number of element is odd or even, through usage of modulo operation.
        - if its even, erases the name positioned -1 from the mid position. 

        input: reference to instances (self)

        output: boolean

        :complexity: O(1)
        
        """
    
        mid = (len(self.srt_list) // 2) #getting a mid value

        if len(self.srt_list) % 2 != 0 : # if odd
            self.erase(self.lexi_list[mid].value)
        
        else: # if even
            self.erase((self.lexi_list[mid - 1].value))


    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:


        """

        Of all currently applied layers, remove the one with median name, not the position.
        In order to complete this, the elements needs to be in lexicographical order.
        
        we will also consider the case of the number of element being even and odd where we pick the smaller name when its between two names.

        input:  reference to instances (self)
                start, timestamp, x, y

        output: tuple[int, int, int]

        :complexity: O(n)
        
        """

        if not self.srt_list.is_empty(): # if the list is not empty, procecess
            current = start

            for i in range(0, len(self.srt_list)):
                current = self.srt_list[i].value.apply(current, timestamp, x, y)
                
            return current

        return start