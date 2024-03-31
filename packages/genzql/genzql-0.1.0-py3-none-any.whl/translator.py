from zql.src.grammar import Grammar
from zql.src.parser import parse_ast
from zql.src.renderer import render_query
from zql.src.types import MaybeDialect


def translate(
    grammar: Grammar,
    source: str,
    source_dialect: MaybeDialect = None,
    target_dialect: MaybeDialect = None
) -> str:
    ast = parse_ast(grammar, source, source_dialect)
    target = render_query(grammar, ast, target_dialect)
    return target