"""Elegant debuging tool"""
if __name__ == '__main__':
    print('Nezu is elegant debuging module')
else:
    from inspect import currentframe
    from typing import Any, Self

    class Nezu:
        """Nezu object"""

        def __init__(self, id: str):
            from nezu._os_env import os_bool, os_int

            self._id = id
            self.seek = os_int(id, 'SEEK')
            self.color = os_bool(id, 'COLOR')
            self._locked = os_bool(id, 'LOCK')

            self.hard = self.__call__

        def __call__(
            self, seek: int = 0, color: bool = False, lock: bool = False
        ):
            """
            Hard coded configuration.

            Parameters
            ------------
                seek: int = 0
                    How deep to seek for hidden calls of `dbg` function?
                    dbg function is called with `hide` parameter (0 by default).
                    If `seek => hide` message will be displayed.
                color: bool = False
                    Determine if output is colored.

            """
            if not self._locked:
                self.seek = seek
                self.color = color
                self._locked = lock
            else:
                raise RuntimeError(
                    f'This Nezu object #{self._id} is locked and cannot be changed.'
                )

        def __iter__(self):
            return iter(
                [
                    ('id', self._id),
                    ('seek', self.seek),
                    ('color', self.color),
                ]
            )

        def json(self, path: str = 'nezu.json', **kwargs):
            """
            Initialaze nezu via json file
            """
            if not self._locked:
                import json

                with open(path, 'r', **kwargs) as file:
                    all_data = json.load(file)
                nezu_data = all_data.get(self._id, {})
                self.seek = nezu_data.get('seek', 0)
                self.color = nezu_data.get('color', False)

            else:
                raise RuntimeError(
                    f'This Nezu object #{self._id} is locked and cannot be changed.'
                )

        def say(self, var, hide: int = 1):
            if self.seek >= hide:
                FRAME = currentframe().f_back
                LINE = FRAME.f_lineno
                prfx = f'@{LINE}'.rjust(7) + ' '
                # palete = {
                #     'default': '\033[0m',
                #     'red': '\033[91m',
                #     'green': '\033[92m',
                #     'yellow': '\033[93m',
                #     'blue': '\033[94m',
                #     'purple': '\033[95m',
                #     'cyan': '\033[96m',
                # }
                print(
                    f'{prfx}\033[92m{var}\033[0m'
                    if self.color
                    else f'{prfx}{var}'
                )

        def dbg(self, *keys: str, note: str = None, hide: int = 1) -> None:
            """
            Parameters
            ------------

            - `*keys:str`

                Names of varables to inspect

            - `note:str=None`

                Optional comment. Ignored if equal to None.

            - `hide:int=1`

                How deep do you want to hide this message.
                If `hide <= 0`, this message will be displayed by default.


            Description
            ------------
            Function `dbg` displays following data in that order for each inspected varable:

            - number of line it was called at

            - scope of inspected variable

            - name of inspected variable

            - type of inspected variable

            - value of inspected variable
            """

            if self.seek >= hide:
                from nezu._parse import get_output

                FRAME = currentframe().f_back
                LINE = FRAME.f_lineno
                LOCAL = FRAME.f_locals
                GLOBAL = FRAME.f_globals
                BINS = FRAME.f_builtins

                if len(keys) < 2:
                    prfx = f'@{LINE}'.rjust(7) + ' '
                    desc = '  |  '.join(
                        [
                            get_output(LOCAL, GLOBAL, BINS, key, self.color)
                            for key in keys
                        ]
                    )
                    sufx = f'  |  << {note} >>' if note != None else ''
                else:
                    tab = f'\n{" "*8}'
                    prfx = f'@{LINE}'.rjust(7) + ' ' + '-' * 70 + tab
                    desc = tab.join(
                        [
                            get_output(LOCAL, GLOBAL, BINS, key, self.color)
                            for key in keys
                        ]
                    )
                    sufx = f'{tab}<< {note} >>' if note != None else ''
                    sufx += f'{tab}{"-"*70}'

                print(f'{prfx}{desc}{sufx}')

    def real_nezu():
        """
        Creates default instance of Nezu.
        # DO NOT USE THIS FUNCTION IN YOUR PROJECT!
        ---
        This function is only to be used in internal tests, so each test has unique Nezu instance identical to deafult Nezu instance.

        If you want multiple nezu instances, create them using constructor function `Nezu(id='my_nezu')`
        """
        defaults = {'id': 'nezu'}
        return Nezu(**defaults)

    ず = nezu = real_nezu()
    虫 = dbg = nezu.dbg
    話 = say = nezu.say
