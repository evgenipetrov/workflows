class BasePipeline:
    def __init__(self, project_name):
        self.project_name = project_name

    def add_arguments(self, parser):
        raise NotImplementedError("Must implement add_arguments")

    def execute(self, args):
        raise NotImplementedError("Must implement execute")
