class Node:
    def __init__(self, tag=None):
        self.parent = None
        self.children = []
        self.node_type = None

        self.tag = tag
        self.source = None
        self.text = None

        self.starting_tag_index = None
        self.closing_tag_index = None

    def set_tag(self, tag):
        self.tag = tag

    '''
    Formats the string and sets the source
    '''
    def set_source(self, source):
        source = source[:45]
        source = source.replace("\n", "")
        source += "..."
        self.source = source

    def set_text(self, text):
        self.text = text

    def set_starting_tag_index(self, index):
        self.starting_tag_index = index

    def set_closing_tag_index(self, index):
        self.closing_tag_index = index

    def print_node(self):
        return f"Tag: {self.tag} \n Source: {self.source} \n Text: {self.text}"
    
    def __repr__(self) -> str:
        return self.tag


class WebOQLTree:
    def __init__(self, source:str):
        self.source = source
        self.root:Node = None
        self.stack = []

        self.filter_out = ["!DOCTYPE", "meta"]

    '''
    Format the html file into a single line removing unnecessary white spaces
    '''
    def format_file(self):
        self.source = self.source.replace('\n', '').replace('\r', '')


    '''
    Filters tag outs and creates the root node if it encounters an "html" tag
    '''
    def filter_tags(self,tag, start_tag_index=None, closing_tag_index=None):
        result_found = any(word in tag for word in self.filter_out)
        if not result_found:
            #self.stack.append(tag)
            if "html" in tag:
                self.root = Node(tag)
                self.root.set_starting_tag_index(start_tag_index)
                self.root.set_closing_tag_index(closing_tag_index)
                self.stack.append(self.root)


    def get_tag_node(self):
        start_index_open = None
        start_index_close = None
        for index, char in enumerate(self.source):
            if char == "</":
                start_index_close = index
            elif char == "<":
                start_index_open = index
            elif char == ">":
                if start_index_open is not None:
                    tag = self.source[start_index_open:index+1]
                    self.filter_tags(tag, start_index_open)
                    start_index_open = None
                if start_index_close is not None:
                    tag = self.source[start_index_close:index+1]
                    self.filter_tags(tag, start_index_close)
                    start_index_close = None


    '''
    This function takes in the starting index of the tag and the starting index of its closing tag
    and iterates through the string to return its source.
    '''
    #def get_tags_source(self, start_tag_index, end_tag_index) -> str:
        