from tree import Node, WebOQLTree

with open('html_sample.html', 'r', encoding='utf-8') as file:
          html_content = file.read()

tree = WebOQLTree(html_content)
tree.format_file()
tree.get_tag_node()
tree.get_tags_text(tree.root, True)
print(tree.stack[10].get_all_bracket_index())