class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is not None:
            attribute_string = ""
            for key in self.props.keys():
                attribute_string += f' {key}="{self.props[key]}"'
            return attribute_string
        return ""
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("leaf nodes must have values")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children=children, props=props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("must have tag")
        if not self.children:
            raise ValueError("must have children")
        for child in self.children:
            if child is None:
                raise ValueError("Children cannot be None")
        props_str = self.props_to_html()
        children_to_html = ""
        for i in map(lambda child: child.to_html(), self.children):
            children_to_html += str(i)
        return f"<{self.tag}{props_str}>" + children_to_html + f"</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"