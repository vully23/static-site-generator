import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_parent_node_with_empty_children_list(self):
        # Should this raise an error or handle it differently?
        # Depends on your implementation requirements
        with self.assertRaises(ValueError):
            node = ParentNode("div", [])
            node.to_html()

    def test_parent_node_with_none_in_children(self):
        # Test handling of None in children list
        # You might want this to raise an error
        with self.assertRaises(ValueError):  # or whatever behavior you expect
            node = ParentNode("div", [LeafNode("p", "text"), None])
            node.to_html()

    def test_parent_node_with_props(self):
        # Test that props are correctly included
        node = ParentNode("div", [LeafNode("span", "hello")], {"class": "container"})
        self.assertEqual(node.to_html(), '<div class="container"><span>hello</span></div>')

    def test_deeply_nested_structure(self):
        # Test with multiple levels of nesting
        great_grandchild = LeafNode("b", "text")
        grandchild = ParentNode("span", [great_grandchild])
        child = ParentNode("div", [grandchild])
        parent = ParentNode("section", [child])
        self.assertEqual(
            parent.to_html(),
            "<section><div><span><b>text</b></span></div></section>"
        )

    def test_mixed_content(self):
        # Test with mix of LeafNode and ParentNode children
        parent = ParentNode("div", [
            LeafNode("p", "first paragraph"),
            ParentNode("ul", [LeafNode("li", "list item")]),
            LeafNode("p", "second paragraph")
        ])
        self.assertEqual(
            parent.to_html(),
            "<div><p>first paragraph</p><ul><li>list item</li></ul><p>second paragraph</p></div>"
        )
    
    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

if __name__ == "__main__":
    unittest.main()