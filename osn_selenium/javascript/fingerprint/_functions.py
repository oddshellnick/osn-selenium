__all__ = ["add_code_level", "reduce_code_level"]


def reduce_code_level(code: str, num: int = 1) -> str:
	"""
	Reduces the indentation level of a multi-line string by removing leading tabs.

	Args:
		code (str): The code block to un-indent.
		num (int): The number of tabs to remove. Defaults to 1.

	Returns:
		str: The un-indented code.
	"""
	
	reducing = "\t" * num
	
	return "\n".join([line.removeprefix(reducing) for line in code.splitlines()])


def add_code_level(code: str, num: int = 1) -> str:
	"""
	Increases the indentation level of a multi-line string by adding leading tabs.

	Args:
		code (str): The code block to indent.
		num (int): The number of tabs to add. Defaults to 1.

	Returns:
		str: The indented code.
	"""
	
	adding = "\t" * num
	
	return adding + f"\n{adding}".join(code.splitlines())
