from tree import Node, WebOQLTree

with open('html_sample.html', 'r', encoding='utf-8') as file:
          html_content = file.read()

tree = WebOQLTree(html_content)
tree.get_tag_node()
