Credits
=======

`sphobjinv` is authored and maintained by Brian Skinn
([Blog](https://bskinn.github.io))
([Mastodon](https://fosstodon.org/@btskinn)).

The idea for the project came about as I was starting to deepen my expertise
with Sphinx, and found it hugely frustrating to debug cross-references to
objects in code. I discovered the `objects.inv` files relatively quickly, but
struggled with trying to get at the actual object information. At the time
(2016), the ability to
[execute `sphinx.ext.intersphinx` as a module](https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#showing-all-links-of-an-intersphinx-mapping-file)
hadn't yet been documented (that happened in
[2018](https://github.com/sphinx-doc/sphinx/commit/7aaba1758a4622298d15339fddd8556eb221af86)),
and a fair bit of searching didn't turn up anything promising.

Once I dug into the Sphinx code to figure out how to zlib-decompress the object
data, it was relatively straightforward to put together the initial v1.0 of
`sphobjinv`, which could only (de)compress `objects.inv` files to/from
plaintext. As I started to use it regularly in my own documentation work, it
became clear that there would be significant advantages to also implement object
searches, especially in large documentation sets. Also, it seemed likely that a
robust API for creation/manipulation of inventory contents would be useful, in
order to assist with things like scraping a non-Sphinx website to generate an
`objects.inv` for cross-referencing in other docs. This led to the current
object-oriented API of `sphobjinv` v2.x.

While there are [numerous](https://github.com/bskinn/sphobjinv/issues) possible
enhancements to the project, I'm satisfied with its ease of use and usefulness,
at least for my purposes, and thus consider it fully stable. I'm always glad to
receive feature requests and bug reports, though.
