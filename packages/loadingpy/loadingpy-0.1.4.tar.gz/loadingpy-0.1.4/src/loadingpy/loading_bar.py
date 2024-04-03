from typing import Any, Iterable, Optional

from loadingpy.basic_bar import BarConfig

from .alias import aliases
from .colored_bar import ColoredBar


@aliases("pybar")
class PyBar(ColoredBar):
    def __init__(
        self,
        iterable: Iterable,
        monitoring: Optional[Any] = None,
        naming: Optional[Any] = None,
        total_steps: int = -1,
        base_str: str = "loop",
        interpolation: int = 1,
        color: str = "green",
    ) -> None:
        """
        creates a progress bar for a python iterable.

        Args:
            iterable: python object that can be iterated over
            monitoring [OPTIONAL]: a python object (or list of python objects) that will be printed after each iteration
                using the following format f'{monitoring}'. IF they are updated during the loop, make sure to
                update inplace, in order to see the changes
            naming [OPTIONAL]: if you want to add a descritpion prefix to the monitoring variables
            total_steps [OPTIONAL]: number of iterations to perform (if you set it to a lower value than the length of the iterable,
                then the process will stop after the given total_steps)
            base_str [OPTIONAL]: prefix description of the loop we are iterating over
            interpolation [int]: interpolation polynomial degree for eta
            color [OPTIONAL]: which color to use for the loading bar
        """
        super().__init__(iterable, total_steps, base_str, interpolation, color)
        self.monitoring = monitoring
        self.naming = naming
        self.description: Optional[str] = None
        if isinstance(self.monitoring, (list, tuple)) and isinstance(self.naming, (list, tuple)):
            assert len(self.naming) == len(self.monitoring)

        self.handle_monitoring()

    def set_description(self, description: Optional[str] = None) -> None:
        self.description = description

    def handle_naming(self) -> int:
        if self.naming is None:
            return 0
        if isinstance(self.naming, (list, tuple)):
            return sum([len(name) + 1 for name in self.naming])
        else:
            return len(self.naming) + 1

    def handle_monitoring(self) -> None:
        if self.description is not None:
            self.suffix_length = 17 + 3 + len(self.description)
        elif self.monitoring is not None:
            if isinstance(self.monitoring, (list, tuple)):
                self.suffix_length = 17 + 2 + sum([len(f"{e}") + 1 for e in self.monitoring]) + self.handle_naming()
            else:
                self.suffix_length = 17 + 3 + len(f"{self.monitoring}") + self.handle_naming()

    def build_monitoring_str(self) -> str:
        if not isinstance(self.monitoring, (list, tuple)):
            if self.naming is not None:
                return f"{self.naming}:{self.monitoring}"
            else:
                return f"{self.monitoring}"
        output = ""
        if self.naming is not None:
            for e, n in zip(self.monitoring, self.naming):
                output += f"{n}:{e}" + " "
        else:
            for e in self.monitoring:
                output += f"{e}" + " "
        output = output[:-1]
        return output

    def build_suffix(self, progression_complete: bool) -> str:
        suffix = super().build_suffix(progression_complete=progression_complete)
        if self.description is not None:
            suffix = f"{suffix} | {self.description}"
        elif self.monitoring is not None:
            suffix = f"{suffix} | {self.build_monitoring_str()}"
        self.handle_monitoring()
        return suffix

    def __next__(self, *args: Any, **kwds: Any) -> Any:
        progression_complete = self.current_progression >= self.total_steps
        base_string = self.build_prefix()
        suffix = self.build_suffix(progression_complete=progression_complete)
        self.update_bar_size()
        bar = self.build_bar(
            progression_complete=progression_complete,
            progress_bar_size=self.progress_bar_size,
            current_progression=self.current_progression,
            total_steps=self.total_steps,
        )
        if not BarConfig["disable loading bar"]:
            print(
                f"\r{base_string} {bar} {suffix}",
                end="" if not progression_complete else "\n",
            )
        else:
            if self.current_progression == 0:
                print(f"{base_string}: started ...")
            elif self.total_steps // 2 == self.current_progression:
                print(f"{base_string}: Half way there ! Still {self.get_remaining_time()}s to finish...")
            elif self.total_steps - 1 == self.current_progression:
                print(f"{base_string}: Finished in {self.runtime()}s ...")
        if progression_complete:
            raise StopIteration
        output = next(self.iterable)
        self.current_progression += 1
        return output
