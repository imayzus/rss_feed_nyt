import pydantic

class RiskCategory(pydantic.BaseModel):
    condition: str
    risk: str

class Gene(pydantic.BaseModel):
    gene: str
    riskCategories: list[RiskCategory]
    # sort_value: int = 0
    number_high_risk: int = 0
    number_inconclusive: int = 0
    number_low: int = 0


class Result(pydantic.BaseModel):
    result: list[Gene]


class SortedResult(pydantic.BaseModel):
    high_no_inconclusive: list[Gene] = []
    high_with_inconclusive: list[Gene] = []
    low_with_inconclusive: list[Gene] = []
    low_no_inconclusive: list[Gene] = []
