from typing import Any

import orjson
import re

BOOK_PM_DOCUMENT_INVARIANTS = [
    {'kind': 'unique_node_attr', 'node': 'bookPageMarker', 'attr': 'id', 'error': 'duplicate_page_marker_id'}
]
BOOK_PM_NODE_ATTR_SPECS = {'bookPageMarker': {}}
BOOK_PM_MARK_ATTR_SPECS = {}
MAX_SAFE_INTEGER = 9_007_199_254_740_991


def book_page_marker_node(
    marker_id: str,
    *,
    printed_page_raw: str | None = None,
    number: int | None = None,
    non_author: bool = False,
    services: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    attrs = {
        'id': marker_id,
        'printedPageRaw': printed_page_raw,
        'number': number,
        'nonAuthor': non_author,
        'services': list(services or []),
    }
    _validate_book_pm_contract_attrs(BOOK_PM_NODE_ATTR_SPECS['bookPageMarker'], attrs)
    return {'type': 'bookPageMarker', 'attrs': attrs}


def canonicalize_book_pm_text(text: str | None) -> str:
    return _book_pm_envelope(parse_book_pm_envelope(text)['doc'])


def _same_json_value(left: Any, right: Any) -> bool:
    return orjson.dumps(left, option=orjson.OPT_SORT_KEYS) == orjson.dumps(
        right, option=orjson.OPT_SORT_KEYS
    )


def legacy_volume_text_from_book_pm_doc(doc_json: dict[str, Any]) -> str:
    pages: list[str] = []
    for marker, blocks in iter_book_pm_page_segments(doc_json):
        pages.append(str((marker, blocks)))
    return ''.join(pages)


def _validate_book_pm_contract_doc(doc: dict[str, Any]) -> None:
    unique_values = [set() for _ in BOOK_PM_DOCUMENT_INVARIANTS]

    for node in _iter_book_pm_nodes(doc):
        node_type = node['type']
        _validate_book_pm_contract_attrs(BOOK_PM_NODE_ATTR_SPECS[node_type], node.get('attrs') or {})
        for mark in node.get('marks') or ():
            _validate_book_pm_contract_attrs(BOOK_PM_MARK_ATTR_SPECS[mark['type']], mark.get('attrs') or {})
        for invariant, seen in zip(BOOK_PM_DOCUMENT_INVARIANTS, unique_values, strict=True):
            if node_type != invariant['node']:
                continue
            value = (node.get('attrs') or {}).get(invariant['attr'])
            if value in seen:
                raise ValueError(invariant['error'])
            seen.add(value)


def _validate_book_pm_contract_attrs(specs: dict[str, Any], attrs: dict[str, Any]) -> None:
    if set(attrs) != set(specs):
        raise ValueError('noncanonical_pm_doc')


def _clean_page_raw(value: str) -> str:
    return value.strip()


def book_printed_page_number(value: Any) -> int | None:
    cleaned = _clean_page_raw(value if isinstance(value, str) else '')
    if not re.fullmatch(r'[0-9]+', cleaned):
        return None
    parsed = int(cleaned)
    return parsed if parsed <= MAX_SAFE_INTEGER else None
