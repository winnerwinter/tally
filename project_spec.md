# Project Spec

This is going to be a purely vibe coded project. I want a simple application to run locally to serve a use case that I commonly run into. Amongst friends, I commonly keep track of various "points" for an assortment of random things. At a high level all I want is a list of names or string identifiers and some numeric value next to it. There will be additional feature that I will go into further detail below. The entries should be sorted in value order, so the first entry is in 1st place, the second entry is in 2nd place, and so on. 

### Example
A 10
B 9
C 8
D 8
E 7
F 5

### Features
- I want a UI, this can just be a desktop application that runs locally. I do not need the application to remember any kind of state, so it should just be able to load a file with data. This file is the state, and the application just interacts with the file.
- This file can probably be a JSON format, and needs to conform to a schema that this tool understands. Files that do not comform are unable to be loaded by the tool.
- From the UI, if I do not have a file to load, I can create an empty file, with no entries.
- I want a title to this particular list that I can edit.
- I want to be able to add entries that are initialized to 0
- I want to be able to edit entry names.
- I want to be able to increment and decrement entries values
- I want to be able to print a nice human readable format of the state that I can copy paste to other places.
- After entering a series of increments and decrements of various entries, and/or new entries, there will be a new state. I want a save button to record that new state, which will update the file. After updating, I want to have a specialized dump, that not only prints each entry, but prints an up or down arrow, and place changes since the old state. For example, after clicking update
- Clicking update updates the file and copys the specialized dump to the clipboard.
- I want a separate button that copys the simple dump to my clipboard.


### Edge Cases To consider
- Entries with the same point value should be ordered in the time they achieved that point value. In other words, there are no ties. This ordering should be not be encoded in the schema. If I mess up incrementing and decrementing, I can just increment and decrement to get myself to my desired state. And the specialized dump just doesn't represent reality. That is okay.
- Do not allow entries with the same name. Just give a warning if I try to add one.