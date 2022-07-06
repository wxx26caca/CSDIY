- **Normal**: for moving around a file and making edits
- **Insert**: for insert text
- **Replace**: for replacing text
- **Visual**: for selecting blocks of text
- **Command-line**: for running a command

change modes
- `<ESC>` to switch from any mode back to Normal mode
- From normal mode
  - `i` to insert mode
  - `R` to replace mode
  - `v` to visual mode
  - `V` to visual line mode
  - `<C-v>` to visual block mode
  - `:` to command line mode
> consider remapping Caps Lock to Escape

Movement
- Basic:  `hjkl`
- Words:  `b` (beginning of word), `w` (next word), `e` (end of word)
- Lines:  `0` (beginning of line), `^` (first non-blank character), `$` (end of line)
- Screen: `H` (top of screen), `M` (middle of screen), `L` (bottom of screen)
- Scroll: `C-u` (up), `C-d` (down)
- File:   `gg`, `G`, `nG`
- Misc:   `%` (corresponding item)
- Find:   `f/t/F/T{character}` find/to/forward/backward character on the current line, `,/;` for navigating matches 
- Search: `/{regex}`, `n/N` for navigating matches 

Edits
- `i`
- `o/O`: insert line below/above
- `d{motion}`: `dw` delete word, `d$` delete to end of line, `d0` delete to beginning of line
- `c{motion}`: `cw` change word, equal to `d{motion} + i`
- `x`: delete character, equal to `dl`
- `s`: substitute character, equal to `xi` 
- Visual mode + manipulation
  - select text, `d` to delete it or `c` to change it
- `u/<C-r>`: undo/redo
- lots more to learn: e.g. `~` flips the case of a character

Counts
- `3w` move 3 words forward
- `5j` move 5 lines down
- `7dw` delete 7 words

Modifiers
- `ci(` **change** the contents **inside** the current pair of **parentheses**
- `ci[` **change** the contents **inside** the current pair of **square brackets**
- `da'` **delete** a single-quoted string, including the **surrounding** single quotes

Vim-mode in other programs
Shell
- Bash user: `set -o vi`
- Zsh: `bindkey -v`
- Fish: `fish_vi_key_bindings`
- `export EDITOR=vim`
Readline
Many programs use [GNU Readline](https://tiswww.case.edu/php/chet/readline/rltop.html) library for their command-line interface.

Advanced Vim
think **"there must be a better way of doing this"**

Search and replace
`:s`
- `%s/foo/bar/g`
- `%s/\[.*\](\(.*\))/\1/g`

Multiple windows:
`:sp`/`:vsp`

Move between splits
`<C-w> hjkl`

Macros
- `q{character}`: start recording a macro in register {character}
- `q`: stop recording
- `@{character}: replays the macro
- `{number}@{character}`: executes a macro {number} times
- Example: [convert xml to json](https://missing.csail.mit.edu/2020/files/example-data.xml) 

Resources
- `vimtutor` command
- [Vim Adventures](https://vim-adventures.com/)
- [Vim Tips Wiki](http://vim.wikia.com/wiki/Vim_Tips_Wiki)
- [Vim Advent Calendar](https://vimways.org/2019/)
- [Vim Golf](http://www.vimgolf.com/)
- [Vi/Vim Stack Exchange](https://vi.stackexchange.com/)
- [Vim Screencasts](http://vimcasts.org/)
- [Practical Vim book](https://pragprog.com/titles/dnvim2/)
