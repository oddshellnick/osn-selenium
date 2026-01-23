import trio
from osn_selenium.exceptions.devtools import CDPEndExceptions
from osn_selenium.dev_tools.target.logging import LoggingMixin


__all__ = ["DetachMixin"]


class DetachMixin(LoggingMixin):
	"""
	Mixin for monitoring target detach, crash, or destruction events.
	"""
	
	async def stop(self):
		"""
		Signals the target to begin its shutdown process.

		Sets the `about_to_stop_event` which allows the main loop to exit.
		"""
		
		self.about_to_stop_event.set()
	
	async def _run_detach_checking(self):
		"""
		Continuously listens for CDP events indicating the target is no longer available.

		Monitors `TargetCrashed`, `TargetDestroyed`, and `DetachedFromTarget` events.
		If the target associated with this instance is affected, it triggers the stop sequence.
		"""
		
		TargetCrashed = self.devtools_package.get("target.TargetCrashed")
		TargetDestroyed = self.devtools_package.get("target.TargetDestroyed")
		DetachedFromTarget = self.devtools_package.get("target.DetachedFromTarget")
		
		self._detached_receive_channel: trio.MemoryReceiveChannel = self.cdp_session.listen(TargetCrashed, TargetDestroyed, DetachedFromTarget, buffer_size=10)
		
		should_stop = False
		break_ = False
		
		while not should_stop and not break_:
			try:
				event = await self._detached_receive_channel.receive()
		
				if isinstance(event, (TargetCrashed, TargetDestroyed, DetachedFromTarget,)):
					if event.target_id == self.target_id:
						should_stop = True
			except* CDPEndExceptions:
				break_ = True
			except* BaseException as error:
				await self.log_cdp_error(error=error)
				break_ = True
		
		if should_stop:
			await self.stop()
