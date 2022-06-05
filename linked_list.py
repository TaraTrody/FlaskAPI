class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node

class LinkedList:
    def __init__(self):
        self.head = None
        self.last_node = None    

    def print_ll(self):
        ll_string = ""
        node = self.head
        if node is None:  
            print(None)
        
        while node: # while node is not equal to non
            ll_string += f" {str(node.data)} -->"
            node = node.next_node
        ll_string += " None"
        print(ll_string)

    def insert_beginning(self, data):
        if self.head is None: #if the ll is empty 
            self.head = Node(data, None) # set the head to the new node that points to None
            self.last_node = self.head # set the last node to be the head bc there's only one node in the list
 
        new_node = Node(data, self.head) 
        self.head = new_node 

    def insert_at_end(self, data):
        if self.head is None: 
            self.insert_beginning(data) 
            return
      
        self.last_node.next_node = Node(data, None) 
        self.last_node = self.last_node.next_node



