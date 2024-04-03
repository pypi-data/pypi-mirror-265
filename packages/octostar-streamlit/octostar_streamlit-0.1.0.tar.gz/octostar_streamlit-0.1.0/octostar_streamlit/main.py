from humps import camelize
from pydantic import BaseModel

from octostar_streamlit.core.params_base_model import ParamsBaseModel

#
# Experiment of automatically converting python conventionally named variables to camelCase
#

class Test(ParamsBaseModel):
    test_value: str
    another_test_value: int

test = Test(test_value="test", another_test_value=1)
print(test.model_dump(by_alias=True))
