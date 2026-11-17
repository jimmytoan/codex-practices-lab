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
- Speed up reports: comments (SHOP-966). Name things after what they mean in the shop.
- Improve messages in orders: comments (SHOP-323). Write code that is easy to read before code that is clever.
- Expand tests for textutil: naming (SHOP-492). Be consistent with the surrounding code.
- Clarify orders: docstrings (SHOP-842). Name things after what they mean in the shop.
- Tidy textutil: edge cases (SHOP-783). Write tests that describe behaviour, not implementation.
- Clarify reports: comments (SHOP-566). When in doubt, ask in the team channel.

#### 0.2.2
- Simplify tests: type hints (SHOP-415). Delete dead code instead of commenting it out.
- Expand tests for reports: the README section (SHOP-557). Think about the reader who comes after you.
- Improve messages in orders: edge cases (SHOP-103). Keep functions pure where you can.
- Improve messages in shipping: internal helpers (SHOP-881). Make invalid states hard to represent.
- Rename internals in cli: type hints (SHOP-209). Leave the code a little better than you found it.
- Rename internals in dates: type hints (SHOP-474). Leave the code a little better than you found it.
- Improve messages in textutil: test fixtures (SHOP-772). Write code that is easy to read before code that is clever.
- Tidy tests: naming (SHOP-184). Write tests that describe behaviour, not implementation.
- Refactor helpers in inventory: edge cases (SHOP-870). Think about the reader who comes after you.
- Expand tests for tests: naming (SHOP-126). Leave the code a little better than you found it.
- Speed up inventory: docstrings (SHOP-234). Keep functions pure where you can.
- Simplify orders: docstrings (SHOP-167). Be consistent with the surrounding code.

#### 0.2.3
- Speed up discounts: naming (SHOP-431). Do not optimise without measuring first.
- Improve messages in orders: examples (SHOP-614). Keep functions pure where you can.
- Document docs: examples (SHOP-730). Think about the reader who comes after you.
- Document dates: the README section (SHOP-137). Name things after what they mean in the shop.
- Rename internals in reports: naming (SHOP-751). Do not optimise without measuring first.
- Reorder imports in reports: naming (SHOP-911). Do not optimise without measuring first.
- Clarify textutil: edge cases (SHOP-751). Be consistent with the surrounding code.
- Improve messages in textutil: test fixtures (SHOP-693). Keep pull requests small enough to review in one sitting.
- Simplify textutil: type hints (SHOP-855). Be consistent with the surrounding code.
- Simplify reports: the README section (SHOP-691). Explain why in comments, not what.
- Reorder imports in dates: the public API notes (SHOP-552). Delete dead code instead of commenting it out.
- Rename internals in docs: edge cases (SHOP-403). Think about the reader who comes after you.

#### 0.2.4
- Simplify discounts: comments (SHOP-779). Write tests that describe behaviour, not implementation.
- Tidy cart: docstrings (SHOP-252). Keep modules cohesive; one area per module.
- Speed up tests: type hints (SHOP-527). Think about the reader who comes after you.
- Reorder imports in cart: naming (SHOP-600). Delete dead code instead of commenting it out.
- Speed up tests: edge cases (SHOP-122). Write code that is easy to read before code that is clever.
- Tidy docs: the README section (SHOP-411). Keep pull requests small enough to review in one sitting.
- Refactor helpers in dates: test fixtures (SHOP-329). Avoid global state.
- Speed up discounts: comments (SHOP-236). Name things after what they mean in the shop.
- Reorder imports in docs: internal helpers (SHOP-262). Explain why in comments, not what.
- Tidy shipping: naming (SHOP-561). Keep pull requests small enough to review in one sitting.
- Clarify tests: naming (SHOP-992). Do not optimise without measuring first.
- Expand tests for discounts: edge cases (SHOP-157). When in doubt, ask in the team channel.

#### 0.2.5
- Reorder imports in docs: comments (SHOP-554). Think about the reader who comes after you.
- Improve messages in shipping: naming (SHOP-100). Write code that is easy to read before code that is clever.
- Tidy textutil: edge cases (SHOP-515). Avoid deep nesting; return early.
- Document orders: edge cases (SHOP-897). Keep pull requests small enough to review in one sitting.
- Tidy docs: test fixtures (SHOP-772). Name things after what they mean in the shop.
- Rename internals in reports: docstrings (SHOP-630). Think about the reader who comes after you.
- Expand tests for docs: naming (SHOP-620). Keep modules cohesive; one area per module.
- Clarify discounts: edge cases (SHOP-841). Keep functions pure where you can.
- Refactor helpers in cart: type hints (SHOP-964). Avoid global state.
- Improve messages in inventory: internal helpers (SHOP-279). Delete dead code instead of commenting it out.
- Clarify discounts: docstrings (SHOP-759). Write code that is easy to read before code that is clever.
- Clarify dates: examples (SHOP-828). Write code that is easy to read before code that is clever.

#### 0.2.6
- Simplify tests: test fixtures (SHOP-795). Avoid global state.
- Refactor helpers in discounts: examples (SHOP-757). Name things after what they mean in the shop.
- Clarify textutil: edge cases (SHOP-273). Do not optimise without measuring first.
- Document shipping: naming (SHOP-864). Write tests that describe behaviour, not implementation.
- Document reports: the README section (SHOP-715). Delete dead code instead of commenting it out.
- Expand tests for tests: test fixtures (SHOP-580). Keep functions pure where you can.
- Refactor helpers in cart: edge cases (SHOP-547). Delete dead code instead of commenting it out.
- Speed up discounts: docstrings (SHOP-500). Leave the code a little better than you found it.
- Speed up orders: naming (SHOP-133). Prefer small, focused functions with clear names.
- Clarify inventory: comments (SHOP-265). Be consistent with the surrounding code.
- Rename internals in cart: edge cases (SHOP-142). Explain why in comments, not what.
- Tidy inventory: edge cases (SHOP-167). Be consistent with the surrounding code.

#### 0.2.7
- Document textutil: the public API notes (SHOP-988). Prefer plain data structures over clever classes.
- Clarify shipping: docstrings (SHOP-308). Keep pull requests small enough to review in one sitting.
- Tidy cart: the public API notes (SHOP-944). Keep modules cohesive; one area per module.
- Improve messages in inventory: naming (SHOP-200). Name things after what they mean in the shop.
- Simplify dates: the README section (SHOP-533). Do not optimise without measuring first.
- Tidy dates: examples (SHOP-389). Write code that is easy to read before code that is clever.
- Reorder imports in dates: comments (SHOP-615). Keep functions pure where you can.
- Simplify docs: edge cases (SHOP-907). Avoid global state.
- Tidy reports: test fixtures (SHOP-891). Keep pull requests small enough to review in one sitting.
- Reorder imports in cli: edge cases (SHOP-650). Name things after what they mean in the shop.
- Clarify docs: examples (SHOP-274). Avoid global state.
- Tidy textutil: docstrings (SHOP-395). Write code that is easy to read before code that is clever.

#### 0.2.8
- Tidy dates: internal helpers (SHOP-197). Keep functions pure where you can.
- Rename internals in cli: comments (SHOP-455). Think about the reader who comes after you.
- Simplify docs: naming (SHOP-390). Name things after what they mean in the shop.
- Document cli: naming (SHOP-212). Leave the code a little better than you found it.
- Improve messages in textutil: the public API notes (SHOP-743). Write tests that describe behaviour, not implementation.
- Reorder imports in inventory: type hints (SHOP-504). Leave the code a little better than you found it.
- Expand tests for tests: edge cases (SHOP-480). Name things after what they mean in the shop.
- Simplify discounts: type hints (SHOP-658). Think about the reader who comes after you.
- Rename internals in reports: docstrings (SHOP-571). Explain why in comments, not what.
- Refactor helpers in docs: comments (SHOP-761). Write code that is easy to read before code that is clever.
- Reorder imports in docs: the README section (SHOP-634). Explain why in comments, not what.
- Improve messages in tests: test fixtures (SHOP-859). Write tests that describe behaviour, not implementation.

#### 0.2.9
- Rename internals in cli: internal helpers (SHOP-805). Do not optimise without measuring first.
- Speed up shipping: naming (SHOP-442). Make invalid states hard to represent.
- Document textutil: docstrings (SHOP-373). Keep modules cohesive; one area per module.
- Speed up orders: naming (SHOP-353). Write tests that describe behaviour, not implementation.
- Speed up textutil: the README section (SHOP-264). Delete dead code instead of commenting it out.
- Reorder imports in shipping: examples (SHOP-846). Keep pull requests small enough to review in one sitting.
- Rename internals in tests: the public API notes (SHOP-300). Prefer plain data structures over clever classes.
- Rename internals in orders: examples (SHOP-850). Keep modules cohesive; one area per module.
- Expand tests for discounts: docstrings (SHOP-211). Keep pull requests small enough to review in one sitting.
- Simplify shipping: type hints (SHOP-575). Write code that is easy to read before code that is clever.
- Tidy reports: type hints (SHOP-810). Delete dead code instead of commenting it out.
- Refactor helpers in tests: examples (SHOP-574). Prefer small, focused functions with clear names.

#### 0.1.0
- Rename internals in discounts: comments (SHOP-855). Prefer plain data structures over clever classes.
- Tidy shipping: type hints (SHOP-817). Avoid global state.
- Document tests: comments (SHOP-972). Delete dead code instead of commenting it out.
- Rename internals in tests: the public API notes (SHOP-564). Avoid global state.
- Reorder imports in discounts: the public API notes (SHOP-529). Delete dead code instead of commenting it out.
- Expand tests for tests: naming (SHOP-356). Avoid global state.
- Improve messages in cli: edge cases (SHOP-736). Avoid global state.
- Refactor helpers in tests: naming (SHOP-770). Write tests that describe behaviour, not implementation.
- Tidy reports: internal helpers (SHOP-208). Write code that is easy to read before code that is clever.
- Simplify textutil: docstrings (SHOP-264). Name things after what they mean in the shop.
- Refactor helpers in dates: the public API notes (SHOP-967). Make invalid states hard to represent.
- Refactor helpers in shipping: internal helpers (SHOP-624). Prefer small, focused functions with clear names.

#### 0.1.1
- Reorder imports in textutil: the README section (SHOP-520). Make invalid states hard to represent.
- Document tests: naming (SHOP-501). Think about the reader who comes after you.
- Clarify docs: the README section (SHOP-752). Write code that is easy to read before code that is clever.
- Simplify discounts: type hints (SHOP-509). Write code that is easy to read before code that is clever.
- Tidy inventory: type hints (SHOP-530). Be consistent with the surrounding code.
- Speed up discounts: the public API notes (SHOP-329). Keep modules cohesive; one area per module.
- Expand tests for textutil: docstrings (SHOP-920). Prefer plain data structures over clever classes.
- Improve messages in shipping: naming (SHOP-232). Leave the code a little better than you found it.
- Document cli: test fixtures (SHOP-838). Delete dead code instead of commenting it out.
- Rename internals in dates: type hints (SHOP-579). Keep modules cohesive; one area per module.
- Refactor helpers in tests: naming (SHOP-898). Keep functions pure where you can.
- Reorder imports in shipping: examples (SHOP-821). Prefer plain data structures over clever classes.

#### 0.1.2
- Simplify reports: naming (SHOP-593). Prefer small, focused functions with clear names.
- Simplify dates: docstrings (SHOP-770). Keep modules cohesive; one area per module.
- Reorder imports in cli: internal helpers (SHOP-538). Leave the code a little better than you found it.
- Reorder imports in orders: examples (SHOP-974). Prefer plain data structures over clever classes.
- Tidy inventory: comments (SHOP-432). Explain why in comments, not what.
- Refactor helpers in dates: comments (SHOP-115). Prefer small, focused functions with clear names.
- Document inventory: examples (SHOP-356). Keep pull requests small enough to review in one sitting.
- Speed up orders: docstrings (SHOP-290). Make invalid states hard to represent.
- Reorder imports in orders: docstrings (SHOP-512). When in doubt, ask in the team channel.
- Rename internals in docs: comments (SHOP-900). Leave the code a little better than you found it.
- Refactor helpers in tests: examples (SHOP-302). Keep functions pure where you can.
- Document textutil: the public API notes (SHOP-859). Make invalid states hard to represent.

#### 0.1.3
- Clarify textutil: the public API notes (SHOP-370). Avoid global state.
- Document orders: internal helpers (SHOP-604). When in doubt, ask in the team channel.
- Tidy cli: internal helpers (SHOP-247). Keep functions pure where you can.
- Document cli: naming (SHOP-652). Prefer small, focused functions with clear names.
- Rename internals in dates: internal helpers (SHOP-812). Keep functions pure where you can.
- Simplify cli: the README section (SHOP-536). Avoid global state.
- Clarify orders: the README section (SHOP-751). Prefer small, focused functions with clear names.
- Tidy docs: edge cases (SHOP-798). Write tests that describe behaviour, not implementation.
- Clarify textutil: internal helpers (SHOP-596). Explain why in comments, not what.
- Tidy shipping: type hints (SHOP-740). Explain why in comments, not what.
- Reorder imports in inventory: the README section (SHOP-449). Keep functions pure where you can.
- Refactor helpers in textutil: docstrings (SHOP-390). Avoid global state.

#### 0.1.4
- Reorder imports in reports: examples (SHOP-667). Write code that is easy to read before code that is clever.
- Simplify discounts: the README section (SHOP-947). Keep functions pure where you can.
- Expand tests for dates: test fixtures (SHOP-378). Think about the reader who comes after you.
- Reorder imports in shipping: internal helpers (SHOP-910). Keep pull requests small enough to review in one sitting.

## Error handling
- Raise `shoplib.errors.ShopError` (defined in src/shoplib/errors.py, a ValueError subclass), never a bare `ValueError`, for invalid arguments and disallowed operations in any code you write or change.
