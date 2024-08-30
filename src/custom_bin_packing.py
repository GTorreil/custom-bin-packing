"""
Problem and solution for custom bin packing.
"""

from typing import Literal, Tuple, Union

BinConstraint = Tuple[Literal["min", "max"], int] | Literal["none"]


class CustomBinPackingSolverNaiveAndSlow:
    """
    Custom bin packing solver with a naive and slow algorithm that distributes items one by one.
    """

    def __init__(self, total_items: int, bin_constraints: list[BinConstraint]) -> None:
        """
        New solver.
        """
        self.total_items = total_items
        self.bin_constraints = bin_constraints

        self.remaining_items = total_items
        self.result: list[int] = [0 for _ in bin_constraints]

    def _add_from_constraints(self) -> None:
        """
        Adds items to the result based on constraints. Updates `remaining_items`.
        """
        for i, bin_constraint in enumerate(self.bin_constraints):
            if bin_constraint == "none":
                self.result[i] = 0
                continue

            constraint_type, constraint_value = bin_constraint
            if constraint_type == "min":
                self.result[i] = constraint_value
                self.remaining_items -= constraint_value
                continue

            if constraint_type == "max":
                self.result[i] = 0
                self.remaining_items -= constraint_value
                continue

            raise ValueError(f"Unknown bin constraint type: {constraint_type}")

    def _bin_accepts_new_item_with_constraint(self, bin_index: int) -> bool:
        """
        Indicates if a bin can accept a new item based solely on its constraints.
        """
        # Find the bin constraint.
        bin_constraint = self.bin_constraints[bin_index]

        if bin_constraint == "none":
            return True

        bin_content = self.result[bin_index]
        bin_constraint_type, bin_constraint_value = bin_constraint

        if bin_constraint_type == "min":
            return True
        if bin_constraint_type == "max":
            return bin_content > bin_constraint_value

        raise ValueError(f"Unknown bin constraint type: {bin_constraint_type}")

    def _bin_accepts_new_item(self, bin_index: int) -> bool:
        """
        Indicates if a bin can accept a new item, according to its constraints and the state of other bins.
        """
        # If constraints don't allow, it's a no.
        if self._bin_accepts_new_item_with_constraint(bin_index) is False:
            return False

        # If any bin has fewer items than this bin, it's a no.
        return not any(
            self._bin_accepts_new_item_with_constraint(i)
            and self.result[i] < self.result[bin_index]
            for i in range(len(self.result))
        )

    def _smallest_bin_accepting_an_item(self) -> int:
        """
        Find the index of the smallest bin that accepts an item.
        """
        return min(range(len(self.result)), key=self._bin_accepts_new_item)

    def solve(self) -> Union[list[int], None]:
        """
        Solve the custom bin packing problem with a dumb algorithm that distributes items one by one.
        """
        # Populate each bin with an item that matches its constraint.
        self._add_from_constraints()

        # If there are remaining items, distribute them one by one like a dumb person who doesn't know what else to do.
        bin_index = 0
        while self.remaining_items > 0:
            # Give an item to the bin if it accepts it.
            if self._bin_accepts_new_item(bin_index):
                self.result[bin_index] += 1
                self.remaining_items -= 1

            bin_index += 1

            # If we exceed the end of the list, go back to the beginning.
            if bin_index == len(self.result):
                bin_index = 0

        return self.result
