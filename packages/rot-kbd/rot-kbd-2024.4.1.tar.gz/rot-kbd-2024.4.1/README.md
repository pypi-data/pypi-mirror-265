# rot-kbd

A highly insecure encryption scheme based on rot13 and keyboard layouts

Use as a Python module

```pycon
>>> from rot_kbd import *

>>> rot_wertyq('qwerty')
'wertyu'
>>> rot_yqwert(rot_wertyq('qwerty'))
'qwerty'

>>> rot_wertyq('wasd')
'esdf'
>>> rot_yqwert(rot_wertyq('wasd'))
'wasd'
```

Or on the command line

```console
$ echo 'qwerty' | python -mrot_kbd
wertyu
$ echo 'qwerty' | python -mrot_kbd | python -mrot_kbd --rotation rot_yqwert
qwerty
```

## Supposedly Asked Questions

### Is this secure?

Absolutely not, it's not even close. `rot_wertyq` and `rot_yqwert` are
certified upto an adversary rated SA 8.75 (Sibling, Age 8¾).
