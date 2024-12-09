
from dataclasses import dataclass

@dataclass
class FileBlock:
    index:int
    start:int
    len:int
    def checksum(self):
        csum = 0
        for i in range(self.len):
            csum += (self.start + i)*self.index
        return csum

@dataclass
class EmptyBlock:
    start:int
    len:int

# Compact the drive to the left as far as possible and return the checksum
def compact_and_checksum(fileblocks, emptyblocks):
    # start with the rightmost fileblock and iterate down
    fileblock_index = len(fileblocks) - 1
    while True:
        # Find the leftmost empty block with space for the current fileblock
        # that appears to the left of the fileblock
        for i in range(len(emptyblocks)):
            # Empty block must be to the left of the fileblock
            if emptyblocks[i].start > fileblocks[fileblock_index].start:
                break
            if emptyblocks[i].len >= fileblocks[fileblock_index].len:
                # Move the fileblock and update the empty block start and 
                # length, deleting the empty block from the list if it is 
                # completely filled.
                fileblocks[fileblock_index].start = emptyblocks[i].start
                if emptyblocks[i].len > fileblocks[fileblock_index].len:
                    emptyblocks[i].start += fileblocks[fileblock_index].len
                    emptyblocks[i].len -= fileblocks[fileblock_index].len
                else:
                    del emptyblocks[i]
                break
        fileblock_index -= 1
        if fileblock_index < 0:
            break
    # calculate checksum across all file blocks
    checksum = 0
    for i in range(len(fileblocks)):
        checksum += fileblocks[i].checksum()
    return checksum

# Use the diskmap to lay out a set of fileblocks and empty blocks, compact the 
# system and return the checksum.
def compact_diskmap(vals, allow_file_fragmentation=True):
    start_index = 0
    block_index = 0
    fileblocks = []
    emptyblocks = []
    # Build a list of fileblocks and emptyblocks using the diskmap. If 
    # fragmentation is permitted, a fileblock is added as multiple blocks of 
    # length 1. Otherwise, fileblocks are added as single blocks of the given 
    # length
    for i in range(len(vals)):
        if i % 2 == 0:
            # add fileblock(s)
            if allow_file_fragmentation:
                for j in range(vals[i]):
                    fileblocks.append(FileBlock(index=block_index, start=start_index, len=1))
                    start_index += 1
            else:
                fileblocks.append(FileBlock(index=block_index, start=start_index, len=vals[i]))
                start_index += vals[i]
            block_index += 1
        else:
            # add emptyblocks
            emptyblocks.append(EmptyBlock(start=start_index,len=vals[i]))
            start_index += vals[i]
    return compact_and_checksum(fileblocks, emptyblocks)
    
def day9(lines):
    # Break the disk map into a list of ints
    vals = list(map(lambda x: int(x),list(lines[0])))
    part1 = compact_diskmap(vals, allow_file_fragmentation=True)
    part2 = compact_diskmap(vals, allow_file_fragmentation=False)
    print("Part 1:", part1)
    print("Part 2:", part2)
