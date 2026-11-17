# Search queries

`search(products, query)` returns the products that match every term of `query`, in their input order.

## Tokens
The query is split on whitespace, except inside double quotes. Quotes can wrap a whole term
(`"blue mug"`) or a field value (`name:"blue mug"`); the quote characters are not part of the value.
An unclosed quote is an error.

## Terms
- A bare word matches when it appears in the product name, case-insensitively, as a substring.
  A quoted phrase works the same way with the whole phrase.
- `sku:V` matches when the SKU equals V, case-insensitively.
- `tag:V` matches when any of the product's tags equals V, case-insensitively.
- `name:V` matches when the name contains V, case-insensitively.
- For `sku` and `tag`, a value that ends in `*` is a prefix match instead (`sku:MUG-*`). A `*` anywhere
  else is an ordinary character.
- `price` directly followed by one of `<`, `<=`, `>`, `>=`, `=` and a whole number of cents compares the
  price: `price>=1000`.
- A `-` in front of a term negates it: `-tag:sale`.
- An empty or all-whitespace query matches every product.

## Errors
Raise `ValueError` for: a field name other than `sku`, `name` and `tag` before a `:` (so `price:5` is an
error); a price comparison whose value is not a whole number; an empty field value (`tag:`); a `-` with
nothing after it; an unclosed quote.
