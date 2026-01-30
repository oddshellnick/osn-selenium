import re
import sys
import pathlib
import importlib.util
import urllib.request
from types import ModuleType
from datetime import datetime, timedelta
from importlib.abc import MetaPathFinder
from importlib.machinery import ModuleSpec
from osn_selenium._typehints import PATH_TYPEHINT
from typing import (
	Dict,
	Mapping,
	Optional,
	Sequence,
	Tuple,
	Union
)


__all__ = ["check_cdp_version_exists_on_github", "install_cdp_hook"]

_SELENIUM_CDP_PATTERN = re.compile(r"selenium\.webdriver\.common\.devtools\.v(\d+)(.*)")
_INTERNAL_CDP_PATTERN = re.compile(r"osn_selenium_cdp_v(\d+)(?!\.legacy)(.*)")

_GITHUB_VERSIONS_CACHE: Dict[str, Tuple[bool, datetime]] = {}
_CDP_PACKAGE_ERROR = None


def _build_cdp_package_error(version: int) -> Exception:
	"""
	Creates an instance of the CDPPackageError exception.

	Args:
		version (int): The version of the CDP package.

	Returns:
		Exception: An instance of the CDPPackageError.
	"""
	
	global _CDP_PACKAGE_ERROR
	
	if _CDP_PACKAGE_ERROR is None:
		from osn_selenium.exceptions.dependencies import CDPPackageError
		_CDP_PACKAGE_ERROR = CDPPackageError
	
	return _CDP_PACKAGE_ERROR(version=version)


def _get_external_spec(fullname: str, root_path: pathlib.Path, submodule_part: str) -> Optional[ModuleSpec]:
	"""
	Creates a module spec for an external path.

	Args:
		fullname (str): The full name of the module.
		root_path (pathlib.Path): The root directory where the module is located.
		submodule_part (str): The part of the name representing submodules.

	Returns:
		Optional[ModuleSpec]: The module spec if found, otherwise None.
	"""
	
	if not submodule_part:
		target_path = root_path / "__init__.py"
		is_package = True
	else:
		rel_path = submodule_part.lstrip(".").replace(".", "/")
		target_path = root_path / f"{rel_path}.py"
	
		if not target_path.exists():
			target_path = root_path / rel_path / "__init__.py"
			is_package = True
		else:
			is_package = False
	
	if target_path.exists():
		spec = importlib.util.spec_from_file_location(
				name=fullname,
				location=str(target_path),
				submodule_search_locations=[str(root_path)]
				if is_package
				else None
		)
	
		return spec
	
	return None


class _CdpMetaPathFinder(MetaPathFinder):
	"""
	A custom meta path finder to redirect Selenium CDP imports.
	"""
	
	def __init__(
			self,
			cdp_paths: Optional[Mapping[int, PATH_TYPEHINT]] = None,
			ignore_package_missing: bool = True
	) -> None:
		"""
		Initializes the finder with user-defined CDP paths.

		Args:
			cdp_paths (Optional[Mapping[int, PATH_TYPEHINT]]): Mapping of versions to paths.
			ignore_package_missing (bool): Whether to ignore missing package errors.
		"""
		
		self._user_cdp_paths = {k: pathlib.Path(v).resolve() for k, v in (cdp_paths or {}).items()}
		
		self._ignore_package_missing = ignore_package_missing
	
	def _find_spec_bypassing_self(self, fullname: str, path: Optional[Sequence[str]]) -> Optional[ModuleSpec]:
		"""
		Attempts to find the module specification using other finders in sys.meta_path.

		Args:
			fullname (str): The full name of the module.
			path (Optional[Sequence[str]]): The search path for the module.

		Returns:
			Optional[ModuleSpec]: The module spec if found, otherwise None.
		"""
		
		for finder in sys.meta_path:
			if finder is self:
				continue
		
			try:
				if hasattr(finder, "find_spec"):
					spec = finder.find_spec(fullname, path)
		
					if spec:
						return spec
			except (Exception,):
				continue
		
		return None
	
	def find_spec(
			self,
			fullname: str,
			path: Optional[Sequence[str]],
			target: Optional[ModuleType] = None,
	) -> Optional[ModuleSpec]:
		"""
		Finds the specification for the requested module if it matches the CDP pattern.

		Args:
			fullname (str): The full name of the module to find.
			path (Optional[Sequence[str]]): The search path for the module.
			target (Optional[ModuleType]): The module object if it is being reloaded.

		Returns:
			Optional[ModuleSpec]: The module spec if found, otherwise None.
		"""
		
		selenium_match = _SELENIUM_CDP_PATTERN.match(fullname)
		internal_match = _INTERNAL_CDP_PATTERN.match(fullname)
		
		if not (selenium_match or internal_match):
			return None
		
		match = selenium_match or internal_match
		version_part = int(match.group(1))
		submodule_part = match.group(2)
		
		user_cdp_path = self._user_cdp_paths.get(version_part, None)
		if user_cdp_path is not None:
			root = (user_cdp_path / "legacy") if selenium_match else user_cdp_path
			return _get_external_spec(fullname=fullname, root_path=root, submodule_part=submodule_part)
		
		spec = None
		
		if selenium_match:
			target_name = f"osn_selenium_cdp_v{version_part}.legacy{submodule_part}"
			spec = importlib.util.find_spec(target_name, path)
		
		if internal_match:
			target_name = f"osn_selenium_cdp_v{version_part}{submodule_part}"
			spec = self._find_spec_bypassing_self(target_name, path)
		
		try:
			if spec:
				return importlib.util.spec_from_file_location(
						name=fullname,
						location=spec.origin,
						submodule_search_locations=spec.submodule_search_locations,
				)
		except ModuleNotFoundError:
			if self._ignore_package_missing:
				return None
		
			raise _build_cdp_package_error(version=version_part)
		
		return None


def install_cdp_hook(
		cdp_paths: Optional[Mapping[int, PATH_TYPEHINT]] = None,
		ignore_package_missing: bool = True,
) -> None:
	"""
	Installs the CDP meta path finder into sys.meta_path.

	Args:
		cdp_paths (Optional[Mapping[int, PATH_TYPEHINT]]): Mapping of versions to custom local paths.
		ignore_package_missing (bool): Whether to ignore missing package errors.
	"""
	
	for finder in sys.meta_path:
		if isinstance(finder, _CdpMetaPathFinder):
			finder._user_cdp_paths.update({k: pathlib.Path(v).resolve() for k, v in (cdp_paths or {}).items()})
			finder._ignore_package_missing = ignore_package_missing
	
			return
	
	sys.meta_path.insert(
			0,
			_CdpMetaPathFinder(cdp_paths=cdp_paths, ignore_package_missing=ignore_package_missing)
	)


def check_cdp_version_exists_on_github(version: Union[int, str]) -> bool:
	"""
	Checks if a specific CDP version exists in the remote repository.

	Args:
		version (Union[int, str]): The version of package.

	Returns:
		bool: True if the version exists, False otherwise.
	"""
	
	branch_name = version if isinstance(version, str) else f"v{version}"
	
	cached_answer = _GITHUB_VERSIONS_CACHE.get(branch_name, None)
	if cached_answer and datetime.now() - cached_answer[1] < timedelta(hours=12):
		return cached_answer[0]
	
	repo_url = f"https://api.github.com/repos/oddshellnick/osn-selenium-cdp/branches/{branch_name}"
	
	try:
		request = urllib.request.Request(url=repo_url, headers={"User-Agent": "osn-selenium"})
		request.get_method = lambda: "HEAD"
	
		with urllib.request.urlopen(url=request, timeout=5.0) as response:
			existing = response.status == 200
			_GITHUB_VERSIONS_CACHE[branch_name] = (existing, datetime.now())
	
			return existing
	except (Exception,):
		_GITHUB_VERSIONS_CACHE[branch_name] = (False, datetime.now())
		return False
