

class HTMLNode():
    def __init__(self, tag: str = None, value: str = None, children: list = None, attributes: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.attributes = attributes
        
    def to_html(self):
        raise NotImplementedError("Child classes will override this method to render themselves as HTML")
    
    def props_to_html(self):
        if self.attributes is None:
            return ''
        return ''.join([f' {key}="{value}"' for key, value in self.attributes.items()])
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.tag}, {self.value}, {self.children}, {self.attributes})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, attributes: dict = None):
        super().__init__(tag, value, attributes=attributes)
        
    def to_html(self):
        if self.value is None:
            raise ValueError("No value found")
        if self.tag is None:
            return f"{self.value}"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, attributes: dict = None):
        super().__init__(tag, children=children, attributes=attributes)

    def to_html(self):
        if self.tag is None:
            raise ValueError("No tag found")
        if self.children is None:
            raise ValueError("Children must be a list of HTMLNode objects")
        children_html = ''.join([child.to_html() for child in self.children])
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"