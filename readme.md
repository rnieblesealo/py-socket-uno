# UNO Clone

### Modus Operandi

Card data is stored in tuples of the form `(kind, value)` where `kind` is the color *(red, blue, wild, etc...)* and `value` represents what it says *(1, 2, 3, etc...)*

Everything works by moving these tuples between arrays that represent the cards' "owners":

- `players` is an array containing $n$ subarrays such that $n$ is the amount of players
- `stack` is the array where we place cards according to game rules
- `pool` is where we draw cards from, if needed

Auxiliary functions may read/move the data between these arrays, according to game logic. **No objects are required.** This makes handling the eventual netcode lighter & easier.

Graphics will be handled in a similary read-based manner.
