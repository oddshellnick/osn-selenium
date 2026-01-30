from osn_selenium._base_models import DictModel


__all__ = ["ExecutablesTableRow"]


class ExecutablesTableRow(DictModel):
	"""
	Represents a row in the executables table containing process information.

	Attributes:
		executable (str): The name of the executable file.
		address (str): The network address (IP:Port) the process is listening on.
		pid (int): The process identifier.
	"""
	
	executable: str
	address: str
	pid: int
