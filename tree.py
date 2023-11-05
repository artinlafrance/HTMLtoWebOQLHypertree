import re

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
        self.formated_source = self.format_file()

        self.root:Node = None
        self.stack = []

        self.filter_out = ["!DOCTYPE", "meta"]


    '''
    Removes all the attributes from the html file before parsing 
    '''
    def remove_attributes(self):
        tag_with_attributes = re.compile(r'<([a-zA-Z]+)(?:\s+[^>]+)>')
        cleaned_html = re.sub(tag_with_attributes, r'<\1>', self.source)
        return cleaned_html


    '''
    Format the html file into a single line removing unnecessary white spaces
    '''
    def format_file(self):
        parsed_contents = self.remove_attributes()
        parsed_contents = parsed_contents.replace('\n', '').replace('\r', '')
        return parsed_contents


    '''
    Filters tag outs and creates the root node if it encounters an "html" tag
    '''
    def validate_tag(self,tag) -> bool:
        result_found = any(word in tag for word in self.filter_out)
        if not result_found:
            return True
        else: 
            return False
    

    def get_tag_node(self):
        opening_tags = []
        index = 0
        while index < len(self.formated_source):
            if self.formated_source[index] == "<":
                closing_index = self.formated_source.find(">", index)
                if closing_index != -1:
                    tag = self.formated_source[index:closing_index + 1] #Gets the tag
                    if self.validate_tag(tag) == False:
                        index += 1
                        continue
                    if tag.startswith("</") and opening_tags:
                        # It's a closing tag, check if it matches the last opening tag
                        last_opening_tag = opening_tags.pop()
                        last_opening_tag.set_closing_bracket_index(index, closing_index)
                        if tag[2:-1] != last_opening_tag.tag:
                            print("Error: Mismatched tags - <{}> and </{}>".format(last_opening_tag, last_opening_tag))
                    else:
                        # It's an opening tag, add it to the list of opening tags
                        node = Node(tag[1:-1])
                        node.set_open_bracket_index(index, closing_index)
                        self.stack.append(node)
                        opening_tags.append(node)
                    index = closing_index + 1
                else:
                    # Invalid tag, move to the next character
                    index += 1
            else:
                # Move to the next character if not a tag
                index += 1


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