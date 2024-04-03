from __future__ import annotations

from markupsafe import Markup
from ormspace import model as md



class SpaceModel(md.Model):
    
    def markup(self) -> Markup:
        raise NotImplementedError
    
    async def setup_instance(self):
        pass


    
class SpaceSearchModel(SpaceModel, md.SearchModel):
    pass