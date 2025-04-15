# Ulrik's Alg Genner

This project is for genning algs, and also has a generic solver for solving specific steps of the cube.
The program uses a unique way to generate move sequences which guarantees better algs and speeds up the search time by quite a lot.

## How to use

This code provides 3 key functions for you to use. gen_full_algs, generic_solver_setup, and generic_solver.
To take full advantage of these functions, you have to understand some components that are unique to this program.

### Move order
The program has a specific move order. 
This is important to keep in mind when making tables and so on.
The order is:
```
R	R2	R'	L	L2	L'	r	r2	r'	l	l2	l'	M	M2	M'	U	U2 	U'	D	D2	D'	u	u2	u'	d	d2	d'	E	E2	E'	F	F2	F'	B	B2	B'	f	f2	f'	b	b2	b'	S	S2	S'
```
This also means R has index 0, R2 index 1, ..., S' index 44

### Move Transition Tables
A move transition table (or just transition table) is a 2D array that you can define fully as you want. 
A transition table has 45 columns, one for each move, and as many rows as you want, with a minimum of 2 (first row will always be filled with 0s).
Such a table tells the program what moves are allowed at what time.
The easiest way to think of it is as grips, meaning you can tell the program which moves are allowed for which grips, and which grips you get to by applying the different moves.
Here is an example of what it may look like:
```
move_transition = np.array([ 
#   [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# Start (homegrip)
#   [ R,R2,R', L,L2,L', r,r2,r', l,l2,l', M,M2,M', U,U2,U', D,D2,D', u,u2,u', d,d2,d', E,E2,E', F,F2,F', B,B2,B', f,f2,f', b,b2,b', S,S2,S'],
    [ 2, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
])
```
In this table, I have 3 rows apart from the 0 row, which respectively represent homegrip, thumb on top, and thumb on bottom.
I've only included R and U moves in this example.
The program will read this as every non-zero element is allowed, so if you're in homegrip, then R, R', U, U2, and U' is allowed, but R2, L, L2, ... is not allowed.
If you for example apply an R, then that has a 2 in that column, meaning by applying R you get to grip 2, where R2('), R', U, U2, and U' is allowed.

You can edit the table as you want in move_transition_table.txt - this does not have the 0 row, and is a bit easier to read and edit since it only contains tab seperated numbers.

### Allowed Moves
Complementing the transition tables, you can also specified how many of each move you want to allow.
This is done by setting allowed_moves to an np.array of length 45, where each index represent a move, and the number in that index represent how many of that move is allowed.
```
#                  moves:[ R,R2,R', L,L2,L', r,r2,r', l,l2,l', M,M2,M', U,U2,U', D,D2,D', u,u2,u', d,d2,d', E,E2,E', F,F2,F', B,B2,B', f,f2,f', b,b2,b', S,S2,S'],
allowed_moves = np.array([50, 2,50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,50, 2,50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
```
This allows for 50 Rs, R's, Us, and U's. 50 is just an arbitrary "large" number, because you will never use algs with this many of one move.
However, R2 and U2 only has 2, meaning it will only generate algs with max 2 R2s and 2 U2s.
Similarly, it will not generate algs with any other move even if they were allowed by the move_transition, since allowed_moves has all other moves set to 0.

### Cubestate
The cubestate is simply an array of 54 elements, one for each sticker.
A solved cube looks like this:
```
np.array([1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,6])
```
You need to customize this based on what you want to generate/solve.
For example if you want to generate PLLs, you should make a cubestate where the side stickers of the top layer is set to another number, for example 0.
This will look like this:
```
np.array([0,0,0,1,1,1,1,1,1,0,0,0,2,2,2,2,2,2,0,0,0,3,3,3,3,3,3,0,0,0,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,6])
```

You may use this as a reference:
```
cubestate = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53])
cube = Cube(cubestate)
print(cube)

-----------------------------------
         36 37 38
         39 40 41
         42 43 44
27 28 29  0 1 2  9 10 11  18 19 20
30 31 32  3 4 5  12 13 14  21 22 23
33 34 35  6 7 8  15 16 17  24 25 26
         45 46 47
         48 49 50
         51 52 53
-----------------------------------
```

With these compontents explained, we can go over to the functions:

### gen_full_algs
Here is the definition of gen_full_algs:
```
def gen_full_algs(search_depth,
                  table_depth,
                  cubestate, 
                  move_transition = move_transition, 
                  start_grips = np.array([1]), 
                  allowed_moves = np.full(45, 10, dtype=np.int8), 
                  skip_U = True, 
                  prnt = True, 
                  categorize = True, 
                  category_state=np.array([1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,6]), 
                  return_full_alg_list = False, 
                  remove_regrips = False):
```
This function can generate full algs.
It uses a bidirectional search, or meet-in-the-middle.
The search works by setting a start and finish point that are identical.
It then generates algs from this state to itself, and then categorizes the algs afterwards

To generate an algset with this, you need to define *search_depth* and *table_depth*.
The algs will be of max length search_depth + table_depth, and a rule of thumb is to try to equal them as much as possible.
If you want algs of length 14, set both to 7 for example.
The table takes some time to generate, which consumes some memory, but is used efficiently afterwards.
The search algs are very fast to generate, and consumes relatively little memory, but takes a lot of time to go through.
You also need to define a cubestate
You also need to pass the move transition table, and you may want to define which starting grips you allow.
From the example table above, if you set *start_grips = np.array([1])*, then that's the same as saying all your algs start in homegrip.
You can use *start_grips = np.array([1,2,3])* if you want to be tell the program to start in any of the 3 grips you defined.
If you don't give it allowed_moves, it just gives it a default array where up to 10 of each move is allowed, since that will never be reached in practice.
Keep in mind that if you allow **N** of a certain move, then that goes for both the search algs and table algs, so you're really allowing **2N** moves.
*skip_U* is a variable that allows you to ignore AUF when genning algs, meaning it will not find algs starting or ending with any U move.
*prnt* allows you to print the progress. 
Some stuff is printed regardless, and if your search is relatively quick it might be better to not have it as it prints out a lot quickly.
If you're doing a long search, it might be helpful to set this to True so you see how far it has come, and get an idea of how long the full search will take.
Next up is some categorize-variables. 
*categorize* is a boolean telling the program if the cases should be categorized.
If this is set to False, then a list of all the algs that has been found will be returned - which you may use if you want to process them further from this point.
If it is set to True, then a dictionary is made with a unique ID for all the cases.
To categorize properly, you also need a cubestate. 
By default, this is set to the solved state, but you may want to change this depending on what you generate.
For example, if you're generating OLLs, you should set the cubestate to a state with LL removed (all 0s), and category_state to a state with the top layer's side stickers removed (same as the example above for generating PLLs).
If *skip_U* is set to True, it will add pre-auf on the cases that need it.
You can set *return_full_alg_list = True* if you also want the full list of algs in addition to the dictionary.
Finally, you can also set *remove_regrips=True* if you want it to remove algs that require regrips (according to the transition table).
Since the search is a meet-in-the-middle, it is not guaranteed that the final algs will fully follow the transition table.
However, if you've ensured that you don't require any regrips with your table, then there will max be 1 regrip.
If you however want to just remove all such algs, set this to true (although I don't recommend it as you might end up missing some shorter algs that are still good).

Here is an example for genning PLL algs:
```
search_depth = 8
table_depth = 8
# PLL
cubestate = np.array([0,0,0,1,1,1,1,1,1,0,0,0,2,2,2,2,2,2,0,0,0,3,3,3,3,3,3,0,0,0,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,6])
move_transition = transition_table
start_grips = np.array([1,2,3])
# moves                   R  R2 R' L  L2 L' r  r2 r' l  l2 l' M  M2 M' U  U2 U' D  D2 D' u  u2 u' d  d2 d' E  E2 E' F  F2 F' B  B2 B' f  f2 f' b  b2 b' S  S2 S'
allowed_moves = np.array([10, 2,10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,10, 2,10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
skip_U = True
prnt = True
categorize = True
category_state=np.array([1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,6])
return_full_alg_list = False
remove_regrips = False

PLLs = gen_full_algs(search_depth, table_depth, cubestate, move_transition, start_grips, allowed_moves, skip_U, prnt, categorize, category_state, return_full_alg_list, remove_regrips)
```

###  generic_solver_setup and generic_solver
generic_solver is a solver that can be used to solve any state, but it requires search algs and a table, which in turn requires you to use generic_solver_setup first.

```
    generic_solver_setup(cubestate, 
                         search_depth, 
                         table_depth, 
                         move_transition=move_transition, 
                         allowed_moves = np.full(45, 10, dtype=np.int8), 
                         start_grips=np.array([1]), 
                         skip_U=False, 
                         prnt=True)
```
This function returns *search_algs* and *table*.
It works similar to the alg-genner above.
However, in this case you should choose a cubestate where the pieces you don't care about don't exist.
For example, if you want a cross-solver, you should set LL and all pairs to 0.
I also recommend setting *search_depth* as low as possible and *table_depth* as high as possible.
This means the setup function will take more time to run, but in turn the generic_solver will be much faster.
*skip_U* means the algs won't start nor end with any U move.


```
    generic_solver(scramble, 
                   cubestate, 
                   search_algs, 
                   table, 
                   string_alg = True,
                   solve_CP = False)
```
To solve a case, use this function, where *search_algs* and *table* is generated from the function above.
*scramble* is any scramble of your choosing, and *cubestate* needs to be the same as the cubestate you used in *generic_solver_setup*.
*string_alg = True* means you get an alg in a text format, such as *R U R' U'*.
If this is set to False, the same alg will be set to *[0, 15, 2, 17]* (the move index version of the same alg).
This may be useful if you don't care about the exact solutions.
For example, you may use it to find stats, in which case you can set it to False.
Then finding the movecount can be done by taking the length of the solution directly.
If solve_CP = True, it will only accept solutions where the DL corners are in the correct positions and the rest of the corners can be solved with only R and U moves.


# Note!
Keep in mind, there are still a lot of improvements that can be made to this program in terms of speed.

# TODO!
* Add setup moves to "scrambled" and "solved" cubestate. This allows searching for WV algs for example
