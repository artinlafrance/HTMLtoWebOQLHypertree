from bs4 import BeautifulSoup

class Node:
    def __init__(self):
        self.parent = None
        self.children = []
        self.node_type = None

        self.tag = None
        self.source = None
        self.text = None

    def set_tag(self, tag):
        self.tag = tag

    def set_source(self, source):
        self.source = source

    def set_text(self, text):
        self.text = text

    def print_node(self):
        return f"Tag: {self.tag} \n Source: {self.source} \n Text: {self.text}"


class WebOQLTree:
    def __init__(self, source):
        self.source = source
        self.soup = BeautifulSoup(source, 'html.parser')
        
        self.head = None
        self.tail = None
        self.children = []

    def get_head_node(self):
        self.head = Node()
        self.head.set_tag("html") 
        self.head.set_source(self.soup.find("html"))
        self.head.set_text(self.soup.find("title"))