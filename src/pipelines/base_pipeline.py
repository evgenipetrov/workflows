class BasePipeline:
    def add_arguments(self, parser):
        raise NotImplementedError("Must implement add_arguments")

    def execute(self, args):
        raise NotImplementedError("Must implement execute")
