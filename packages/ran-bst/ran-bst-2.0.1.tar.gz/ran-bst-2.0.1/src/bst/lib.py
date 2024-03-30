"""
Binary Search Tree Implementation

Author: Ran (01-ERFA)
Date created: 26/03/2024
Last modified: 29/03/2024

This module contains the implementation of a binary search tree (BST).
"""

from collections import deque
from dataclasses import dataclass
from typing import Any

@dataclass
class BinaryNode:
    value  : Any
    son0   = None
    son1   = None

    def __lt__(self, other):
        return isinstance(other, BinaryNode) and self.value <  other.value

    def __eq__(self, other):
        return isinstance(other, BinaryNode) and self.value == other.value

    def __gt__(self, other):
        return isinstance(other, BinaryNode) and self.value >  other.value

class BinarySearchTree:
    """
    Represents a binary search tree (BST) capable of storing elements of a specified type.
    
    Usage:
        bst = BinarySearchTree(int)

    Parameters:
        type: The type of elements to be stored in the binary search tree. It should support comparison
        operators such as ">" (greater than), "<" (less than), and "==" (equal to). Once the type is defined,
        the binary search tree can only work with elements of that type.

    Attributes:
        is_empty: True if the binary search tree has no elements.
        type: The type of elements in the binary search tree
        length: The number of elements in the binary search tree.
        height: The height of the binary search tree.
        min_value: The minimum element in the binary search tree.
        max_value: The maximum element in the binary search tree.

        __root: The root node of the binary search tree.
        __size: The number of elements in the binary search tree.
        __type: The type of elements stored in the binary search tree.
        
    Methods:
        pop(): Removes and returns the maximum element from the binary search tree.
        popleft(): Removes and returns the minimum element from the binary search tree.
        copy(): Returns a deep copy of the binary search tree.
        insert(*args): Inserts the specified elements into the binary search tree.
        remove(*args): Removes the specified elements from the binary search tree.
        search(*args): Checks if all the specified elements are present in the binary search tree.
        is_compatible(*args): Checks if all the elements in the provided arguments are compatible with the type stored in the binary search tree.
        clear(): Removes all nodes from the binary tree, leaving it empty.
        
        inorder(): Returns a list containing the elements of the binary search tree in sorted order (in-order traversal).
        preorder(): Returns a list containing the elements of the binary search tree in pre-order traversal order.
        postorder(): Returns a list containing the elements of the binary search tree in post-order traversal order.
        levelorder(): Returns a list containing the elements of the binary search tree in level-order traversal order.
        spiralorder(): Returns a list containing the elements of the binary search tree in spiral order.
        
        __repr__(): Returns a string representation of the binary search tree.
        __len__(): Returns the number of elements in the binary search tree.
        __iter__(): Returns an iterator for the binary search tree.
        __add__(other): Concatenates two binary search trees or appends an element of the tree's type to the tree.
        __radd__(other): Concatenates two binary search trees or appends an element of the tree's type to the tree (reversed).
        __sub__(other): Removes elements from the binary search tree based on another binary search tree or removes a single element if present.
        __contains__(other): Checks if a value exists in the binary search tree or checks if a binary search tree is contained within another binary search tree.
        __eq__(other): Checks if the binary search tree is equal to another binary search tree.
        __getitem__(index): Returns the element at the specified index in sorted order.
        __exists__(value): Checks if the specified value exists in the binary search tree.
    """

    def __init__(self, bst_type) -> None:
        import inspect
        self.__root = None
        self.__size = 0
        self.__type = bst_type if inspect.isclass(bst_type) else type(bst_type)

    def __repr__(self) -> str:
        """
        Returns a string representation of the binary search tree.

        Returns:
            A string representation of the binary search tree.
        """
        return f"BST({self.__type.__name__}):{repr(self.preorder())}"

    def __len__(self):
        """
        Returns the number of elements in the binary search tree.

        Returns:
            The number of elements in the binary search tree as an integer.
        """
        return self.__size
    
    def __iter__(self):
        """
        Returns an iterator for the binary search tree.

        Returns:
            An iterator for the binary search tree.
        """
        yield from self.inorder()

    def __add__(self, other):
        """
        Concatenates two binary search trees or appends an element of the tree's type to the tree.

        Parameters:
            other: Another binary search tree or an element of the tree's type.

        Returns:
            A new binary search tree containing the elements of both trees or the original tree with the appended element.

        Raises:
            TypeError: If the specified type of 'other' is not compatible with the type of elements in the binary search tree.
        """
        bst = self.copy()

        if isinstance(other, BinarySearchTree): bst.insert(*other.preorder())
        elif isinstance(other, self.__type): bst.insert(other)
        else: raise TypeError(f"unsupported operand type(s) for +: '{BinarySearchTree.__name__}({self.__type.__name__})' and '{other.__class__.__name__}'")

        return bst

    def __radd__(self, other):
        """
        Concatenates two binary search trees or appends an element of the tree's type to the tree (reversed).

        Parameters:
            other: Another binary search tree or an element of the tree's type.

        Returns:
            A new binary search tree containing the elements of both trees or the original tree with the appended element.

        Raises:
            TypeError: If the specified type of 'other' is not compatible with the type of elements in the binary search tree.
        """
        return self.__add__(other)

    def __sub__(self, other):
        """
        Removes elements from the binary search tree based on another binary search tree or removes a single element if present.

        Parameters:
            other: Another binary search tree or an element of the tree's type.

        Returns:
            A new binary search tree with elements removed based on the specified 'other' object.

        Raises:
            TypeError: If the specified type of 'other' is not compatible with the type of elements in the binary search tree.
        """
        bst = self.copy()
        
        if isinstance(other, BinarySearchTree): bst.remove(*other.preorder())
        elif isinstance(other, self.__type): bst.remove(other)
        else: raise TypeError(f"unsupported operand type(s) for -: '{BinarySearchTree.__name__}({self.__type.__name__})' and '{other.__class__.__name__}'")

        return bst

    def __contains__(self, other) -> bool:
        """
        Checks if a value exists in the binary search tree or checks if a binary search tree is contained within another binary search tree.

        Parameters:
            other: Another binary search tree or a value of the tree's type to search for.

        Returns:
            True if the specified value exists in the binary search tree or if the binary search tree 'other' is contained within the current binary search tree, False otherwise.

        Raises:
            TypeError: If the specified type of 'other' is not compatible with the type of elements in the binary search tree.
        """
        return self.search(*other.preorder()) if isinstance(other, BinarySearchTree) else self.search(other)

    def __eq__(self, other) -> bool:
        """
        Checks if the binary search tree is equal to another binary search tree.

        Parameters:
            other: Another binary search tree to compare with.

        Returns:
            True if the binary search tree is equal to the 'other' binary search tree, False otherwise.
        """
        return isinstance(other, BinarySearchTree) and self.__contains__(other) and other.__contains__(self)

    def __getitem__(self, index):
        """
        Returns the element at the specified index in the sorted order of the binary search tree.

        Parameters:
            index (int): The index of the element to retrieve.

        Returns:
            The element at the specified index in the sorted order of the binary search tree.

        Raises:
            IndexError: If the index is out of range.
        """
        try: return self.inorder()[index]
        except IndexError: raise IndexError("index out of range")

    def __exists__(self, value) -> bool:
        """
        Checks if the specified value exists in the binary search tree.

        Parameters:
            value: The value to check for existence in the binary search tree.

        Returns:
            True if the value exists in the binary search tree, False otherwise.
        """
        if not self.is_compatible(value) or self.is_empty: return False

        search  = BinaryNode(value)
        current = self.__root 

        while isinstance(current, BinaryNode):
            if search < current:
                if isinstance(current.son0, BinaryNode): current = current.son0
                else: return False
            elif search > current:
                if isinstance(current.son1, BinaryNode): current = current.son1
                else: return False
            else: return search == current
        return False

    @property
    def is_empty(self) -> bool:
        """True if the binary search tree has no elements."""
        return not isinstance(self.__root, BinaryNode)
    
    @property
    def length(self) -> int:
        """Number of elements in the binary search tree.""" 
        return self.__size
    
    @property
    def type(self) -> object:
        """Type of elements in the binary search tree."""
        return self.__type
    
    @property
    def min_value(self):
        """Minimum element in the binary search tree. None if the binary search tree is empty."""
        if self.is_empty: return None;

        current = self.__root
        while isinstance(current.son0, BinaryNode): current = current.son0

        return current.value
    
    @property
    def max_value(self):
        """Maximum element in the binary search tree. None if the binary search tree is empty."""
        if self.is_empty: return None;
        
        current = self.__root
        while isinstance(current.son1, BinaryNode): current = current.son1
        
        return current.value

    @property
    def height(self):
        """Height of the binary search tree."""
        if self.is_empty: return 0;

        queue = deque([(self.__root, 1)])
        max_height = 0

        while queue:
            node, level = queue.popleft()
            max_height  = max(max_height, level)

            if isinstance(node.son0, BinaryNode): queue.append((node.son0, level+1))
            if isinstance(node.son1, BinaryNode): queue.append((node.son1, level+1))
        return max_height

    def is_compatible(self, *args) -> bool:
        """
        Checks if all the elements in the provided arguments are compatible with the type stored in the binary search tree.

        Parameters:
            *args: The elements to be checked for compatibility.

        Returns:
            bool: True if all elements are compatible with the type stored in the binary search tree, False otherwise.
        """
        return all(isinstance(arg, self.__type) for arg in args)

    def clear(self):
        """Removes all nodes from the binary tree, leaving it empty."""
        self.__root = None
        self.__size = 0
        return self

    def insert(self, *args):
        """
        Inserts the specified elements into the binary search tree.

        Parameters:
            *args: The elements to be inserted into the binary search tree.

        Raises:
            TypeError: If any value is not of the same type as the elements stored in the binary search tree.
        """
        if not self.is_compatible(*args): raise TypeError (f"expected an '{self.__type.__name__}', but received a incompatible type")
        
        for value in args:
            insert = BinaryNode(value)
            if self.is_empty: self.__root = insert; self.__size+=1; continue;

            current = self.__root
            while isinstance(current, BinaryNode):
                if insert < current: 
                    if not isinstance(current.son0, BinaryNode):
                        current.son0 = insert
                        self.__size+=1
                        break
                    else: current = current.son0
                elif insert > current:
                    if not isinstance(current.son1, BinaryNode):
                        current.son1 = insert
                        self.__size+=1
                        break
                    else: current = current.son1
                else: break;
        return self
    
    def remove(self, *args):
        """
        Removes the specified elements from the binary search tree.

        Parameters:
            *args: The elements to be removed from the binary search tree.
    
        Raises:
            TypeError: If any value is not of the same type as the elements stored in the binary search tree.
        """
        if not self.is_compatible(*args): raise TypeError (f"expected an '{self.__type.__name__}', but received a incompatible type")

        for value in args:
            if self.is_empty: break

            current_node = self.__root
            parent       = None
            remove_node  = BinaryNode(value)
            
            while isinstance(current_node, BinaryNode):
                if remove_node < current_node:
                    parent = current_node
                    current_node = current_node.son0
                elif remove_node > current_node:
                    parent = current_node
                    current_node = current_node.son1
                else:
                    if not isinstance(current_node.son0, BinaryNode) or not isinstance(current_node.son1, BinaryNode):
                        if not isinstance(current_node.son0, BinaryNode):
                            next_node = current_node.son1
                        else: next_node = current_node.son0

                        if isinstance(parent, BinaryNode):
                            if parent.son0 == current_node: parent.son0 = next_node
                            else: parent.son1 = next_node
                        else: self.__root = next_node
                    else:
                        succesor = current_node.son1
                        succesor_parent = current_node

                        while isinstance(succesor.son0, BinaryNode):
                            succesor_parent = succesor
                            succesor = succesor.son0
                        
                        current_node.value = succesor.value

                        if succesor_parent.son0 == succesor: succesor_parent.son0 = succesor.son1
                        else: succesor_parent.son1 = succesor.son1
                    self.__size-=1
                    break
        return self

    def search(self, *args):
        """
        Checks if all the specified elements are present in the binary search tree.

        Parameters:
            *args: The elements to be checked for presence in the binary search tree.

        Returns:
            bool: True if all specified elements are present in the binary search tree, False otherwise.
        """
        return all(self.__exists__(a) for a in args)

    def copy(self):
        """
        Creates a deep copy of the binary search tree.

        Returns:
            A deep copy of the binary search tree.
        """
        from copy import deepcopy
        return deepcopy(self)
    
    def pop(self):
        """
        Removes and returns the maximum element from the binary search tree.

        Returns:
            The maximum element in the binary search tree, or None if the tree is empty.
        """
        if self.is_empty: return None;

        current = self.__root
        last    = None
        while isinstance(current.son1, BinaryNode):
            last    = current
            current = current.son1
        
        res = current.value
        if isinstance(last, BinaryNode): last.son1 = current.son0
        else: self.__root = current.son0
        self.__size-=1
        return res
    
    def popleft(self):
        """
        Removes and returns the minimum element from the binary search tree.

        Returns:
            The minimum element in the binary search tree, or None if the tree is empty.
        """
        if self.is_empty: return None;

        current = self.__root
        last    = None
        while isinstance(current.son0, BinaryNode):
            last    = current
            current = current.son0
        
        res = current.value
        if isinstance(last, BinaryNode): last.son0 = current.son1
        else: self.__root = current.son1
        self.__size-=1
        return res
    
    def stabilize(self):
        """Balances the binary search tree to improve efficiency."""
        inorder_nodes = self.inorder()
        if not inorder_nodes: return self
        
        m = len(inorder_nodes) // 2
        self.__root = BinaryNode(inorder_nodes[m])

        stack = [(self.__root, 0, inorder_nodes[m+1:]), (self.__root, 1, inorder_nodes[:m])]

        while stack:
            parent, son, nodes = stack.pop()
            if not nodes: continue

            m = len(nodes) // 2
            node = BinaryNode(nodes[m])

            if bool(son): parent.son0 = node
            else: parent.son1 = node
            
            stack.append((node, 0, nodes[m+1:]))
            stack.append((node, 1, nodes[:m]))
        
        return self

    def inorder(self) -> list:
        """
        Returns a list containing the elements of the binary search tree in sorted order (in-order traversal).

        Returns:
            A list containing the elements of the binary search tree in sorted order.
        """
        if self.is_empty: return []

        nodes   = []
        stack   = []
        current = self.__root

        while True:
            if isinstance(current, BinaryNode):
                stack.append(current)
                current = current.son0
            elif stack:
                current = stack.pop()
                nodes.append(current.value)
                current = current.son1
            else: break;
        
        return nodes
    
    def preorder(self) -> list:
        """
        Returns a list containing the elements of the binary search tree in pre-order traversal order.

        Returns:
            A list containing the elements of the binary search tree in pre-order traversal order.
        """
        if self.is_empty: return []

        nodes   = []
        stack   = [self.__root]

        while stack:
            current = stack.pop()
            nodes.append(current.value)

            if isinstance(current.son1, BinaryNode): stack.append(current.son1)
            if isinstance(current.son0, BinaryNode): stack.append(current.son0)
        
        return nodes
    
    def postorder(self) -> list:
        """
        Returns a list containing the elements of the binary search tree in post-order traversal order.

        Returns:
            A list containing the elements of the binary search tree in post-order traversal order.
        """
        if self.is_empty: return []

        nodes = []
        stack = [self.__root]

        while stack:
            current = stack.pop()
            nodes.append(current.value)

            if isinstance(current.son0, BinaryNode): stack.append(current.son0)
            if isinstance(current.son1, BinaryNode): stack.append(current.son1)

        return nodes[::-1]
    
    def levelorder(self) -> list:
        """
        Returns a list containing the elements of the binary search tree in level-order traversal order.

        Returns:
            A list containing the elements of the binary search tree in level-order traversal order.
        """
        if self.is_empty: return []

        nodes = []
        queue = deque([self.__root])

        while queue:
            node = queue.popleft()
            nodes.append(node.value)

            if isinstance(node.son0, BinaryNode): queue.append(node.son0)
            if isinstance(node.son1, BinaryNode): queue.append(node.son1)

        return nodes
    
    def spiralorder(self) -> list:
        """
        Returns a list containing the elements of the binary search tree in spiral-order traversal order.

        Returns:
            A list containing the elements of the binary search tree in spiral-order traversal order.
        """
        if self.is_empty: return []
        
        nodes = []
        queue = deque([self.__root])
        left_to_right = True

        while queue:
            level_size  = len(queue)
            level_nodes = []

            for _ in range(level_size):
                if left_to_right:
                    node = queue.popleft()
                    level_nodes.append(node.value)
                    if isinstance(node.son0, BinaryNode): queue.append(node.son0)
                    if isinstance(node.son1, BinaryNode): queue.append(node.son1)
                else: 
                    node = queue.pop()
                    level_nodes.append(node.value)
                    if isinstance(node.son1, BinaryNode): queue.appendleft(node.son1)
                    if isinstance(node.son0, BinaryNode): queue.appendleft(node.son0)

            nodes.extend(level_nodes)
            left_to_right = not left_to_right

        return nodes
    
