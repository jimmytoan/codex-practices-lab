# Shipping

## Cost of one parcel
`shipping_cost(weight_g)` uses weight tiers with inclusive upper bounds:

| Up to and including | Cost |
|---|---|
| 1,000 g | 500 |
| 2,000 g | 800 |
| 5,000 g | 1,200 |
| 20,000 g | 2,500 |

A weight of 0 or less, or more than 20,000 g, raises `ValueError`.

## Splitting an order into parcels
`split_parcels(items, max_weight_g)` takes `items` as a list of
`(sku, unit_weight_g, qty)` and returns a list of parcels; each parcel is the
list of SKUs packed into it (one entry per unit), in the order they were packed.

The algorithm is first-fit decreasing:

1. Expand the items into single units.
2. Sort the units by weight, heaviest first. Units of equal weight are ordered
   by SKU, ascending.
3. Take the units in that order. Put each unit into the first parcel (in the
   order the parcels were opened) that still has room for it. If none has room,
   open a new parcel.

A parcel's total weight may equal `max_weight_g` but not exceed it. A unit
heavier than `max_weight_g`, a quantity below 1, or a weight below 1 raises
`ValueError`. An empty item list gives an empty list.

`shipment_cost(items, max_weight_g)` is the sum of `shipping_cost` over the
parcels from `split_parcels`.
