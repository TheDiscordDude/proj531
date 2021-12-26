def getPiece(coords:str):
    return (ord(coords[0])-97)+(int(coords[1:])-1)*8