* I have a fixed number of bins and items
* Items are identical (all the same value)
* Bins can have constraints : max, min or none.
* I want to pack the items in the bins, but what I want to minimize is the item count in each bin.

# Example

```python
BinConstraint = Tuple[Literal["min", "max"], int] | Literal["none"]

# Let's say we have 60 items and we want to pack them in 4 bins
total_items = 60

# Let's define the 4 bins with different constraints
bin_constraints: list[BinConstraint] = [
    "none",
    ("min", 30),
    ("max", 0),
    "none",
]

result = solve_bin_packing(total_items, bin_constraints)
```

I expect the result to be : `[15, 30, 0, 15]`, as it uses the constraints and minimizes the item count in each bin.
