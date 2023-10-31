# chat_components.py

class ChatComponent:
    def accept(self, visitor):
        pass

class Message(ChatComponent):
    def __init__(self, role, content):
        self.role = role
        self.content = content

    def accept(self, visitor):
        visitor.visit_message(self)

class ChatComposite(ChatComponent):
    def __init__(self):
        self.children = []

    def add(self, child):
        self.children.append(child)

    def accept(self, visitor):
        visitor.visit_composite(self)
        for child in self.children:
            child.accept(visitor)

class ChatVisitor:
    def visit_message(self, message):
        print(f"{message.role}: {message.content}")

    def visit_composite(self, composite):
        print("Start of Chat")
