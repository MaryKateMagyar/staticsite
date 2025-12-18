from textnode import TextType, TextNode

def main():
    test = TextNode("This is some dummy text", TextType.LINK, "www.boot.dev")
    print(test)

if __name__ == "__main__":
    main()