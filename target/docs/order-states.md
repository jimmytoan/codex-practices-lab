# Order states

    NEW -> PAID -> SHIPPED -> DELIVERED
     |      |
     +------+--> CANCELLED

- Creating an order reserves its stock in the inventory.
- `pay()`: NEW -> PAID.
- `ship()`: PAID -> SHIPPED. Ships the reserved stock out of the inventory.
- `deliver()`: SHIPPED -> DELIVERED.
- `cancel()`: allowed from NEW and PAID only.
  - The order's reserved stock is released back to available.
  - Cancelling a PAID order sets `refund_due` to `True`. Cancelling a NEW order
    leaves it `False`.
  - Cancelling an order that is already CANCELLED does nothing (no error, stock
    is not released twice).
  - Cancelling a SHIPPED or DELIVERED order raises `ValueError` and changes
    nothing.
