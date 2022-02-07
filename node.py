"""
Node Data Structure
"""


class Node:
    def __init__(self, label, children=None):
        self.label = label
        self.children = {} if children is None else children

    def __str__(self):
        return str(self.label)

    def setLabel(self, label):
        self.label = label

    def getLabel(self):
        return self.label

    def setChild(self, children):
        if isinstance(children, dict):
            self.children = children

    def getChild(self):
        return self.children
