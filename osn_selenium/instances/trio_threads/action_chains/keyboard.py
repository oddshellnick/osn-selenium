from typing import (
	Optional,
	TYPE_CHECKING
)
from osn_selenium.instances.convert import get_legacy_instance
from osn_selenium.instances._typehints import WEB_ELEMENT_TYPEHINT
from osn_selenium.instances.trio_threads.action_chains.base import BaseMixin
from osn_selenium.instances.unified.action_chains.keyboard import UnifiedKeyboardMixin
from osn_selenium.abstract.instances.action_chains.keyboard import (
	AbstractKeyboardMixin
)


__all__ = ["KeyboardMixin"]

if TYPE_CHECKING:
	from osn_selenium.instances.trio_threads.action_chains import ActionChains


class KeyboardMixin(BaseMixin, UnifiedKeyboardMixin, AbstractKeyboardMixin):
	"""
	Mixin class providing keyboard interaction methods.
	"""
	
	async def key_down(self, value: str, element: Optional[WEB_ELEMENT_TYPEHINT] = None) -> "ActionChains":
		action_chains = await self.sync_to_trio(sync_function=self._key_down_impl)(value=value, element=get_legacy_instance(instance=element))
		
		return self.from_legacy(
				legacy_object=action_chains,
				execute_js_script_function=self._execute_js_script_function,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	async def key_up(self, value: str, element: Optional[WEB_ELEMENT_TYPEHINT] = None) -> "ActionChains":
		action_chains = await self.sync_to_trio(sync_function=self._key_up_impl)(value=value, element=get_legacy_instance(instance=element))
		
		return self.from_legacy(
				legacy_object=action_chains,
				execute_js_script_function=self._execute_js_script_function,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	async def send_keys(self, *keys_to_send: str) -> "ActionChains":
		action_chains = await self.sync_to_trio(sync_function=self._send_keys_impl)(*keys_to_send)
		
		return self.from_legacy(
				legacy_object=action_chains,
				execute_js_script_function=self._execute_js_script_function,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
	
	async def send_keys_to_element(self, element: WEB_ELEMENT_TYPEHINT, *keys_to_send: str) -> "ActionChains":
		action_chains = await self.sync_to_trio(sync_function=self._send_keys_to_element_impl)(get_legacy_instance(instance=element), *keys_to_send)
		
		return self.from_legacy(
				legacy_object=action_chains,
				execute_js_script_function=self._execute_js_script_function,
				lock=self._lock,
				limiter=self._capacity_limiter,
		)
