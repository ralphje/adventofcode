"""This file holds the solutions for Advent of Code 2023 day 20: Pulse Propagation
https://adventofcode.com/2023/day/20
"""

from __future__ import annotations

import itertools
import math
import re
from collections.abc import Iterator
from typing import cast


class Signal:
    """Definition of the two signal singletons. This is a bit nicer than using booleans, though
    that would work too.
    """

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name


Low = Signal("Low")
High = Signal("High")


class Module:
    """Implementation of a module. The generic module doesn't do anything with the signals it
    receives.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.inputs: set[Module] = set()
        self.outputs: set[Module] = set()

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}: {self.name} -> {','.join(i.name for i in self.outputs)}>"
        )

    def add_input(self, sender: Module) -> None:
        """Hook function to add inputs to this module. Used by Conjunction so it knows all its
        inputs in advance. Default implementation simply adds it to the set of inputs.
        """
        self.inputs.add(sender)

    def add_output(self, receiver: Module) -> None:
        """Add an output to this module."""
        self.outputs.add(receiver)
        receiver.add_input(self)

    def receive(self, sender: Module, signal: Signal) -> Signal | None:
        """Receive the signal and decide what to do with it. Return None if nothing, return a
        signal if we want to send this signal
        """
        return None

    def handle(self, sender: Module, signal: Signal) -> Iterator[tuple[Module, Module, Signal]]:
        """Handle receiving the signal by the given module. Returns any new signals it needs to
        send, with (sender, receiver, signal) tuples.
        """

        next_signal = self.receive(sender, signal)
        if next_signal is None:
            return

        for output in self.outputs:
            yield self, output, next_signal


class FlipFlop(Module):
    """Flip-flop modules (prefix %) are either on or off; they are initially off. If a flip-flop
    module receives a high pulse, it is ignored and nothing happens. However, if a flip-flop module
    receives a low pulse, it flips between on and off. If it was off, it turns on and sends a high
    pulse. If it was on, it turns off and sends a low pulse.
    """

    state: bool = False

    def receive(self, sender: Module, signal: Signal) -> Signal | None:
        if signal is Low:
            # However, if a flip-flop module receives a low pulse, it flips between on and off. If
            # it was off, it turns on and sends a high pulse. If it was on, it turns off and sends
            # a low pulse.
            self.state = not self.state
            return High if self.state else Low
        # If a flip-flop module receives a high pulse, it is ignored and nothing happens.
        return None


class Conjunction(Module):
    """Conjunction modules (prefix &) remember the type of the most recent pulse received from each
    of their connected input modules; they initially default to remembering a low pulse for each
    input. When a pulse is received, the conjunction module first updates its memory for that input.
    Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a
    high pulse.
    """

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.memory: dict[Module, Signal] = {}

    def add_input(self, sender: Module) -> None:
        super().add_input(sender)
        self.memory[sender] = Low

    def receive(self, sender: Module, signal: Signal) -> Signal | None:
        # When a pulse is received, the conjunction module first updates its memory for that input.
        self.memory[sender] = signal

        # Then, if it remembers high pulses for all inputs, it sends a low pulse
        if all(v is High for v in self.memory.values()):
            return Low

        # otherwise, it sends a high pulse.
        return High


class Broadcaster(Module):
    """There is a single broadcast module (named broadcaster). When it receives a pulse, it sends
    the same pulse to all of its destination modules.
    """

    def receive(self, sender: Module, signal: Signal) -> Signal | None:
        return signal


class Button(Module):
    """Here at Desert Machine Headquarters, there is a module with a single button on it called,
    aptly, the button module. When you push the button, a single low pulse is sent directly to the
    broadcaster module.
    """

    def receive(self, sender: Module, signal: Signal) -> Signal | None:
        return Low

    def press(self) -> Iterator[tuple[Module, Module, Signal]]:
        """Simplified method to allow pressing the button."""
        yield from self.handle(self, Low)


DEFINITION_RE = re.compile(r"([%&]?)([a-z]+) -> (.*)")


def build_modules(definitions: list[str]) -> dict[str, Module]:
    """Build all modules and return a dict of name, module instances."""
    modules: dict[str, Module] = {}
    destinations_todo: dict[str, list[str]] = {}

    # Iterate over all definitions, and create all Modules
    for definition in definitions:
        type, name, destinations = DEFINITION_RE.findall(definition)[0]
        destinations_todo[name] = destinations.split(", ")
        if type == "%":
            # Flip-flop modules (prefix %)
            modules[name] = FlipFlop(name)
        elif type == "&":
            # Conjunction modules (prefix &)
            modules[name] = Conjunction(name)
        elif name == "broadcaster":
            # a single broadcast module (named broadcaster)
            modules[name] = Broadcaster(name)
        else:
            raise AssertionError(f"unknown definition: {type!r} {name!r}")

    # Add the outputs to each module
    for name, destinations in destinations_todo.items():
        module = modules[name]
        for destination in destinations:
            # it can happen that an output is not defined, e.g. for the output module in the second
            # example or the rx module.
            if destination not in modules:
                modules[destination] = Module(destination)
            module.add_output(modules[destination])

    # Add the button to the schema
    modules["button"] = Button("button")
    modules["button"].add_output(modules["broadcaster"])

    return modules


def handle_signals(button: Button) -> Iterator[tuple[Module, Module, Signal]]:
    """Press the button, and handle all signals that result in this button press. This method
    will yield all signals seen in the process, as (sender, receiver, signal) tuples, before they
    are processed.

    Debug using print(f"{sender.name} -{signal}-> {receiver.name}")
    """

    # Pulses are always processed in the order they are sent. So, if a pulse is sent to modules
    # a, b, and c, and then module a processes its pulse and sends more pulses, the pulses sent
    # to modules b and c would have to be handled first.
    signals: list[tuple[Module, Module, Signal]] = list(button.press())

    # Handle all signals in order
    while signals:
        sender, receiver, signal = signals.pop(0)

        # Yield this signal as it is being processed (before it is being processed)
        yield sender, receiver, signal

        # Process and add signals
        signals.extend(receiver.handle(sender, signal))


def part_1(lines: list[str]) -> int:
    """Solution for Advent of Code 2023 day 20 part 1"""
    button = cast(Button, build_modules(lines)["button"])

    # What do you get if you multiply the total number of low pulses sent by the total number of
    # high pulses sent?
    counts = {Low: 0, High: 0}

    # Repeat pushing the button 1000 times. Never push the button if modules are still processing
    # pulses.
    for _ in range(1000):
        # Iterate over all signals seen in the process
        for _, _, signal in handle_signals(button):
            counts[signal] += 1

    return math.prod(counts.values())


def part_2(lines: list[str]) -> int:
    """Solution for Advent of Code 2023 day 20 part 2"""
    modules = build_modules(lines)
    button = cast(Button, modules["button"])

    # This solution is input-specific and depends on the fact that the input is crafted as follows:
    # * rx has a single input, say rx_input
    assert len(modules["rx"].inputs) == 1
    rx_input = next(iter(modules["rx"].inputs))

    # * rx_input is a conjunction with several inputs, each containing a loop
    assert isinstance(rx_input, Conjunction)

    # * after rx_input receives a high input from a certain loop, that loop resets entirely as if
    #   there haven't been any button presses
    # * when rx_input receives a high input at any time from a loop, it is not reset before
    #   any other high signal from another loop is sent to rx_input.
    #
    # There are probably more assumptions being made here, but this produces a valid solution for
    # my input.
    #
    # I don't like solutions such as these that highly depend on a certain input structure.

    # Prepare button press counts for every rx_input's input, i.e. how many times a button press is
    # required for that input to emit a high signal to rx_input.
    button_counts = {mod: 0 for mod in rx_input.inputs}

    for i in itertools.count(start=1):
        # Iterate over all signals, and record first time we see any High signal being emitted to
        # rx_input.
        for sender, receiver, signal in handle_signals(button):
            if receiver == rx_input and signal == High and not button_counts[sender]:
                button_counts[sender] = i
        # Stop looping once we've found all button press counts
        if all(button_counts.values()):
            break

    return math.lcm(*button_counts.values())
