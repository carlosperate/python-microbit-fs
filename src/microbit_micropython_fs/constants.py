#!/usr/bin/env python3
"""Constants for the MicroPython filesystem."""

# =============================================================================
# Chunk Constants
# =============================================================================

CHUNK_SIZE = 128
"""Size of a filesystem chunk in bytes."""

CHUNK_DATA_SIZE = 126
"""Size of data that can be stored in a chunk (128 - 1 marker - 1 tail)."""

CHUNK_MARKER_SIZE = 1
"""Size of the chunk marker byte."""

MAX_CHUNKS = 252
"""Maximum number of chunks (256 - 4 reserved markers)."""

MAX_FILENAME_LENGTH = 120
"""Maximum length of a filename in bytes."""


class ChunkMarker:
    """Chunk marker byte values."""

    FREED = 0x00
    """Chunk has been freed but not erased."""

    PERSISTENT_DATA = 0xFD
    """Persistent data page marker (first byte of last FS page)."""

    FILE_START = 0xFE
    """Start of a file."""

    UNUSED = 0xFF
    """Empty/unused chunk."""
