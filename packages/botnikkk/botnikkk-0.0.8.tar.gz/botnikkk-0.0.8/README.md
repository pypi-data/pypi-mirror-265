
# botnikkk  

Under construction! Not ready for use yet! Currently experimenting and planning!

Developed by BotNikkk / Nikkk

# Examples of How To Use

## 1. centre() function

Usage = Centering Elemtents.

```python
import botnikkk

botnikkk.centre('text')
```

It also takes 2 extra parameters as input :

1. symbol : determines what symbol will fill in the blank space, deault parameter = " "

```python
botnikkk.centre('text',symbol='=')
```

2. str_end : determines what symbol will print as end= in print statement, deault parameter = "\n"

```python
botnikkk.centre('text',str_end='\r')
```

## 2. format_input() function

Usage = centering the input variable.

```python
import botnikkk

botnikkk.format_input('input_question')
```

## 3. int_check() function

Usage = checks if an input variable is a interger or not, takes repetetive inputs if not Interger.

```python
import botnikkk

botnikkk.int_check('any_variable')
```

## 4. ans_check() function

Usage = takes a list of strings as input and displays it to the user as centred options, returns the choosen option. 

```python
import botnikkk

botnikkk.ans_check(['list_of_varibales'])
```

## 4. redirect() function

Usage = takes a input string as screen name and redirects the user to the said screen in a countdown of 3 seconds. Can only be used in async functions due it's await nature.

```python
import botnikkk
import asyncio

async def function():

    #some code
    await botnikkk.redirect("screen_name")
    #some more code

asyncio.run(function())
```

check out : https://botnikkk.github.io