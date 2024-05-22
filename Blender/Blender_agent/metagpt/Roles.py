from metagpt.roles import Role
from Actions import *
class BlenderOperator(Role):
    name: str = "BlenderOperator"
    profile: str = "Operator"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([AddObjectToBlender])

class SceneVerifier(Role):
    name: str = "SceneVerifier"
    profile: str = "Verifier"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([VerifyBlenderScene])
