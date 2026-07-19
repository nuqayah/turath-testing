function book_image_source_from_dom() {
    return null
}

function define_book_image() {
    return {
        parseDOM: [
            {
                tag: 'img',
                getAttrs: dom => {
                    const source = book_image_source_from_dom(
                        dom.getAttribute('src'),
                        dom.getAttribute('data-book-asset'),
                    )
                    if (!source) return false
                    return {
                        source,
                        width: null,
                        height: null,
                        alt: null,
                        title: null,
                    }
                },
            },
        ],
    }
}

export {define_book_image}
