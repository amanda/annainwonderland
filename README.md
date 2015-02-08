annainwonderland
================

anna karenina in wonderland: takes people entities from one text and swaps them with the people in another. my project for [nanogenmo 2014](https://github.com/dariusk/NaNoGenMo-2014).

## requirements
- nltk
- numpy (for nltk)

## usage

install dependencies by running ```pip install -r requirements.txt```.

run the script using your source text (with people you want to replace) as the first argument and it will prompt you for the names of people to insert, or (optional) run using a list of people in a text file separated by newlines as the second argument flagged using -l:

```py
python annainwonderland.py sourcetextfile [-l listfile]
```

a file called 'sourcetextfile-swapped.txt' will appear in the current directory with your new people inserted.
