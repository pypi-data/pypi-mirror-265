from scoutbook_parser.parser import Parser
from pathlib import Path
from objexplore import explore


ROOT = Path(
    "/home/perkinsms/Projects/django-troop/django_troop/data/example_troop_scoutbook"
)


p = Parser(
    input_advancement=ROOT / "advancement.csv",
    input_personal=ROOT / "personal_data.csv",
    file_format="json",
)


explore(p)
