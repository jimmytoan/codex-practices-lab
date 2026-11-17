# AGENTS.md

## Layout
- `src/shoplib/`: library code, one module per area (cart, inventory, orders, shipping, discounts, dates, textutil, reports, cli).
- `tests/`: pytest tests, one file per module.
- `docs/`: specs. `docs/CONVENTIONS.md` has the money, error and output rules; read it before changing money or output code.

## Commands
- Test: `python -m pytest -q`
- No build or lint step. Standard library only; do not add dependencies.

## Rules
- Money is integer cents. Percentages go through `shoplib.money.percent_of` (rounds half up). Never use `round()` or float for money.
- Raise `shoplib.errors.ShopError` (defined in src/shoplib/errors.py, a ValueError subclass), never a bare `ValueError`, for invalid arguments and disallowed operations in any code you write or change.
- Do not modify `src/shoplib/legacy_pricing.py`; an external importer depends on it.
- Keep changes to the files the task needs.

## Done means
- The behaviour asked for, and the spec it refers to, holds, with tests for it in `tests/`.
- `python -m pytest -q` passes.

## Team notes

These notes collect things the team has agreed over time. Most are general.

### Working style
- Prefer small, focused functions with clear names.
- Write code that is easy to read before code that is clever.
- Leave the code a little better than you found it.
- Keep pull requests small enough to review in one sitting.
- Explain why in comments, not what.
- Avoid deep nesting; return early.
- Name things after what they mean in the shop.
- Delete dead code instead of commenting it out.
- Do not optimise without measuring first.
- Keep modules cohesive; one area per module.
- Write tests that describe behaviour, not implementation.
- Be consistent with the surrounding code.
- Prefer plain data structures over clever classes.
- Avoid global state.
- Make invalid states hard to represent.
- Keep functions pure where you can.
- Think about the reader who comes after you.
- When in doubt, ask in the team channel.

### Glossary
- **SKU**: stock keeping unit; the identifier of a product variant.
- **Line**: one SKU in a cart with a quantity.
- **Subtotal**: sum of line totals before coupons.
- **Coupon**: a code that lowers the price of an order.
- **Reservation**: stock held for an order that has not shipped.
- **On hand**: units physically in the warehouse.
- **Available**: on hand minus reserved.
- **Parcel**: one box sent to a customer.
- **Tier**: a weight band with one shipping price.
- **Order**: a confirmed purchase with a life cycle.
- **Refund**: money returned to a customer.
- **Slug**: the URL-safe form of a product name.
- **Report**: an export of sales data.
- **Business day**: a weekday that is not a holiday.
- **Importer**: the nightly job that loads supplier prices.
- **Fulfilment**: picking, packing and shipping.

### Changelog

#### 0.4.0
- Reorder imports in orders: type hints (SHOP-766). Write code that is easy to read before code that is clever.
- Clarify textutil: the public API notes (SHOP-474). Write code that is easy to read before code that is clever.
- Refactor helpers in shipping: edge cases (SHOP-188). Avoid global state.
- Expand tests for inventory: docstrings (SHOP-192). When in doubt, ask in the team channel.
- Expand tests for cart: comments (SHOP-226). Delete dead code instead of commenting it out.
- Speed up cart: comments (SHOP-699). Prefer plain data structures over clever classes.
- Tidy shipping: edge cases (SHOP-670). Explain why in comments, not what.
- Simplify reports: naming (SHOP-653). Keep pull requests small enough to review in one sitting.
- Speed up discounts: test fixtures (SHOP-935). Avoid deep nesting; return early.
- Clarify docs: comments (SHOP-754). Name things after what they mean in the shop.
- Reorder imports in inventory: test fixtures (SHOP-829). Leave the code a little better than you found it.
- Speed up cart: comments (SHOP-310). Keep functions pure where you can.

#### 0.4.1
- Refactor helpers in reports: the README section (SHOP-576). Make invalid states hard to represent.
- Reorder imports in discounts: docstrings (SHOP-913). Avoid deep nesting; return early.
- Document inventory: comments (SHOP-407). Think about the reader who comes after you.
- Improve messages in dates: internal helpers (SHOP-394). Leave the code a little better than you found it.
- Clarify textutil: type hints (SHOP-268). Write tests that describe behaviour, not implementation.
- Rename internals in cli: type hints (SHOP-140). Leave the code a little better than you found it.
- Refactor helpers in docs: the README section (SHOP-448). Be consistent with the surrounding code.
- Speed up cli: comments (SHOP-916). Make invalid states hard to represent.
- Clarify inventory: examples (SHOP-585). Leave the code a little better than you found it.
- Tidy discounts: comments (SHOP-797). Make invalid states hard to represent.
- Simplify reports: the README section (SHOP-123). Make invalid states hard to represent.
- Reorder imports in orders: comments (SHOP-219). Keep functions pure where you can.

#### 0.4.2
- Tidy shipping: examples (SHOP-232). Delete dead code instead of commenting it out.
- Expand tests for reports: internal helpers (SHOP-182). Avoid deep nesting; return early.
- Improve messages in reports: test fixtures (SHOP-384). Explain why in comments, not what.
- Expand tests for textutil: examples (SHOP-823). Avoid global state.
- Reorder imports in tests: type hints (SHOP-336). Explain why in comments, not what.
- Clarify orders: naming (SHOP-337). Delete dead code instead of commenting it out.
- Tidy cli: comments (SHOP-286). Do not optimise without measuring first.
- Simplify cart: naming (SHOP-529). When in doubt, ask in the team channel.
- Reorder imports in docs: comments (SHOP-426). Explain why in comments, not what.
- Refactor helpers in docs: edge cases (SHOP-567). When in doubt, ask in the team channel.
- Expand tests for reports: type hints (SHOP-503). Keep pull requests small enough to review in one sitting.
- Improve messages in tests: type hints (SHOP-163). Name things after what they mean in the shop.

#### 0.4.3
- Clarify shipping: internal helpers (SHOP-266). Keep pull requests small enough to review in one sitting.
- Reorder imports in docs: edge cases (SHOP-204). Prefer small, focused functions with clear names.
- Speed up orders: test fixtures (SHOP-203). Be consistent with the surrounding code.
- Speed up cart: the public API notes (SHOP-995). Name things after what they mean in the shop.
- Speed up reports: naming (SHOP-749). Do not optimise without measuring first.
- Reorder imports in docs: the README section (SHOP-585). Keep pull requests small enough to review in one sitting.
- Clarify cli: internal helpers (SHOP-591). Keep functions pure where you can.
- Simplify inventory: naming (SHOP-204). Write tests that describe behaviour, not implementation.
- Simplify cli: naming (SHOP-628). Prefer small, focused functions with clear names.
- Document textutil: the README section (SHOP-250). When in doubt, ask in the team channel.
- Tidy textutil: examples (SHOP-758). Leave the code a little better than you found it.
- Simplify textutil: the README section (SHOP-271). Be consistent with the surrounding code.

#### 0.4.4
- Document textutil: test fixtures (SHOP-897). Think about the reader who comes after you.
- Reorder imports in tests: docstrings (SHOP-727). Name things after what they mean in the shop.
- Document reports: docstrings (SHOP-304). Think about the reader who comes after you.
- Improve messages in dates: edge cases (SHOP-128). Do not optimise without measuring first.
- Improve messages in discounts: docstrings (SHOP-809). Be consistent with the surrounding code.
- Improve messages in dates: the README section (SHOP-182). Delete dead code instead of commenting it out.
- Clarify shipping: internal helpers (SHOP-301). Write tests that describe behaviour, not implementation.
- Document cli: comments (SHOP-724). Prefer small, focused functions with clear names.
- Improve messages in tests: the README section (SHOP-918). Leave the code a little better than you found it.
- Clarify reports: docstrings (SHOP-589). Avoid deep nesting; return early.
- Expand tests for tests: the README section (SHOP-188). Prefer plain data structures over clever classes.
- Improve messages in reports: the public API notes (SHOP-842). Avoid deep nesting; return early.

#### 0.4.5
- Rename internals in orders: edge cases (SHOP-254). Make invalid states hard to represent.
- Rename internals in docs: comments (SHOP-585). Be consistent with the surrounding code.
- Rename internals in textutil: test fixtures (SHOP-234). Prefer small, focused functions with clear names.
- Tidy tests: the public API notes (SHOP-639). Explain why in comments, not what.
- Expand tests for shipping: docstrings (SHOP-128). Do not optimise without measuring first.
- Document discounts: test fixtures (SHOP-346). Write tests that describe behaviour, not implementation.
- Simplify textutil: type hints (SHOP-954). Explain why in comments, not what.
- Tidy dates: internal helpers (SHOP-778). Think about the reader who comes after you.
- Expand tests for textutil: naming (SHOP-644). Explain why in comments, not what.
- Refactor helpers in textutil: edge cases (SHOP-993). Make invalid states hard to represent.
- Rename internals in docs: edge cases (SHOP-894). Explain why in comments, not what.
- Rename internals in orders: internal helpers (SHOP-733). Keep pull requests small enough to review in one sitting.

#### 0.4.6
- Refactor helpers in cart: the README section (SHOP-798). Think about the reader who comes after you.
- Refactor helpers in textutil: internal helpers (SHOP-903). Keep pull requests small enough to review in one sitting.
- Refactor helpers in cart: docstrings (SHOP-295). Do not optimise without measuring first.
- Tidy inventory: test fixtures (SHOP-563). When in doubt, ask in the team channel.
- Tidy inventory: internal helpers (SHOP-433). Think about the reader who comes after you.
- Speed up textutil: docstrings (SHOP-809). Do not optimise without measuring first.
- Improve messages in textutil: test fixtures (SHOP-926). Keep functions pure where you can.
- Refactor helpers in shipping: test fixtures (SHOP-997). Do not optimise without measuring first.
- Refactor helpers in shipping: internal helpers (SHOP-240). Avoid global state.
- Clarify reports: internal helpers (SHOP-423). Leave the code a little better than you found it.
- Document reports: the public API notes (SHOP-317). Keep modules cohesive; one area per module.
- Clarify orders: the README section (SHOP-246). Do not optimise without measuring first.

#### 0.4.7
- Rename internals in cli: docstrings (SHOP-864). Keep pull requests small enough to review in one sitting.
- Expand tests for cli: naming (SHOP-783). Delete dead code instead of commenting it out.
- Rename internals in reports: test fixtures (SHOP-513). Write tests that describe behaviour, not implementation.
- Expand tests for shipping: the README section (SHOP-426). Leave the code a little better than you found it.
- Reorder imports in cart: the README section (SHOP-667). Make invalid states hard to represent.
- Improve messages in cart: type hints (SHOP-439). Think about the reader who comes after you.
- Speed up discounts: test fixtures (SHOP-165). Keep pull requests small enough to review in one sitting.
- Document inventory: the public API notes (SHOP-371). Do not optimise without measuring first.
- Tidy orders: examples (SHOP-873). Explain why in comments, not what.
- Expand tests for tests: examples (SHOP-515). Explain why in comments, not what.
- Refactor helpers in textutil: comments (SHOP-606). Write tests that describe behaviour, not implementation.
- Clarify discounts: edge cases (SHOP-918). Avoid deep nesting; return early.

#### 0.4.8
- Expand tests for inventory: examples (SHOP-117). Leave the code a little better than you found it.
- Simplify inventory: comments (SHOP-976). Delete dead code instead of commenting it out.
- Clarify discounts: the public API notes (SHOP-564). Prefer small, focused functions with clear names.
- Reorder imports in textutil: type hints (SHOP-374). Explain why in comments, not what.
- Tidy textutil: docstrings (SHOP-212). Avoid deep nesting; return early.
- Simplify cart: naming (SHOP-306). Keep modules cohesive; one area per module.
- Simplify textutil: docstrings (SHOP-396). Make invalid states hard to represent.
- Refactor helpers in tests: naming (SHOP-377). Be consistent with the surrounding code.
- Tidy discounts: edge cases (SHOP-115). Prefer small, focused functions with clear names.
- Refactor helpers in textutil: docstrings (SHOP-626). Keep functions pure where you can.
- Document cli: the public API notes (SHOP-774). Avoid global state.
- Improve messages in textutil: type hints (SHOP-618). Keep modules cohesive; one area per module.

#### 0.4.9
- Document shipping: the README section (SHOP-303). Explain why in comments, not what.
- Expand tests for dates: edge cases (SHOP-957). Explain why in comments, not what.
- Tidy inventory: examples (SHOP-541). Avoid deep nesting; return early.
- Tidy inventory: type hints (SHOP-991). Think about the reader who comes after you.
- Simplify docs: docstrings (SHOP-809). Keep modules cohesive; one area per module.
- Tidy cli: naming (SHOP-261). Do not optimise without measuring first.
- Improve messages in cart: examples (SHOP-472). Write tests that describe behaviour, not implementation.
- Refactor helpers in dates: docstrings (SHOP-135). Keep modules cohesive; one area per module.
- Document dates: naming (SHOP-101). Write tests that describe behaviour, not implementation.
- Expand tests for inventory: internal helpers (SHOP-385). Think about the reader who comes after you.
- Document shipping: test fixtures (SHOP-894). Prefer small, focused functions with clear names.
- Clarify discounts: the public API notes (SHOP-247). Prefer plain data structures over clever classes.

#### 0.3.0
- Speed up cart: type hints (SHOP-123). Keep modules cohesive; one area per module.
- Simplify tests: docstrings (SHOP-186). Think about the reader who comes after you.
- Rename internals in tests: comments (SHOP-498). Write tests that describe behaviour, not implementation.
- Improve messages in orders: examples (SHOP-841). Explain why in comments, not what.
- Tidy textutil: type hints (SHOP-851). Think about the reader who comes after you.
- Rename internals in textutil: test fixtures (SHOP-682). Prefer small, focused functions with clear names.
- Speed up tests: docstrings (SHOP-187). Prefer small, focused functions with clear names.
- Tidy orders: the README section (SHOP-207). Prefer plain data structures over clever classes.
- Improve messages in textutil: edge cases (SHOP-742). Prefer small, focused functions with clear names.
- Refactor helpers in tests: docstrings (SHOP-601). Do not optimise without measuring first.
- Tidy cli: the public API notes (SHOP-866). Think about the reader who comes after you.
- Refactor helpers in inventory: test fixtures (SHOP-167). Keep functions pure where you can.

#### 0.3.1
- Simplify inventory: examples (SHOP-340). Name things after what they mean in the shop.
- Document tests: internal helpers (SHOP-605). Prefer plain data structures over clever classes.
- Clarify cli: examples (SHOP-885). Write code that is easy to read before code that is clever.
- Speed up tests: docstrings (SHOP-179). Explain why in comments, not what.
- Reorder imports in discounts: examples (SHOP-736). Explain why in comments, not what.
- Tidy cli: edge cases (SHOP-597). Do not optimise without measuring first.
- Clarify shipping: internal helpers (SHOP-397). Think about the reader who comes after you.
- Simplify cli: internal helpers (SHOP-577). Keep pull requests small enough to review in one sitting.
- Refactor helpers in shipping: examples (SHOP-187). Keep functions pure where you can.
- Tidy discounts: internal helpers (SHOP-178). Think about the reader who comes after you.
- Improve messages in discounts: type hints (SHOP-314). Name things after what they mean in the shop.
- Clarify docs: the public API notes (SHOP-245). Think about the reader who comes after you.

#### 0.3.2
- Simplify dates: naming (SHOP-717). Think about the reader who comes after you.
- Simplify inventory: the README section (SHOP-336). Keep functions pure where you can.
- Improve messages in reports: edge cases (SHOP-262). Prefer small, focused functions with clear names.
- Improve messages in tests: internal helpers (SHOP-515). Keep modules cohesive; one area per module.
- Rename internals in reports: the README section (SHOP-485). Write tests that describe behaviour, not implementation.
- Clarify dates: edge cases (SHOP-432). Write tests that describe behaviour, not implementation.
- Expand tests for inventory: docstrings (SHOP-830). Prefer small, focused functions with clear names.
- Simplify discounts: the README section (SHOP-166). Prefer plain data structures over clever classes.
- Expand tests for docs: the public API notes (SHOP-469). Avoid global state.
- Simplify cart: examples (SHOP-204). Write code that is easy to read before code that is clever.
- Simplify tests: naming (SHOP-355). Do not optimise without measuring first.
- Expand tests for textutil: the README section (SHOP-294). Be consistent with the surrounding code.

#### 0.3.3
- Expand tests for cart: type hints (SHOP-996). When in doubt, ask in the team channel.
- Refactor helpers in shipping: the public API notes (SHOP-150). Avoid global state.
- Improve messages in docs: naming (SHOP-759). Keep modules cohesive; one area per module.
- Improve messages in cart: test fixtures (SHOP-230). Avoid deep nesting; return early.
- Improve messages in reports: the README section (SHOP-388). Keep modules cohesive; one area per module.
- Simplify tests: examples (SHOP-515). Delete dead code instead of commenting it out.
- Simplify cli: test fixtures (SHOP-784). Prefer plain data structures over clever classes.
- Clarify orders: naming (SHOP-176). Name things after what they mean in the shop.
- Refactor helpers in cli: test fixtures (SHOP-325). Make invalid states hard to represent.
- Reorder imports in cli: type hints (SHOP-242). When in doubt, ask in the team channel.
- Document shipping: the public API notes (SHOP-278). Write tests that describe behaviour, not implementation.
- Refactor helpers in inventory: the README section (SHOP-344). Be consistent with the surrounding code.

#### 0.3.4
- Simplify docs: docstrings (SHOP-120). Avoid global state.
- Expand tests for reports: test fixtures (SHOP-315). Prefer plain data structures over clever classes.
- Simplify dates: edge cases (SHOP-610). Do not optimise without measuring first.
- Speed up dates: naming (SHOP-803). Think about the reader who comes after you.
- Refactor helpers in tests: docstrings (SHOP-194). Do not optimise without measuring first.
- Document reports: type hints (SHOP-761). Make invalid states hard to represent.
- Expand tests for discounts: edge cases (SHOP-230). Write code that is easy to read before code that is clever.
- Expand tests for cli: comments (SHOP-601). Prefer small, focused functions with clear names.
- Clarify reports: test fixtures (SHOP-975). Make invalid states hard to represent.
- Improve messages in shipping: the public API notes (SHOP-329). Explain why in comments, not what.
- Rename internals in textutil: the public API notes (SHOP-945). Make invalid states hard to represent.
- Clarify textutil: edge cases (SHOP-101). Explain why in comments, not what.

#### 0.3.5
- Document docs: edge cases (SHOP-760). Keep modules cohesive; one area per module.
- Rename internals in tests: examples (SHOP-640). Avoid global state.
- Clarify inventory: the public API notes (SHOP-407). Think about the reader who comes after you.
- Speed up shipping: type hints (SHOP-367). Delete dead code instead of commenting it out.
- Speed up cart: edge cases (SHOP-650). Keep modules cohesive; one area per module.
- Improve messages in discounts: the README section (SHOP-760). Delete dead code instead of commenting it out.
- Improve messages in textutil: docstrings (SHOP-660). Delete dead code instead of commenting it out.
- Tidy reports: examples (SHOP-156). Prefer small, focused functions with clear names.
- Document cli: type hints (SHOP-183). Do not optimise without measuring first.
- Document tests: type hints (SHOP-479). Delete dead code instead of commenting it out.
- Improve messages in cart: the README section (SHOP-835). Avoid global state.
- Reorder imports in tests: type hints (SHOP-302). Prefer small, focused functions with clear names.

#### 0.3.6
- Simplify textutil: the public API notes (SHOP-310). Keep functions pure where you can.
- Document discounts: docstrings (SHOP-336). Make invalid states hard to represent.
- Document discounts: examples (SHOP-211). Keep functions pure where you can.
- Speed up orders: docstrings (SHOP-596). Avoid global state.
- Tidy docs: naming (SHOP-502). Write code that is easy to read before code that is clever.
- Document cart: comments (SHOP-245). Avoid global state.
- Tidy cart: naming (SHOP-502). Make invalid states hard to represent.
- Reorder imports in inventory: the public API notes (SHOP-269). Write tests that describe behaviour, not implementation.
- Document orders: test fixtures (SHOP-864). Make invalid states hard to represent.
- Tidy discounts: type hints (SHOP-959). Be consistent with the surrounding code.
- Reorder imports in cli: naming (SHOP-211). Prefer small, focused functions with clear names.
- Clarify discounts: the public API notes (SHOP-459). Avoid global state.

#### 0.3.7
- Clarify textutil: docstrings (SHOP-489). Be consistent with the surrounding code.
- Simplify reports: the public API notes (SHOP-150). Keep functions pure where you can.
- Document dates: test fixtures (SHOP-557). Name things after what they mean in the shop.
- Reorder imports in dates: internal helpers (SHOP-131). Avoid global state.
- Document tests: type hints (SHOP-141). Prefer plain data structures over clever classes.
- Tidy cli: the public API notes (SHOP-922). Write code that is easy to read before code that is clever.
- Simplify shipping: the public API notes (SHOP-720). Write tests that describe behaviour, not implementation.
- Reorder imports in discounts: the README section (SHOP-731). Write code that is easy to read before code that is clever.
- Simplify dates: examples (SHOP-404). Prefer small, focused functions with clear names.
- Speed up tests: the public API notes (SHOP-124). Delete dead code instead of commenting it out.
- Clarify cli: internal helpers (SHOP-894). Prefer plain data structures over clever classes.
- Simplify reports: internal helpers (SHOP-235). Keep functions pure where you can.

#### 0.3.8
- Rename internals in cart: examples (SHOP-942). Explain why in comments, not what.
- Speed up shipping: the README section (SHOP-981). Write tests that describe behaviour, not implementation.
- Improve messages in dates: comments (SHOP-180). Think about the reader who comes after you.
- Document reports: naming (SHOP-353). Avoid global state.
- Clarify tests: edge cases (SHOP-593). When in doubt, ask in the team channel.
- Refactor helpers in dates: naming (SHOP-536). Keep pull requests small enough to review in one sitting.
- Clarify discounts: comments (SHOP-186). Name things after what they mean in the shop.
- Clarify reports: internal helpers (SHOP-826). Make invalid states hard to represent.
- Rename internals in shipping: naming (SHOP-526). Make invalid states hard to represent.
- Speed up tests: docstrings (SHOP-865). When in doubt, ask in the team channel.
- Clarify discounts: examples (SHOP-386). Do not optimise without measuring first.
- Reorder imports in discounts: examples (SHOP-303). Make invalid states hard to represent.

#### 0.3.9
- Document orders: docstrings (SHOP-341). Explain why in comments, not what.
- Simplify docs: docstrings (SHOP-434). Leave the code a little better than you found it.
- Expand tests for discounts: docstrings (SHOP-619). Think about the reader who comes after you.
- Document tests: the public API notes (SHOP-769). Make invalid states hard to represent.
- Tidy inventory: edge cases (SHOP-586). Delete dead code instead of commenting it out.
- Improve messages in dates: edge cases (SHOP-997). Keep modules cohesive; one area per module.
- Document inventory: edge cases (SHOP-294). Name things after what they mean in the shop.
- Clarify dates: test fixtures (SHOP-986). Avoid deep nesting; return early.
- Improve messages in docs: examples (SHOP-893). Prefer small, focused functions with clear names.
- Clarify tests: comments (SHOP-826). Be consistent with the surrounding code.
- Document cart: the README section (SHOP-448). Explain why in comments, not what.
- Tidy shipping: examples (SHOP-139). Name things after what they mean in the shop.

#### 0.2.0
- Tidy dates: type hints (SHOP-794). Be consistent with the surrounding code.
- Rename internals in docs: examples (SHOP-179). Name things after what they mean in the shop.
- Tidy cli: test fixtures (SHOP-595). Leave the code a little better than you found it.
- Expand tests for inventory: type hints (SHOP-779). When in doubt, ask in the team channel.
- Rename internals in tests: test fixtures (SHOP-193). Avoid deep nesting; return early.
- Expand tests for discounts: type hints (SHOP-390). Keep modules cohesive; one area per module.
- Expand tests for cart: examples (SHOP-863). Be consistent with the surrounding code.
- Expand tests for reports: edge cases (SHOP-984). Be consistent with the surrounding code.
- Document reports: type hints (SHOP-308). Prefer small, focused functions with clear names.
- Expand tests for orders: type hints (SHOP-216). Leave the code a little better than you found it.
- Expand tests for docs: the README section (SHOP-571). Avoid deep nesting; return early.
- Rename internals in cart: edge cases (SHOP-664). Explain why in comments, not what.

#### 0.2.1
- Expand tests for inventory: comments (SHOP-737). Be consistent with the surrounding code.
- Refactor helpers in orders: naming (SHOP-456). Keep modules cohesive; one area per module.
- Rename internals in textutil: naming (SHOP-168). Keep pull requests small enough to review in one sitting.
- Expand tests for cli: docstrings (SHOP-408). Explain why in comments, not what.
- Tidy cli: the README section (SHOP-154). Prefer plain data structures over clever classes.
- Clarify docs: naming (SHOP-755). Delete dead code instead of commenting it out.
