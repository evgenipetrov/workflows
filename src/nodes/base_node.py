class BaseNode:
    def execute(self, input_data):
        """Execute should be implemented by each specific node class."""
        raise NotImplementedError("Each node must implement the 'execute' method.")
