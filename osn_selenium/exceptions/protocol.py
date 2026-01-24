from osn_selenium.exceptions.base import OSNSeleniumError
from typing import (
	Any,
	Iterable,
	Protocol,
	Type,
	Union,
	get_origin
)


__all__ = ["ProtocolComplianceError", "ProtocolError"]


class ProtocolError(OSNSeleniumError):
	"""
	Base class for errors related to Protocol contract violations.
	"""
	
	pass


class ProtocolComplianceError(ProtocolError):
	"""
	Error raised when an object fails to implement the required protocol members.

	Attributes:
		instance (Any): The object instance that failed the check.
		instance_name (str): The name of the instance class.
		expected_list (list): A list of protocols the instance was checked against.
	"""
	
	def __init__(self, instance: Any, expected_protocols: Union[Type, Iterable[Type]]) -> None:
		"""
		Initializes ProtocolComplianceError.

		Args:
			instance (Any): The object instance that failed the check.
			expected_protocols (Union[Type, Iterable[Type]]): The protocol or protocols expected.
		"""
		
		self.instance = instance
		
		self.instance_name = type(instance).__name__
		
		if isinstance(expected_protocols, type) or get_origin(expected_protocols) is not None:
			self.expected_list = [expected_protocols]
		else:
			self.expected_list = list(expected_protocols)
		
		super().__init__(self._generate_report())
	
	def _generate_report(self) -> str:
		"""
		Generates a detailed report of missing members for the protocols.

		Returns:
			str: A formatted string containing missing members and compliance status.
		"""
		
		report = [f"Object '{self.instance_name}' failed protocol compliance check."]
		
		for proto in self.expected_list:
			proto_name = getattr(proto, "__name__", str(proto))
			needed_attrs = getattr(proto, "__protocol_attrs__", set())
		
			if not needed_attrs:
				report.append(f"\t- Protocol '{proto_name}': No checkable attributes found.")
				continue
		
			missing = [attr for attr in needed_attrs if not hasattr(self.instance, attr)]
		
			if missing:
				report.append(
						f"\t- Protocol '{proto_name}' requires missing members: {', '.join(missing)}"
				)
			else:
				report.append(
						f"\t- Protocol '{proto_name}': Members present, but contract check failed."
				)
		
		report.append(
				f"Please ensure the object implements all required properties and methods defined in the Protocol."
		)
		
		return "\n".join(report)
