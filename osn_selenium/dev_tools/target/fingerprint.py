import trio
from osn_selenium.dev_tools.utils import FingerprintData
from osn_selenium.dev_tools.errors import cdp_end_exceptions
from osn_selenium.dev_tools.target.logging import LoggingMixin
from osn_selenium.dev_tools._functions import execute_cdp_command


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
			cdp_end_exceptions: If a CDP connection error occurs.
			BaseException: If any other error occurs.
		"""
		
		await self.log_cdp_step(message="Fingerprint detection listener starting.")
		
		try:
			BindingCalled = self.devtools_package.get("runtime.BindingCalled")
		
			self._fingerprint_receive_channel = self.cdp_session.listen(BindingCalled, buffer_size=100)
		
			ready_event.set()
		except cdp_end_exceptions as error:
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
			except* cdp_end_exceptions:
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
			cdp_end_exceptions: If a CDP connection error occurs.
			BaseException: If any other error occurs.
		"""
		
		if self._fingerprint_injection_script:
			try:
				await execute_cdp_command(
						self=self,
						error_mode="log",
						function=self.devtools_package.get("page.enable")
				)
				await execute_cdp_command(
						self=self,
						error_mode="log",
						function=self.devtools_package.get("runtime.enable")
				)
		
				await execute_cdp_command(
						self=self,
						error_mode="log",
						function=self.devtools_package.get("runtime.add_binding"),
						name="__osn_fingerprint_report__"
				)
		
				await execute_cdp_command(
						self=self,
						error_mode="log",
						function=self.devtools_package.get("page.add_script_to_evaluate_on_new_document"),
						source=self._fingerprint_injection_script,
						run_immediately=True
				)
		
				self._nursery_object.start_soon(self._run_fingerprint_detect_listener, ready_event)
			except* cdp_end_exceptions as error:
				raise error
			except* BaseException as error:
				await self.log_cdp_error(error=error)
				raise error
