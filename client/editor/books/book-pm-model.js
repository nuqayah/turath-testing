const wire_identity = {nodes: {}, marks: {}}
const document_invariants = []
const BOOK_ASSET_HASH_RE = /^[0-9a-f]{40}$/
const BOOK_ASSET_PATH_RE = /^\/api\/books\/(?:[^/]+\/)*book-assets\//
const BOOK_ASSET_URL_RE = /^\/api\/books\/book-assets\/([0-9a-f]{40})\/$/

export function assert_book_pm_document_contract(doc) {
    assert_book_pm_contract(doc, document_invariants)
}

function assert_book_pm_contract(root, invariants) {
    const unique_values = invariants.map(invariant => {
        if (invariant.kind !== 'unique_node_attr') {
            throw new Error('unknown_book_pm_document_invariant')
        }
        return new Set()
    })
    const pending = [root]
    while (pending.length) {
        const node = pending.pop()
        assert_book_pm_attrs(wire_identity.nodes[node.type.name].attrs || {}, node.attrs)
        for (const mark of node.marks) {
            assert_book_pm_attrs(wire_identity.marks[mark.type.name].attrs || {}, mark.attrs)
        }
        invariants.forEach((invariant, index) => {
            if (node.type.name !== invariant.node) return
            const value = node.attrs[invariant.attr]
            if (unique_values[index].has(value)) throw new RangeError(invariant.error)
            unique_values[index].add(value)
        })
        for (let index = node.childCount - 1; index >= 0; index -= 1) {
            pending.push(node.child(index))
        }
    }
}

function assert_book_pm_attrs(specs, attrs) {
    if (Object.keys(attrs).length !== Object.keys(specs).length) {
        throw new RangeError('noncanonical_pm_doc')
    }
}

function normalize_book_url(value) {
    return typeof value === 'string' ? value : null
}

function book_url_path(value) {
    return value.split(/[?#]/, 1)[0]
}

export function book_image_source_from_dom(src_value) {
    const src = normalize_book_url(src_value, 'media_url')
    const hash = String(src || '').match(BOOK_ASSET_URL_RE)?.[1] || null
    if (src && BOOK_ASSET_PATH_RE.test(book_url_path(src)) && !hash) return null
    if (hash) return {kind: 'asset', hash}
    return src ? {kind: 'url', url: src} : null
}

export function book_image_dom_attrs(source) {
    if (source?.kind === 'asset') return {src: `/api/books/book-assets/${source.hash}/`}
    return source?.kind === 'url' ? {src: source.url} : {}
}
