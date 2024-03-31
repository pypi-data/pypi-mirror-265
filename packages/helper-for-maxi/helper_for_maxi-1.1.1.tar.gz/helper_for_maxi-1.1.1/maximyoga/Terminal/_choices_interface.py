from os import system
from typing import Tuple
from string import digits
from random import choices
from pygetwindow import getActiveWindowTitle
from pynput.keyboard import Listener, Key, KeyCode
from .color import foreground as fgcolor, background as bgcolor, RESET

clear = lambda: system("cls")

class ChoiceInterface:
	r"""Creates a Terminal Interface with choices

	When a created instance is called, starts a Terminal Interface where the User can choose from given options and the chosen option is returned as an index
	"""

	def __init__(
		self, *,
		textColor: fgcolor = fgcolor.WHITE,
		highlightTextColor: fgcolor = fgcolor.BLACK,
		highlightColor: bgcolor = bgcolor.WHITE,
		confirmKey: list[Key | KeyCode] | Key | KeyCode = [Key.enter, Key.right],
		cancelKey: list[Key | KeyCode] | Key | KeyCode = Key.esc,
		choicesSurround: str = "",
		addArrowToSelected: bool = False
	) -> None:
		r"""Creates an Instance of Choice Interface

		To start the interface, call the created instance

		Parameters
		----------
		textColor: :class:`mTc.foreground` (optional)
			The color of the Text shown in the Interface
			DEFAULT = :param:`mTc.foreground.WHITE`
		
		highlightTextColor: :class:`mTc.foreground` (optional)
			The color of text of the selected item
			DEFAULT = :param:`mTc.foreground.BLACK`

		highlightColor: :class:`mTc.background` (optional)
			The background color of the text of the selected item
			DEFAULT = :param:`mTc.background.WHITE`
		
		confirmKey: :class:`pk.Key` | :class:`pk.KeyCode` | :class:`list[:class:`pk.Key` | :class:`pk.KeyCode`]` (optional)
			The key(s) that need(s) to be pressed to confirm a choice
			DEFAULT = :param:`[pk.Key.enter, pk.Key.right]`
		
		cancelKey: :class:`pk.Key` | :class:`pk.KeyCode` | :class:`list[:class:`pk.Key` | :class:`pk.KeyCode`]` (optional)
			The key(s) that need(s) to be pressed to cancel the Interface, in which case -1 is returned
			DEFAULT = :param:`pk.Key.esc`
		
		choicesSurround: :class:`str`
			What the choices should be surrounden by.
			The :param:`choicesSurround` string itself will be outside of the highlighted area of the selected choice.
			When set, :param:`minimumHighlightLength` parameter in :meth:`__call__` will be forced to -1
			DEFAULT = :param:`""`
		
		addArrowToSelected: :class:`bool`
			If there should be a " >" added to the end of the selected choice.
			When set, :param:`minimumHighlightLength` parameter in :meth:`__call__` will be forced to -1
			DEFAULT = :param:`False`

		Abbreviations
		-------------
		mTc = maximyoga.Terminal.color

		pk = pynput.keyboard
		"""
		cfKey = confirmKey if isinstance(confirmKey, list) else [confirmKey]
		ccKey = cancelKey if isinstance(cancelKey, list) else [cancelKey]
		if set(cfKey) & set(ccKey):
			raise ValueError("values in confirmKey and cancelKey may not overlap!")
		self.confirmKeys = cfKey
		self.cancelKeys = ccKey
		self.textColor = textColor
		self.hlTextColor = highlightTextColor
		self.hlColor = highlightColor
		self.choicesSurround = choicesSurround
		self.addArrowToSelected = addArrowToSelected
		self.terminalWindowTitle = "Choice Interface {"+"".join(choices(digits, k=10))+"}"
		self.lastKeyPressed = None
	
	def __call__(self, 
			choices: list[str],
			prefix: str = "", 
			suffix: str = "", 
			selected: int = 0, 
			minimumHighlightLength: int = -1, 
			terminalTitleBefore: str = "Terminal"
		) -> Tuple[int, str]:
		r"""Starts the interface in the Terminal

		draws the prefix, choices and suffix to the terminal and handles input to make an Interface

		Parameters
		----------
		lines: :class:`list[:class:`str`]`
			The list of choices to use
		
		prefix: :class:`str` (optional)
			What should be printed above the choices and not included in the selectable items
			DEFAULT = :param:`""`
		
		suffix: :class:`str` (optional)
			What should be printed below the choices and not included in the selectable items
			DEFAULT = :param:`""`

		selected: :class:`int` (optional)
			Which choice should be selected when the Interface is started
			DEFAULT = :param:`0`

		minimumHighlightLength: :class:`int` (optional)
			How long the highlight should at least be
				will be :param:`len(:param:`choices[:param:`selected`]`)` if :param:`choices[:param:`selected`]` is longer than :param:`minimumHighightLength`
			negative values will mean :param:`max(:param:`len(:param:`choices`)`)` + :param:`abs(:param:`minimumHighlightLength`)`
			DEFAULT = :param:`-1`
		
		terminalTitleBefore: :class:`str` (optional)
			What the terminal title should be set to after the interface is done
			DEFAULT = :param:`"Terminal"`
		"""
		system(f"TITLE {self.terminalWindowTitle}")

		if len(choices) <= 1 or (not (isinstance(choices, list) and all([isinstance(x, str) for x in choices]))):
			raise ValueError("Parameter 'lines' must be of length >= 2 and of type list[str]")
		if 0 > selected >= len(choices):
			raise ValueError("Parameter 'selected' must be index of line in 'lines' and may therefore not be bigger than the "
							 "biggest index of 'lines' or smaller than 0")
		
		hlLen = minimumHighlightLength if minimumHighlightLength >= 0 and not(any([self.choicesSurround, self.addArrowToSelected]))\
			 							else max([len(line) for line in choices]) + abs(minimumHighlightLength)
		
		while True:
			clear()
			if prefix:
				print(self.textColor+prefix+RESET)
			
			for i, line in enumerate(choices):
				if i == selected:
					if not any([self.choicesSurround, self.addArrowToSelected]):
						_out = f"{self.hlColor+self.hlTextColor}{line:<{hlLen}}{RESET}"
					elif self.addArrowToSelected:
						_out = f"{self.hlColor+self.hlTextColor}{line+" >":<{hlLen+2}}{RESET}"
				else:
					_out = self.textColor+line+RESET
				if self.choicesSurround:
					_out = self.choicesSurround+_out+self.choicesSurround
				print(_out)

			if suffix:
				print(self.textColor+prefix+RESET)
			
			key = self._waitForKey()
			
			if key == Key.down and selected != len(choices)-1:
				selected += 1
			elif key == Key.up and selected != 0:
				selected -= 1
			elif key in self.confirmKeys:
				if key == Key.enter: input()
				system(f"TITLE {terminalTitleBefore}")
				return selected
			elif key in self.cancelKeys:
				if key == Key.enter: input()
				system(f"TITLE {terminalTitleBefore}")
				return -1
			elif key in [Key.down, Key.up]:
				pass
			else:
				raise Exception("Somehow, Somewhere, Something went wrong :/")
		
	def _waitForKey(self) -> str:
		lst = Listener(on_press=lambda key: self._onKeyPress(key, lst))
		lst.start()
		lst.join()
		return self.__lastKeyPressed

	def _onKeyPress(self, key: Key | KeyCode, lst: Listener) -> None:
		if getActiveWindowTitle() != self.terminalWindowTitle:
			return
		self.__lastKeyPressed = key
		if self.__lastKeyPressed in self.confirmKeys+self.cancelKeys+[Key.up, Key.down]:
			lst.stop()