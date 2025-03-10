from typing import Any


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __repr__(self) -> str:
        return f"({self.row}, {self.column})"


class Ship:
    def __init__(
            self, start: tuple, end: tuple, is_drowned: bool = False
    ) -> None:
        self.decks = []
        self.start = start
        self.end = end
        self.is_drowned = is_drowned

        if start[0] == end[0]:
            if start[1] > end[1]:
                row = start[0]
                for col in range(end[1], start[1] + 1):
                    self.decks.append(Deck(row, col))
                return

            row = start[0]
            for col in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, col))
            return

        if start[1] == end[1]:
            if start[0] > end[0]:
                col = start[1]
                for row in range(end[0], start[0] + 1):
                    self.decks.append(Deck(row, col))
                return

            col = start[1]
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, col))
            return

    def get_deck(self, row: int, column: int) -> Any:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                deck.is_alive = False

        if all(not deck.is_alive for deck in self.decks):
            self.is_drowned = True

    def __repr__(self) -> str:
        return f"{self.decks}"


class Battleship:
    def __init__(self, ships: list[tuple[tuple, tuple]]) -> None:
        self.field = {}

        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def print_field(self) -> None:
        matrix_field = []

        for row_item in range(10):
            row = []
            for col_item in range(10):
                if (row_item, col_item) in self.field:
                    ship = self.field[(row_item, col_item)]
                    deck = ship.get_deck(row_item, col_item)
                    if ship.is_drowned:
                        row.append("x")
                    elif not deck.is_alive:
                        row.append("*")
                    else:
                        row.append("□")
                else:
                    row.append("~")
            matrix_field.append("  ".join(row))

        for row in matrix_field:
            print(row)

    def fire(self, location: tuple) -> str:
        row, col = location
        if not (0 <= row < 10 and 0 <= col < 10):
            return "Invalid coordinates! Out of bounds."

        if location in self.field:
            ship = self.field[location]
            ship.fire(location[0], location[1])
            if ship.is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"
