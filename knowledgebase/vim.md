# basic commands
`c` change

`d` delete

`y` copy

`p` paste after the cursor

`P` paste before the cursor

`r` replace

`yy` copy line

`dd` delete line


# move
`0` move to the beginning of a line

`$` move to the end of a line

`gg` move to the beginning of a file

`G` move to the end of a file

`ctrl f` move page forward

`ctrl b` move page backward

`)` move to the beginning of next sentence

`(` move to the previous sentence

`}` move to the next paragraph

`{` move to the previous paragraph

`/` search forwards

`?` search backwards

`ctrl o` move backward to the jump list

`ctrl l` move forward to the jump list

`:jumps` list jump list

`'.` move to last change


# windows and buffers
`:split` split windows into same buffer

`ctrl w w` move between windows

`ctrl w c` close window

`:new`+$filename open another file in same window

`:e`/`:edit` edit new file or another file

`:ls` list buffers

`:b`+number move to the specific buffer(number is found by `:ls`)

`:bd`+$filename delete buffer

`:e`+tab list buffers

`:e`+$prefix+tab list files start with the prefix

`:bn`, `:bp` move between buffers

`:b`+space+$filename move to specific buffer

`:e!` load the latest version of the file and disregard the changes



# mode
`shift v` visual line

`ctrl v` visual block


# registers
`"`+ a-zA-Z, e.g.:
- `"a yy` yank the line to the register a
- `"a p` paste from register a


# change block:
1. enter visual mode
2.  select block
3.  `c`
4.  enter new charactors
5.  go back to normal mode

# replace
`s/old/new` only replace the first occurrence

`s/old/new/g` for global


# marks
`m` create mark, e.g.:
1.  go to the exact line
2.  create a mark: `ma`, notes: `m`+a-zA-Z set the mark name, e.g.: `ma`, `a-z` local to the current buffer, `A-Z` global marks
3.  `'a` back to the mark


# read
`:r`+$filename read $filename into current file
