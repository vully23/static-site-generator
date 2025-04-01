import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is another test", TextType.ITALIC)
        node4 = TextNode("Here's a code block test", TextType.CODE)
        node5 = TextNode("Link node test", TextType.LINK, "https://www.rtarchive.org")
        node6 = TextNode("Link node test", TextType.LINK, "https://www.rtarchive.org")
        node7 = TextNode("Image with no url", TextType.IMAGE, None)
        self.assertEqual(node, node2)
        self.assertNotEqual(node3, node4)
        self.assertNotEqual(node3, node5)
        self.assertEqual(node5, node6)
        self.assertNotEqual(node4, node7)
    
    def test_equality_with_same_properties(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_inequality_with_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node_different = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node_different)
    
    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )


if __name__ == "__main__":
    unittest.main()