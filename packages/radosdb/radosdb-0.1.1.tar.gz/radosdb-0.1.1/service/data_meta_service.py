from radosdb.repo.mongo_data_meta_repo import MongoDataMetaRepo


class DataMetaService:
    def __init__(self, repo: MongoDataMetaRepo):
        self.repo = repo

    def update_max_eff(self, name: str, eff: int):
        return self.repo.update_max_eff(name, eff)

    def update_eff(self, name: str, eff: int):
        return self.repo.update_eff(name, eff)

    def query_eff(self, name):
        return self.repo.query_eff(name)

    def reset_eff(self, name):
        return self.repo.reset_eff(name)

    def find_data(self, name):
        return self.repo.find_data(name)

    def insert_data(self,
                    name: str = None,
                    data_type: dict = None,
                    eff: int = None,
                    expression: dict = None,
                    should_update: bool = None,
                    perfData: str = None,
                    must_store: bool = None,
                    depth: int = None
                    ):

        return self.repo.insert_data(name,
                    data_type,
                    eff,
                    expression,
                    should_update,
                    perfData,
                    must_store,
                    depth)
