## Course overview the shell
1. echo $SHELL
2. create a new directory called `missing` under `/tmp`
3. man touch
4. use `touch` to create a new file `semester` in `missing`
5. write the following into that file
   ``` 
   #!/bin/sh 
   curl --head --silent https://missing.csail.mit.edu
   ```
   see bash quoting manual page for more information about `'` and `"`
6. try to execute the file use `./semester`
7. try to execute use `sh semester`
8. man chmod
9. see `shebang` for more information
10. use `|` and `>` to write "last modified" date output by `semester` into a file called `last-modified.txt` in your home directory.
11. reads out power level or your machine's CPU temperture from `/sys`
## Shell Tools and Scripting
1. read `man ls` and write an `ls` command that lists files in the following manner.
   - includes all files, including hidden files
   - sizes are listed in human readable format
   - files are ordered by recency
   - output is colorized
2. Write bash function `macro` and `polo` that do the following.
   - execute `macro` the current working directory should be saved in some manner
   - execute `polo` should `cd` you back to the directory where you executed `macro`
3. Write a bash script that runs the following script until it fails and captures its standard output and error streams to files and prints everything at the end. Bonus points if you can also report how many runs it took for the script to fail.
   ```
   #!/usr/bin/env bash
   
   n=$(( RANDOM % 100 ))
   
   if [[ n -eq 42 ]]; then
      echo "Something went wrong"
      >&2 echo "The error was using magic numbers"
      exit 1
   fi
   
   echo "Everything went according to plan"
   ```
4. man xargs
   write a command that recursively finds all HTML files in the folder and makes a zip with them. Note that your command should work evev if the files have spaces (hint: check `-d` for `xargs`).
5. Write a command or script to recursively find the most recently modified file in a directory. More generally, can you list all files by recency?  
## Vim
1. Complete `vimtutor` in `80*24` size.
2. Download [basic vimrc](https://missing.csail.mit.edu/2020/files/vimrc) and save it to `~/.vimrc`.
3. Install an configure a plugin: [ctrlp.vim](https://github.com/ctrlpvim/ctrlp.vim).
   - Create the plugins directory `mkdir -p ~/.vim/pack/vendor/start`.
   - Download the plugin `cd ~/.vim/pack/vendor/start; git clone https://github.com/ctrlpvim/ctrlp.vim`.
   - Read the documentation for the plugin. Try using CtrlP to locate a file by navigating to a project directory, opening Vim, and using the Vim command-line to start `:CtrlP`.
   - Customize CtrlP by adding [configuration](https://github.com/ctrlpvim/ctrlp.vim/blob/master/readme.md#basic-options) to your `~/.vimrc` to open CtrlP by pressing Ctrl-P.
4. re-do the Demo from lecture on your own machine.
5. Use Vim for *all* your text editing for the next month.
6. Configure your other tools to use Vim bindings.
7. Further customize your `~/.vimrc` and install more plugins.
8. Convert XML to JSOM using Vim macros.
