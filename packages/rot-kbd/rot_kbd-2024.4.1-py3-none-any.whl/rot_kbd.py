"""
Like rot13(), but rotating left or right by one key on a keyboard

>>> rot_wertyq('qwerty')
'wertyu'
>>> rot_yqwert(rot_wertyq('qwerty'))
'qwerty'

>>> rot_wertyq('wasd')
'esdf'
>>> rot_yqwert(rot_wertyq('wasd'))
'wasd'
"""

from typing import Self


class _Keyboard:
    def __init__(self, rows):
        self._rows = tuple(row.replace(' ', '') for row in rows)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.rows!r})'

    @property
    def rows(self):
        return self._rows

    def characters(self) -> str:
        return ''.join(self.rows)

    def maketrans(self, other: Self) -> dict[int, int]:
        src_table = self.characters() + self.characters().upper()
        dst_table = other.characters() + other.characters().upper()
        return str.maketrans(src_table, dst_table)

    def rotated(self, n: int) -> Self:
        cls = type(self)
        return cls(rows=(row[-n:] + row[:-n] for row in self.rows))


_QWERTY = _Keyboard(rows=(
    'q w e r t y u i o p',
    ' a s d f g h j k l ',
    '  z x c v b n m    ',
))
_QWERTY_RL = _QWERTY.rotated(-1)  # QWERTY rotated left by 1
_QWERTY_RR = _QWERTY.rotated(+1)  # QWERTY rotated right by 1
_QWERTY_RL_TR = _QWERTY.maketrans(_QWERTY_RL)
_QWERTY_RR_TR = _QWERTY.maketrans(_QWERTY_RR)

def rot_wertyq(s: str) -> str:
    "Return s as if each letter was 1 to the right on a QWERTY keyboard."
    return s.translate(_QWERTY_RL_TR)

def rot_yqwert(s: str) -> str:
    "Return s as if each letter was 1 to the left on a QWERTY keyboard."
    return s.translate(_QWERTY_RR_TR)


_DVORAK = _Keyboard(rows=(
    '      p y f g c r l ',
    ' a o e u i d h t n s',
    '  q j k x b m w v z ',
))
_DVORAK_RL = _DVORAK.rotated(-1)  # DVORAK rotated left by 1
_DVORAK_RR = _DVORAK.rotated(+1)  # DVORAK rotated right by 1
_DVORAK_RL_TR = _DVORAK.maketrans(_DVORAK_RL)
_DVORAK_RR_TR = _DVORAK.maketrans(_DVORAK_RR)

def rot_vorakd(s: str) -> str:
    "Return s as if each letter was 1 to the right on a DVORAK keyboard."
    return s.translate(_DVORAK_RL_TR)

def rot_kdvora(s: str) -> str:
    "Return s as if each letter was 1 to the left on a DVORAK keyboard."
    return s.translate(_DVORAK_RR_TR)


__all__ = [
    rot_wertyq.__name__,
    rot_yqwert.__name__,
    rot_vorakd.__name__,
    rot_kdvora.__name__,
]


def _main(argv=None):
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description=__doc__.strip().splitlines()[0],
    )
    parser.add_argument(
        '--rotation', choices=__all__, default=__all__[0],
        help='Rotation keyboard layout/direction (default: %(default)s)',
    )
    args = parser.parse_args(argv)

    rotation_fn = globals()[args.rotation]

    for line in sys.stdin:
        sys.stdout.write(rotation_fn(line))
        sys.stdout.flush()

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(_main())
