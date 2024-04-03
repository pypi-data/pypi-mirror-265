from io import IOBase

def file_size(f: IOBase) -> int:
    cur = f.tell()
    f.seek(0, 2) # jump to eof
    size = f.tell()
    f.seek(cur) # jump to cur
    return size

def bytes_remaining(f: IOBase) -> int:
    return file_size(f) - f.tell()
