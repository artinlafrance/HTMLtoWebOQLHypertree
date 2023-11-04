class Node:
    def __init__(self, tag=None):
        self.parent = None
        self.children = []
        self.node_type = None

        self.tag = tag
        self.source = None
        self.text = None

        self.open_bracket_starting_index = None
        self.open_bracket_closing_index = None

        self.closing_bracket_starting_index = None
        self.closing_bracket_closing_index = None

    def set_tag(self, tag):
        self.tag = tag

    
    def set_open_bracket_index(self, startIndexPos, endIndexPos):
        self.open_bracket_starting_index = startIndexPos
        self.open_bracket_closing_index = endIndexPos


    def set_closing_bracket_index(self, startIndexPos, endIndexPos):
        self.closing_bracket_starting_index = startIndexPos
        self.closing_bracket_closing_index = endIndexPos

    '''
    Formats the string and sets the source
    '''
    def set_source(self, source):
        source = source[:100]
        source = source.replace("\n", "")
        if source[-1] != '>':
            source += "..."
        self.source = source

    def set_text(self, text):
        self.text = text

    '''
    Debug purposes : Prints the indexes of all the brackets.
    '''
    def get_all_bracket_index(self):
        return f"Open bracket indexes : {self.open_bracket_starting_index}, {self.open_bracket_closing_index} \n Close bracket indexes : {self.closing_bracket_starting_index}, {self.closing_bracket_closing_index}"

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
    def filter_tags(self,tag, starting_index, closing_index):
        result_found = any(word in tag for word in self.filter_out)
        if not result_found:
            node = Node()
            stack_index = self.check_tag_in_stack(tag[2:])
            if "<html" in tag:
                self.root = Node(tag)
                self.root.set_open_bracket_index(starting_index, closing_index)
                self.stack.append(self.root)
            elif "</html" in tag:
                self.root.set_closing_bracket_index(starting_index, closing_index)
                self.get_tags_source(self.root)
            else:
                #Push the tag 
                if "<" in tag and "</" not in tag:
                    node.set_tag(tag)
                    node.set_open_bracket_index(starting_index, closing_index)
                    self.stack.append(node)
                if "</" in tag and stack_index != -1 :
                    self.stack[stack_index].set_closing_bracket_index(starting_index, closing_index)
                    self.get_tags_source(self.stack[stack_index])
                    self.get_tags_text(self.stack[stack_index])
    

    '''
    Checks to see if a substring (tag) is in the stack.
    If it is it returns the Index. If not it returns false

    Something needs to be fixed in this though
    '''
    def check_tag_in_stack(self, substring):
        for index, node in enumerate(self.stack):    
            if hasattr(node, 'tag') and substring in node.tag:
                return index
        return -1
    

    def get_tag_node(self):
        starting_index = None
        for index, char in enumerate(self.source):
            if char == "<":
                starting_index = index
            elif char == ">":
                if starting_index is not None:
                    tag = self.source[starting_index:index+1]
                    self.filter_tags(tag, starting_index, index)
                    starting_index = None


    '''
    This function takes in the starting index of the tag and the ending index of its closing tag
    and gets the string between each index and sets its source
    '''
    def get_tags_source(self, Node:Node):
        node_source = self.source[Node.open_bracket_starting_index:Node.closing_bracket_closing_index+1]
        Node.set_source(node_source)


    '''
    This function searches for the Text portion of a Node 
    '''
    def get_tags_text(self, Node:Node, isRootNode = False):
        string_to_search = self.source[Node.open_bracket_closing_index+1:Node.closing_bracket_starting_index]
        if (isRootNode is True or "head" in Node.tag):
            start_string_index = string_to_search.find("<title>")
            end_string_index = string_to_search.find("</title>")
            text = string_to_search[start_string_index+7:end_string_index]
            Node.set_text(text)
        else:
            Node.set_text(string_to_search)