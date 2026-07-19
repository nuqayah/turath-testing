import assert from 'node:assert/strict'
import test from 'node:test'

import {
    BOOK_PM_MAX_INTEGER,
    BOOK_PM_SCHEMA_ARTIFACT_HASH,
    BOOK_PM_SCHEMA_ID,
    assert_book_pm_document_contract,
    assert_book_pm_node_contract,
    book_pm_attr_specs,
    book_pm_blocked_response_facts,
    book_image_source_from_dom,
    book_link_attrs_from_dom,
    book_link_dom_attrs,
    book_page_marker_attrs,
    book_pm_json_equal,
    book_pm_policy_accepts,
    book_printed_page_number,
    book_pm_steps_within_send_limits,
    canonical_book_services,
    canonical_book_pm_envelope,
    empty_book_pm_doc,
    new_book_page_marker_id,
} from './book-pm-model.js'

test('Book PM constructors produce only canonical attribute values', () => {
    assert.throws(() => book_page_marker_attrs('bad marker'), /invalid_pm_attr/)
    assert.deepEqual(book_image_source_from_dom('/api/books/book-assets/' + 'a'.repeat(40) + '/'), {
        kind: 'asset',
        hash: 'a'.repeat(40),
    })
    assert.equal(
        book_image_source_from_dom(
            'https://example.com/api/books/book-assets/' + 'a'.repeat(40) + '/',
        ),
        null,
    )
})
