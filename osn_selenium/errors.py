from typing import (
	Any,
	Iterable,
	Type,
	Union,
	get_origin
)


__all__ = ["PlatformNotSupportedError", "ProtocolComplianceError"]


class ProtocolComplianceError(Exception):
	def __init__(self, instance: Any, expected_protocols: Union[Type, Iterable[Type]]):
		self.instance = instance
		
		self.instance_name = type(instance).__name__
		
		if isinstance(expected_protocols, type) or get_origin(expected_protocols) is not None:
			self.expected_list = [expected_protocols]
		else:
			self.expected_list = list(expected_protocols)
		
		super().__init__(self._generate_report())
	
	def _generate_report(self) -> str:
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


class PlatformNotSupportedError(Exception):
	"""
	Custom exception raised when the current platform is not supported.

	This exception is intended to be raised when the script or application is run on a platform that is not explicitly supported by the program logic.
	"""
	
	def __init__(self, platform: str):
		"""
		Initializes a new instance of `PlatformNotSupportedError`.

		Args:
		   platform (str): The name of the unsupported operating system.
		"""
		
		super().__init__(
				f"Platform not supported: {platform}. Currently supported: Windows, Linux."
		)
