import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_empty_props_to_html(self):
        node = HTMLNode()
        self.assertEqual("", node.props_to_html())

    def test_props_to_html(self):
        node2 = HTMLNode("p", "some text", "r", {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(' href="https://www.google.com" target="_blank"', node2.props_to_html())
    
    def test_repr(self):
        node3 = HTMLNode("h1", "sbgr", None, {"href": "https://www.google.com", "target": "_blank",})
        node4 = HTMLNode("h2", "4as3yn", None, None)
        self.assertEqual("HTMLNode(h1, sbgr, None, {'href': 'https://www.google.com', 'target': '_blank'})", repr(node3))
        self.assertEqual("HTMLNode(h2, 4as3yn, None, None)", repr(node4))
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

if __name__ == "__main__":
    unittest.main()