import bitio
import huffman
import pickle

def read_tree(tree_stream):
    '''Read a description of a Huffman tree from the given compressed
    tree stream, and use the pickle module to construct the tree object.
    Then, return the root node of the tree itself.

    Args:
      tree_stream: The compressed stream to read the tree from.

    Returns:
      A Huffman tree root constructed according to the given description.
    '''
    try:
      # Read Tree Use the Pickle Module
      tree = pickle.load(tree_stream)
    except Exception:
      print('Read Tree Error')
      exit()
    #Return the Tree Value
    return(tree)

def decode_byte(tree, bitreader):
    """
    Reads bits from the bit reader and traverses the tree from
    the root to a leaf. Once a leaf is reached, bits are no longer read
    and the value of that leaf is returned.

    Args:
      bitreader: An instance of bitio.BitReader to read the tree from.
      tree: A Huffman tree.

    Returns:
      Next byte of the compressed bit stream.
    """
    Traverses = tree
    while True:
      try:
        readbyte = bitreader.readbit()
        # Left Child with bit 0
        if readbyte == 0:
            Traverses = Traverses.getLeft()
        # Right Child with bit 1
        elif readbyte == 1:
          Traverses = Traverses.getRight()
        # Continue Statment to continue the readbit() across the TreeBranch
        if type(Traverses) == huffman.TreeBranch:
          continue
        # Get TreeLeaf value and return it
        elif type(Traverses) == huffman.TreeLeaf:
          return(Traverses.getValue())
      except Exception:
        print('Decode Error')
        exit()

def decompress(compressed, uncompressed):
    '''First, read a Huffman tree from the 'compressed' stream using your
    read_tree function. Then use that tree to decode the rest of the
    stream and write the resulting symbols to the 'uncompressed'
    stream.

    Args:
      compressed: A file stream from which compressed input is read.
      uncompressed: A writable file stream to which the uncompressed
          output is written.
    '''
    # Get the Tree
    tree = read_tree(compressed)
    file_Reader = bitio.BitReader(compressed)
    file_Writer = bitio.BitWriter(uncompressed)
    # Booleams to control the while loop
    Nonebit = True
    try:
      while Nonebit:
        # Get the value from the decode_byte on the TreeLeaf
        byte = decode_byte(tree,file_Reader)
        # Write the bits to decompress
        if byte is not None:
          file_Writer.writebits(byte,8)
        # False statment to end of writebits
        else:
          Nonebit = False
    except Exception:
      print('Decompress Error')
      exit()
def write_tree(tree, tree_stream):
    '''Write the specified Huffman tree to the given tree_stream
    using pickle.

    Args:
      tree: A Huffman tree.
      tree_stream: The binary file to write the tree to.
    '''
    try:
      # Write Tree Use the Pickle Module
      tree = pickle.dump(tree,tree_stream)
    except Exception:
      print('Write Tree Error')
      exit()

def compress(tree, uncompressed, compressed):
    '''First write the given tree to the stream 'compressed' using the
    write_tree function. Then use the same tree to encode the data
    from the input stream 'uncompressed' and write it to 'compressed'.
    If there are any partially-written bytes remaining at the end,
    write 0 bits to form a complete byte.

    Flush the bitwriter after writing the entire compressed file.

    Args:
      tree: A Huffman tree.
      uncompressed: A file stream from which you can read the input.
      compressed: A file stream that will receive the tree description
          and the coded input data.
    '''
    # Write tree into file
    write_tree(tree,compressed)
    file_Reader = bitio.BitReader(uncompressed)
    file_Writer = bitio.BitWriter(compressed)
    # Get a dictionary with using make_encoding_table import from huffman
    encodeTable = huffman.make_encoding_table(tree)
    try:
      while True:
        # Make a list and use for loop to get 8 binary number in list
        bitslist = []
        for i in range(8):
          bitslist.append(str(file_Reader.readbit()))
        # Join the list as a string
        byte = ''.join(bitslist)
        # Encodeing value with use int() function in binary(2)
        matchvalue = encodeTable[int(byte,2)]
        # Match the correspoding value with the encoding table
        if int(byte,2) in encodeTable:
          for i in matchvalue:
            # Write the value 
            file_Writer.writebit(i)
    except EOFError:
      # Handle EOF flag, finshing with encodeing None
      Nonebit = encodeTable[None]
      for i in Nonebit:
        file_Writer.writebit(i)
      # Using the flush function to refresh the data in buffer.
      file_Writer.flush()
    except Exception:
      print('Compress Error')
      file_Writer.flush()
      exit()