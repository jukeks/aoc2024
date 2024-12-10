from aoc.lib import (
    Matrix,
    create_matrix,
    print_matrix,
    parse_matrix,
    neighbor_indexes_diagonal,
    read_matrix,
    neighbors_diagonal,
    read_input,
)
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
import itertools


test_input = """\
2333133121414131402"""
#test_input = "12345"

Offset = int

@dataclass
class File:
    id: int
    blocks: list[Offset]

    def size(self) -> int:
        return len(self.blocks)

@dataclass
class Space:
    blocks: list[Offset]

    def size(self) -> int:
        return len(self.blocks)


@dataclass
class FAT:
    size: int
    files: list[File]
    unallocated: list[Space]

    @classmethod
    def parse(cls, text: str) -> 'FAT':
        files = []
        unallocated = []
        offset = 0
        id = 0
        for p in itertools.batched(text, n=2):
            if len(p) == 2:
                file_len = int(p[0])
                free_len = int(p[1])
            else:
                file_len = int(p[0])
                free_len = 0

            files.append(File(
                id=id,
                blocks=[offset + i for i in range(file_len)]
            ))

            offset += file_len
            if free_len:
                unallocated.append(Space(
                    blocks=[offset + i for i in range(free_len)]
                ))

            offset += free_len
            id += 1

        return FAT(size=offset, files=files, unallocated=unallocated)
    
    def defrag(self, file: File) -> bool:
        new_unallocated = file.blocks.copy()
        new_unallocated.sort()
        unallocated_chunk = self.unallocated[0].blocks
        for block_i in range(len(file.blocks) -1, -1, -1):
            if not unallocated_chunk:
                self.unallocated.pop(0)
                unallocated_chunk = self.unallocated[0].blocks
            
            block = file.blocks[block_i]
            if unallocated_chunk[0] > block:
                return True

            unallocated_block = unallocated_chunk.pop(0)
            file.blocks[block_i] = unallocated_block
            self.print()

        self.unallocated.append(Space(new_unallocated))
        self.consolidate_unallocated()

    def defrag_whole(self, file: File) -> bool:
        for free in self.unallocated:
            if free.blocks[0] > file.blocks[0]:
                # already defragged
                return True
            if free.size() < file.size():
                continue

            file_size = file.size()
            new_free = file.blocks
            file.blocks = free.blocks[:file_size]
            free.blocks = free.blocks[file_size:]
            self.unallocated.append(Space(new_free))
            self.consolidate_unallocated()
            return True

        return False

    def consolidate_unallocated(self) -> None:
        self.unallocated.sort(key=lambda x: x.blocks[0] if len(x.blocks) else 0)
        removed = []
        for i, a in enumerate(self.unallocated[:len(self.unallocated)-1]):
            b = self.unallocated[i+1]
            if not a.blocks:
                removed.append(a)
                continue
            if not b.blocks:
                removed.append(b)
                continue

            if a.blocks[-1] + 1 == b.blocks[0]:
                # merge
                removed.append(a)
                b.blocks = a.blocks + b.blocks
                a.blocks = []
        
        for r in removed:
            try:
                self.unallocated.remove(r)
            except:
                pass

    def is_defragged(self) -> bool:
        return len(self.unallocated) == 1 and self.unallocated[0].blocks[-1] + 1 == self.size

    def print(self):
        alloc = ["." for _ in range(self.size)]
        for f in self.files:
            for b in f.blocks:
                alloc[b] = str(f.id)
        
        print("".join(alloc))

    def checksum(self) -> int:
        alloc = [0 for _ in range(self.size)]
        for f in self.files:
            for b in f.blocks:
                alloc[b] = f.id

        total = 0
        for i, id in enumerate(alloc):
            total += i*id
        return total


def main():
    test_input = read_input("aoc/09/input.txt")
    fat = FAT.parse(test_input)
    print(fat)
    fat.print()

    for file in fat.files[::-1]:
        fat.defrag_whole(file)
        #fat.print()
        if fat.is_defragged():
            break

    #fat.print()
    print("checksum", fat.checksum())


if __name__ == "__main__":
    main()
