# A.M.: 5361
# Anna Tarasidou


class Point:
    # 2D spatial point (x,y)
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class MBR:
    # Minimum Bounding Rectangle < x-low, y-low, x-high, y-high >
    def __init__(self, x_low: float, y_low: float, x_high: float, y_high: float):
        self.x_low = x_low
        self.y_low = y_low
        self.x_high = x_high
        self.y_high = y_high

    def __repr__(self):
        return f"[{self.x_low}, {self.y_low}, {self.x_high}, {self.y_high}]"


class LeafEntry:
    # Entry to leaf node
    def __init__(self, record_id: int, point: Point):
        self.record_id = record_id
        self.point = point

    def __repr__(self):
        return f"({self.record_id}, {self.point})"


def load_data(filepath: str) -> list[LeafEntry]:
    # Reads Data File, Returns list of LeafEntry objects
    entries = []

    with open(filepath, 'r', encoding='utf-8') as file:
        first_line = file.readline().strip()
        if not first_line:
            return entries

        total_points = int(first_line)
        print(f"Total points: {total_points}")

        # Read the coordinates line by line
        record_id = 1
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                x = float(parts[0])
                y = float(parts[1])
                point = Point(x, y)

                # Create a LeafEntry <record-id, point>
                entry = LeafEntry(record_id, point)
                entries.append(entry)

                record_id += 1

    return entries


MAX_LEAF_CAP = 51
MIN_LEAF_CAP = 20

MAX_INT_CAP = 28
MIN_INT_CAP = 11


class Node:
    # Node in the r_tree
    def __init__(self, node_id: int, level: int, is_leaf: bool):
        self.node_id = node_id
        self.level = level
        self.is_leaf = is_leaf
        self.entries = []
        self.mbr = None

    def add_entry(self, entry):
        self.entries.append(entry)

    def __repr__(self):
        return f"Node(id={self.node_id}, level={self.level}, is_leaf={self.is_leaf}, entries={len(self.entries)})"


def split_into_nodes(entries: list, max_cap: int, min_cap: int) -> list[list]:
    # Splits entries in maximum capacity nodes
    if not entries:
        return []

    # If all entries fit in a single node return them
    if len(entries) <= max_cap:
        return [entries]

    blocks = []
    # Split by max capacity
    for i in range(0, len(entries), max_cap):
        blocks.append(entries[i: i + max_cap])

    # Check if there is underflow of the last block
    if len(blocks) > 1:
        last_block = blocks[-1]
        if len(last_block) < min_cap:
            need = min_cap - len(last_block)
            previous_block = blocks[-2]
            borrow = previous_block[-need:]

            blocks[-2] = previous_block[:-need]
            blocks[-1] = borrow + last_block

    return blocks
