from pydantic import BaseModel

class TuConsultaVariables(BaseModel):
    variable1: str
    variable2: int

class TuConsulta:
    def __init__(self, variables: TuConsultaVariables):
        self.query = """
        query($variable1: String, $variable2: Int) {
          tuConsulta(variable1: $variable1, variable2: $variable2) {
            tuCampo
          }
        }
        """
        self.variables = dict(variables)
