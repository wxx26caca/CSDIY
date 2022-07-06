# VIM BASICS
## Staring VIM
## Buffers, Windows and Tabs
make sure have the `set hidden` option in vimrc
### Buffers
Running `vim file1 file2 ...` creates n amount of buffers.
Each time you open a new file, Vim create a new buffer for it.
- see all the buffers `:buffers` or `:ls`
- go to next/previous buffer `:bnext`/`bprevious`
- go to n buffer `:buffer n`
- delete n buffer `:bdelete n`
### Exiting Vim
close all of the buffers use quit-all `:qall` `:qall!` `:wqall` 
### Windows
A window is a viewport on a buffer.
- `split file2`
- `vsplit file3`
- move shortcuts
  * C-W H  move the cursor to the left window
  * C-W J  move the cursor to the down window
  * C-W K  move the cursor to the up window
  * C-W L  move the cursor to the right window
- create shortcuts
  * C-W V  open a new vertical split
  * C-W S  open a new horizontal split
  * C-W C  close a windwow
  * C-W O  keep current window on screen and closes others
### Tabs
- `tabnew file`
- `tabclose`
- `tabnext`
- `tabeprevious`
- `tablast`
- `tabfirst`
## Searching Files
### Opening And Editing Files
open a file in vim `:edit`
- examples
  * basic usage. `edit file.txt`
  * use `<Tab>` to autocomplete. `edit a<Tab>b<Tab>c<Tab>`
  * open files with `.yml` in current directory. `edit *.yml<Tab>`
  * search recursively. use `*` and `**` wildcards. `edit **/*.md<Tab>` 
### Searching Files With Find
- examples
  * `find package.json`
  * `find p<Tab>`
### Find And Path
`:find` finds file in `path`, `:edit` doesn't.
check what your paths are. `:set path?`
By default, it looks like this: `path=.,/usr/include,,`
you can update path use: `set path+={your-path-here}` 
- `set path+=app/controllers/`
- `set path+=$PWD/**`
### Searching In Files With Grep
- Internal grep `:vim` it's short for `:vimgrep`
  * `:vim /pattern/ file` (jump to original file, check buffers and jump)
- External grep `:grep`
  * `:grep -irn 'test' file` (normal grep command)
### Browsing Files with Netrw
`netrw` built-in file explorer. To run `netrw`, add two settings in `.vimrc`
- set nocp
- filetype plugin on
vim-vinegar is a good plugin to import netrw.
NERDTree is another good choices.
### Fzf plugin make searching easy and powerful
## Vim Grammar
### Grammar Rule
the most import rule is : `verb + noun`
### Nouns (Motions)
- h  Left
- j  Down
- k  Up
- l  Right
- w  move forward to the beginning of the next word
- }  Jump to the next paragraph
- $  Go to the end of the line
### Verbs (Operators)
- y  Yank text (copy)
- d  Delete text and save to register
- c  Delete text, save to register, and start insert mode
- p  Paste after the cursor
- P  Paste before the cursor
- a  editing one character ahead
  Examples:
  - y2h
  - d2w
  - c2j
  - dd
  - yy
  - cc
### More Nouns (Text Objects)
Two types of text objects: Inner and Outer text objects.
- i + object  Inner text object
- a + object  Outer text object
Example:
  your cursor is somewhere inside the parentheses in the expression `(hello vim)`
  - To delete the text inside the parentheses without deleting the parentheses
    `di(`
    output: ()
  - To delete the parentheses and text inside
    `da(`
    output: all delete
  Learn more: `:h text-objects`
### Composability And Grammar
Vim has a filter operator (external command operator) `!` to use external programs 
as filters for our texts.
Example: ```!} column -t -s "|" | awk 'NR > 1 && /Ok/ {print $0}'```
The `vim-textobj-user` (search in github) plugin allows to create your own text objects.
## Moving In A File
### Count Your Move
`[count] + motion`
12j, 9h, 6l, 7k
### Word Navigation
- w     Move forward to the beginning of the next word
- W     Move forward to the beginning of the next WORD
- e     Move forward one word to the end of the next word
- E     Move forward one word to the end of the next WORD
- b     Move backward to beginning of the previous word
- B     Move backward to beginning of the previous WORD
- ge    Move backward to end of the previous word
- gE    Move backward to end of the previous WORD
### Current Line Navigation
- 0     Go to the first character in the current line
- ^     Go to the first nonblank char in the current line
- g_    Go to the last non-blank char in the current line
- $     Go to the last char in the current line
- n|    Go the column n in the current line
### Sentence And Paragraph Navigation
A sentence ends with either `. ! ?` followed by an EOL, a space, or a tab.
- (     Jump to the previous sentence
- )     Jump to the next sentence
A paragraph begins after each empty line and also at each set of a paragraph
macro specified by the pairs of characters in paragraphs option.
A paragraph begins and ends after an empty line.
- {     Jump to the previous paragraph 
- }     Jump to the next paragraph 
`:h sentence` and `:h paragraph` to learn more.
### Match Navigation
- %     Navigate to another mathch, usually works for (), [], {}
### Line Number Navigation
Jump to line number n with `nG`.
Show total lines in a file, use `Ctrl+g`.  
### Window Navigation
- H     Go to top of screen
- M     Go to medium of screen
- L     Go to bottom of screen
- nH    Go n line from top 
- nL    Go n line from bottom 
### Scrolling
### Search Navigation
- /    Search forward for a match
- ?    Search backward for a match
- n    Repeat last search in same direction of previous search
- N    Repeat last search in opposite direction of previous search
### Marking Position
Use marks to save your current position and return to this position later.
- ma    Mark position with mark "a"
- `a    Jump to line and column "a"
- 'a    Jump to line "a"
:s   substitute
:tag    Jump to tag definition
## Insert Mode
### Ways To Go To Insert Mode
- i    Insert text before the cursor
- I    Insert text before the first non-blank character of the line
- a    Append text after the cursor
- A    Append text at the end of line
- o    Start a new line below the cursor and insert text
- O    Start a new line above the cursor and insert text 
- s    Delete the character under the cursor and insert text
- S    Delete the current line and insert text
- gi   Insert text in same position where the last insert mode was stopped
- gI   Insert text at the start of line
### Different Ways To Exit Insert Mode
- <ESC>    Exits insert mode and go to normal mode
- Ctrl-[   Exits insert mode and go to normal mode
- Ctrl-C   Like Ctrl-[ and <ESC>, but does not check for abbreviation   
### Repeating Insert Mode
`10i`
For example, before entering insert mode, input `10i`, and the input `hello`
output is `hellohellohellohellohellohellohellohellohellohello`
This works with any insert mode(`10I`, `10a`, `10o`)
### Deleting Chunks In Insert Mode
- Ctrl-H    Delete one character
- Ctrl-W    Delete one word
- Ctrl-U    Delete the entire line
### Insert From Register
`"ayiw`
- "a tells vim that the target of your next action will go to register a
- yiw yanks inner word.
### Scrolling
press Ctrl-X, vim will enter sub-mode
- Ctrl-X and then Ctrl-Y    Scroll up
- Ctrl-X and then Ctrl-E    Scroll down
### Autocompletion
- Ctrl-X and then Ctrl-L    Insert a whole line 
- Ctrl-X and then Ctrl-N    Insert a text from current file
- Ctrl-X and then Ctrl-I    Insert a text from included files
- Ctrl-X and then Ctrl-F    Insert a file name
### Executing A Normal Mode Command
press Ctrl-O, vim will enter insert-normal sub-mode.
In this mode, you can do one normal mode command.
For example:
- Repeating text    Ctrl-O 100ihello    Insert hello 100 times
- Executing terminal commands    Ctrl-O !! pwd    Run pwd
- Deleting faster    Ctrl-O dtz    Delete from current location till the letter "z"
## The Dot Command
`:h .` the dot command repeats the last change.
## Registers

## Settings
### Set tab to 4 space
set tabstop=4
set shiftwidth=4
set expandtab
### Disable arrow buttons
noremap \<Up\> \<NOP\>
noremap \<Down\> \<NOP\>
noremap \<Left\> \<NOP\>
noremap \<Right\> \<NOP\>
### Relative Numbering
set relativenumber number
### Set highlight search
set hlsearch
### Mapping default key to other
inoremap jj <ESC>
## Practices
1. use Inner or Outer text objects to delete something.
`dit`, `dat`, `di<`
```
<div>
  <h1>Header1</h1>
  <p>Paragraph1</p>
  <p>Paragraph2</p>
</div>
```
2. use filter operator `!` to tabularize below
```
ID|Name|Cuteness
01|Puppy|Very
02|Kitten|Ok
03|Bunny|Ok
```
3. play around with sentence navigations {} and ()
```
Hello. How are you? I am great, thanks!
Vim is awesome.
It may not easy to learn it at first...- but we are in this together. Good luck!

Hello again.

Try to move around with ), (, }, and {. Feel how they work.
You got this.
```
4. Match navigation
```
   (define (fib n)
    (cond ((= n 0) 0)
        ((= n 1) 1)
        (else
          (+ (fib (- n 1)) (fib (- n 2)))
        )))
```
5. Dot
``` pancake, potatoes, fruit-juice,```
`df,..`

