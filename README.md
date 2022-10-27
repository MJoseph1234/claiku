# Claiku

A CLI Haiku assistant
***

**Claiku** helps you write haikus by counting and showing the number of syllables in each line of your poem.

[Picture or gif of claiku in action]

> a CLI haiku tool  
> to count syllables per line  
> in your great new poems

## CLI Options

### Short Form

Use the `-s` or `--short` flag to run **Claiku** in a short-form, 3-5-3 syllable mode.

[picture or gif of short form]

> seasons pass  
> but claiku remains  
> write haikus

### Color

Use `--no-color` to run the program without using ANSI color codes in the display or output.

## Saving your poems

By default, **Claiku** saves poems by appending them into a `haikus.txt` file in the current directory. You can change the output file by specifying a file after the  `-o` or `--output` flag.

## Future

 - Additional options for saving your haiku to file
 	- options to include date and timestamps so you can see when you wrote all of your haikus
 - Saving user configuration so flags and filepaths don't have to be specified every time
 - rewrite in Rust because I'm learning Rust