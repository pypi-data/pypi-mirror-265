from typing import List, Dict
from glcidocs.pipelineparser import Workflow, Rule


class HTMLBuilder:

    def __init__(self, workflow: Workflow):
        self._show_pipelinename_column = False
        headers = ['Trigger', 'Variable', 'Default value', 'Required', 'Type', 'Choices']
        if workflow.pipeline_name_in_rules:
            headers.insert(0, 'Pipeline name')
            self._show_pipelinename_column = True
        self._docs = self.table(headers, workflow.rules)

    @property
    def docs(self) -> str:
        return self._docs

    def create_rule_rows(self, rule: Rule) -> str:
        get_row_var_cells = lambda v: [
            {'value': v.name},
            {'value': v.value},
            {'value': v.required_str},
            {'value': v.typename if v.typename else '-'},
            {'value': v.choices_str if v.choices_str else '-'}
        ]
        pipeline_name_row = [{'value': rule.pipeline_name, 'rowspan': len(rule.variables)}] if self._show_pipelinename_column else []
        first_row = self.row(
            pipeline_name_row
            + [{'value': f'if: {rule.condition}', 'rowspan': len(rule.variables)}]
            + get_row_var_cells(rule.variables[0])
        )
        other_rows = '\n'.join([self.row(get_row_var_cells(v)) for v in rule.variables[1:]])

        return first_row + other_rows

    def table(self, headers: List[str], rules: List[Rule]) -> str:
        return '\n'.join([
            '<table>',
            self.headers(headers),
            '\n'.join([self.create_rule_rows(r) for r in rules]),
            '</table>'
        ])

    def headers(self, headers: List[str]) -> str:
        return f'<tr>{"".join([f"<th>{h}</th>" for h in headers])}</tr>'

    def row(self, data: List[Dict[str, str]]) -> str:
        return f'<tr>{"".join([self.cell(v["value"], v.get("rowspan", None)) for v in data])}</tr>'

    def cell(self, value: str, rowspan=None) -> str:
        rowspan = f' rowspan="{rowspan}"' if rowspan and rowspan > 1 else ''
        return f'<td{rowspan}>{value}</td>'
