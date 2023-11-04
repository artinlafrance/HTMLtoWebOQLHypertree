from tree import Node, WebOQLTree

with open('html_sample.html', 'r', encoding='utf-8') as file:
          html_content = file.read()

tree = WebOQLTree(html_content)
tree.format_file()
tree.get_tag_node()
print(tree.root.starting_tag_index)
print(tree.root.closing_tag_index)