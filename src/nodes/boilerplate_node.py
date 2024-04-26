from src.nodes.base_node import BaseNode


class BoilerplateNode(BaseNode):
    def execute(self, input_data):
        print("BoilerplateNode processing:", input_data)
        return input_data
