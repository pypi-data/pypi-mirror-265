import re

from ruamel.yaml import YAML
from typing import Dict, List

from glcidocs.errors import BadVariableCommentFormatError


class Variable:

    _regex_value_regex = '[a-zA-Z0-9-_\.]'
    _regex_group_req = '(?P<required>required\s?)?'
    _regex_group_type = '(?P<type>:[a-zA-Z]+)?'
    _regex_group_opt = property(lambda s: f'(?P<options>{s._regex_value_regex}+(\|{s._regex_value_regex}+)*)?')
    _regex = property(lambda s: f'^#\s*{s._regex_group_req}{s._regex_group_type}{s._regex_group_opt}$')

    def __init__(self, name: str, value: str, comment: str):
        self._name = name
        self._value = value
        self._required = None
        self._choices = []
        self._typename = ''

        if (comment := comment.strip()) and comment != '#':
            if (matched := re.fullmatch(self._regex, comment)) is None:
                raise BadVariableCommentFormatError(f'Variable comment ({comment}) has invalid format. Valid format: {self._regex}')
            if matched['options'] and matched['type']:
                raise BadVariableCommentFormatError(f'Variable comment ({comment}) has invalid format. Valid format: {self._regex}')

            self._required = bool(matched['required'])
            self._choices = list(set(matched['options'].split('|'))) if matched['options'] else []
            self._typename = matched['type'][1:] if matched['type'] else None

    @property
    def name(self) -> str:
        return self._name

    @property
    def key(self) -> str:
        return self._name

    @property
    def value(self) -> str:
        return self._value

    @property
    def required(self) -> bool:
        return self._required

    @property
    def required_str(self) -> str:
        return None if self._required is None else 'Yes' if self._required else 'No'

    @property
    def optional(self) -> bool:
        return None if self._required is None else not self._required

    @property
    def choices(self) -> List[str]:
        return self._choices

    @property
    def choices_str(self) -> str:
        return ' '.join(self._choices) if self._choices else ''

    @property
    def typename(self) -> str:
        return self._typename


class Rule:

    def __init__(self, rule: Dict):
        self._pipeline_name = ''
        self._condition = rule['if']
        self._variables = [
            Variable(
                name=key,
                value=rule['variables'][key],
                comment=c[2].value if (c := rule['variables'].ca.items.get(key, None)) else ''
            ) for key in rule.get('variables', {}) if key != '_PIPELINE_NAME'
        ]
        self._pipeline_name = rule.get('variables').get('_PIPELINE_NAME', '')

    @property
    def condition(self) -> str:
        return self._condition

    @property
    def variables(self) -> List[Variable]:
        return self._variables

    @property
    def pipeline_name(self) -> str:
        return self._pipeline_name


class Workflow:

    _regex_pipeline_source = '\$CI_PIPELINE_SOURCE\s==\s[\'"]?(web|pipeline|api|trigger)[\'"]?'

    @classmethod
    def _include_rule(cls, rule_if: str) -> bool:
        return bool(re.search(cls._regex_pipeline_source, rule_if))

    def __init__(self, workflow: Dict):
        self._pipeline_name = workflow.get('name', '')
        self._rules = [Rule(r) for r in workflow['rules'] if self._include_rule(r['if'])]

    @property
    def rules(self) -> List[Rule]:
        return self._rules

    @property
    def pipeline_name(self) -> str:
        return self._pipeline_name

    @property
    def pipeline_name_in_rules(self):
        return any(r.pipeline_name for r in self.rules)


class CiFileParser:

    def __init__(self, filepath: str):
        with open(filepath) as f:
            pipeline = YAML().load(f)
        self._workflow = Workflow(pipeline['workflow'])

    @property
    def workflow(self) -> Workflow:
        return self._workflow
