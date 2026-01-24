import trio
from osn_selenium.dev_tools.models import FingerprintData
from osn_selenium.exceptions.devtools import CDPEndExceptions
from osn_selenium.dev_tools.target.logging import LoggingMixin
from osn_selenium.dev_tools._functions import execute_cdp_command


__all__ = ["FingerprintMixin"]


class FingerprintMixin(LoggingMixin):
	"""
	Mixin for detecting and logging fingerprinting attempts in the browser.
	"""
	
	async def _run_fingerprint_detect_listener(self, ready_event: trio.Event):
		"""
		Runs the listener for fingerprint detection events from the browser.

		Args:
			ready_event (trio.Event): Event to signal when the listener is set up and ready.

		Raises:
			CDPEndExceptions: If a CDP connection error occurs.
			BaseException: If any other error occurs.
		"""
		
		await self.log_cdp_step(message="Fingerprint detection listener starting.")
		
		try:
			BindingCalled = self.devtools_package.get("runtime.BindingCalled")
		
			self._fingerprint_receive_channel = self.cdp_session.listen(BindingCalled, buffer_size=100)
		
			ready_event.set()
		except CDPEndExceptions as error:
			raise error
		except BaseException as error:
			await self.log_cdp_error(error=error)
			raise error
		
		await self.log_cdp_step(message="Fingerprint detection listener started.")
		
		keep_alive = True
		while keep_alive:
			try:
				event = await self._fingerprint_receive_channel.receive()
		
				if event.name == "__osn_fingerprint_report__":
					fingerprint_data = FingerprintData.model_validate_json(event.payload)
		
					await self.log_fingerprint(level="Detect", data=fingerprint_data)
			except* CDPEndExceptions:
				keep_alive = False
			except* BaseException as error:
				await self.log_cdp_error(error=error)
	
	async def _setup_fingerprint_injection(self, ready_event: trio.Event):
		"""
		Injects the fingerprint detection scripts into the browser page.

		Enables necessary domains (Page, Runtime), adds the reporting binding,
		and evaluates the fingerprint injection script on new document creation.

		Args:
			ready_event (trio.Event): Event to signal when injection setup is complete.

		Raises:
			CDPEndExceptions: If a CDP connection error occurs.
			BaseException: If any other error occurs.
		"""
		
		if self._fingerprint_injection_script:
			try:
				await execute_cdp_command(
						self=self,
						cdp_error_mode="pass"
						if not self._is_main_target
						else "log",
						error_mode="pass"
						if not self._is_main_target
						else "log",
						function=self.devtools_package.get("page.enable"),
				)
				await execute_cdp_command(
						self=self,
						cdp_error_mode="pass"
						if not self._is_main_target
						else "log",
						error_mode="pass"
						if not self._is_main_target
						else "log",
						function=self.devtools_package.get("runtime.enable"),
				)
		
				await execute_cdp_command(
						self=self,
						cdp_error_mode="pass"
						if not self._is_main_target
						else "log",
						error_mode="pass"
						if not self._is_main_target
						else "log",
						function=self.devtools_package.get("runtime.add_binding"),
						name="__osn_fingerprint_report__",
				)
		
				await execute_cdp_command(
						self=self,
						cdp_error_mode="pass"
						if not self._is_main_target
						else "log_without_args",
						error_mode="pass"
						if not self._is_main_target
						else "log_without_args",
						function=self.devtools_package.get("page.add_script_to_evaluate_on_new_document"),
						source=self._fingerprint_injection_script,
						run_immediately=True,
				)
		
				self._nursery_object.start_soon(self._run_fingerprint_detect_listener, ready_event)
			except* CDPEndExceptions as error:
				raise error
			except* BaseException as error:
				await self.log_cdp_error(error=error)
				raise error
