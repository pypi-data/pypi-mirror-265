# Python text menu
Python module for interacting with the user through console

## Simple use
```python
options = ['Option 1', 'Option 2', 'Option 3']
choice = print_menu(options)
```
Output:
```
Menu:
[1] Option 1
[2] Option 2
[3] Option 3
[4] Exit
Select an option: 
```

Then you can create your own flow based on 'choice':
```
if choice == '1':
    # Do something
elif choice == '2':
    # Do something else
...
```

## Customize

You can customize it by giving it a title, a separator and/or an input text:


```python
options = ['Option 1', 'Option 2', 'Option 3']
choice = print_menu(options, title='New title', sep=''*20, input_text='Choose something...')
```
Output:
```
New title:
====================
[1] Option 1
[2] Option 2
[3] Option 3
[4] Exit
Choose something...
```
