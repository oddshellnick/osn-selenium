from pydantic import Field
from typing import Optional
from osn_selenium._typehints import PATH_TYPEHINT
from osn_selenium._base_models import ExtraDictModel
from osn_selenium.flags._typehints import (
	AUTOPLAY_POLICY_TYPEHINT,
	LOG_LEVEL_TYPEHINT,
	USE_GL_TYPEHINT
)
from osn_selenium.flags.models.base import (
	BrowserArguments,
	BrowserAttributes,
	BrowserExperimentalOptions,
	BrowserFlags
)


__all__ = [
	"BlinkArguments",
	"BlinkAttributes",
	"BlinkExperimentalOptions",
	"BlinkFeatures",
	"BlinkFlags"
]


class BlinkFeatures(ExtraDictModel):
	"""
	Typed dictionary for Blink-specific feature flags.

	These flags control experimental or internal features within the Blink rendering engine.

	Attributes:
		calculate_native_win_occlusion (Optional[bool]): Controls native window occlusion calculation.
		accept_ch_frame (Optional[bool]): Enables/disables Accept-CH frame.
		avoid_unload_check_sync (Optional[bool]): Avoids synchronous unload checks.
		bfcache_feature (Optional[bool]): Controls the Back-Forward Cache feature.
		heavy_ad_mitigations (Optional[bool]): Enables/disables heavy ad mitigations.
		isolate_origins (Optional[bool]): Controls origin isolation.
		lazy_frame_loading (Optional[bool]): Enables/disables lazy frame loading.
		script_streaming (Optional[bool]): Controls script streaming.
		global_media_controls (Optional[bool]): Enables/disables global media controls.
		improved_cookie_controls (Optional[bool]): Enables/disables improved cookie controls.
		privacy_sandbox_settings4 (Optional[bool]): Controls Privacy Sandbox settings (version 4).
		media_router (Optional[bool]): Enables/disables media router.
		autofill_server_comm (Optional[bool]): Controls autofill server communication.
		cert_transparency_updater (Optional[bool]): Controls certificate transparency updater.
		optimization_hints (Optional[bool]): Enables/disables optimization hints.
		dial_media_route_provider (Optional[bool]): Controls DIAL media route provider.
		paint_holding (Optional[bool]): Enables/disables paint holding.
		destroy_profile_on_browser_close (Optional[bool]): Destroys user profile on browser close.
		site_per_process (Optional[bool]): Enforces site isolation (site-per-process model).
		automation_controlled (Optional[bool]): Indicates if the browser is controlled by automation.
	"""
	
	calculate_native_win_occlusion: Optional[bool] = None
	accept_ch_frame: Optional[bool] = None
	avoid_unload_check_sync: Optional[bool] = None
	bfcache_feature: Optional[bool] = None
	heavy_ad_mitigations: Optional[bool] = None
	isolate_origins: Optional[bool] = None
	lazy_frame_loading: Optional[bool] = None
	script_streaming: Optional[bool] = None
	global_media_controls: Optional[bool] = None
	improved_cookie_controls: Optional[bool] = None
	privacy_sandbox_settings4: Optional[bool] = None
	media_router: Optional[bool] = None
	autofill_server_comm: Optional[bool] = None
	cert_transparency_updater: Optional[bool] = None
	optimization_hints: Optional[bool] = None
	dial_media_route_provider: Optional[bool] = None
	paint_holding: Optional[bool] = None
	destroy_profile_on_browser_close: Optional[bool] = None
	site_per_process: Optional[bool] = None
	automation_controlled: Optional[bool] = None


class BlinkAttributes(BrowserAttributes):
	"""
	Typed dictionary for WebDriver attributes specific to Blink-based browsers.

	Attributes:
		enable_bidi (Optional[bool]): Enables/disables BiDi (Bidirectional) protocol mapper.
	"""
	
	pass


class BlinkExperimentalOptions(BrowserExperimentalOptions):
	"""
	Typed dictionary for experimental options specific to Blink-based browsers.

	Attributes:
		debugger_address (Optional[str]): The address (IP:port) of the remote debugger.
	"""
	
	debugger_address: Optional[str] = None


class BlinkArguments(BrowserArguments):
	"""
	Typed dictionary for command-line arguments specific to Blink-based browsers.

	Attributes:
		se_downloads_enabled (bool): Enables/disables Selenium downloads.
		headless_mode (bool): Runs the browser in headless mode (without a UI).
		mute_audio (bool): Mutes audio output from the browser.
		no_first_run (bool): Prevents the browser from showing the "first run" experience.
		disable_background_timer_throttling (bool): Disables throttling of background timers.
		disable_backgrounding_occluded_windows (bool): Prevents backgrounding of occluded windows.
		disable_hang_monitor (bool): Disables the browser's hang monitor.
		disable_ipc_flooding_protection (bool): Disables IPC flooding protection.
		disable_renderer_backgrounding (bool): Prevents renderer processes from being backgrounded.
		disable_back_forward_cache (bool): Disables the Back-Forward Cache.
		disable_notifications (bool): Disables web notifications.
		disable_popup_blocking (bool): Disables the built-in popup blocker.
		disable_prompt_on_repost (bool): Disables the prompt when reposting form data.
		disable_sync (bool): Disables browser synchronization features.
		disable_background_networking (bool): Disables background network activity.
		disable_breakpad (bool): Disables the crash reporter.
		disable_component_update (bool): Disables component updates.
		disable_domain_reliability (bool): Disables domain reliability monitoring.
		disable_new_content_rendering_timeout (bool): Disables timeout for new content rendering.
		disable_threaded_animation (bool): Disables threaded animation.
		disable_threaded_scrolling (bool): Disables threaded scrolling.
		disable_checker_imaging (bool): Disables checker imaging.
		disable_image_animation_resync (bool): Disables image animation resynchronization.
		disable_partial_raster (bool): Disables partial rasterization.
		disable_skia_runtime_opts (bool): Disables Skia runtime optimizations.
		disable_dev_shm_usage (bool): Disables the use of /dev/shm (important for Docker).
		disable_gpu (bool): Disables GPU hardware acceleration.
		aggressive_cache_discard (bool): Enables aggressive discarding of cached data.
		allow_running_insecure_content (bool): Allows running insecure content on HTTPS pages.
		no_process_per_site (bool): Runs all sites in a single process (less secure, but saves memory).
		enable_precise_memory_info (bool): Enables precise memory information reporting.
		use_fake_device_for_media_stream (bool): Uses a fake camera/microphone for media streams.
		use_fake_ui_for_media_stream (bool): Uses a fake UI for media stream requests.
		deny_permission_prompts (bool): Automatically denies all permission prompts.
		disable_external_intent_requests (bool): Disables external intent requests.
		noerrdialogs (bool): Suppresses error dialogs.
		enable_automation (bool): Enables automation features.
		test_type (bool): Sets the browser to test mode.
		remote_debugging_pipe (bool): Uses a pipe for remote debugging instead of a port.
		silent_debugger_extension_api (bool): Silences debugger extension API warnings.
		enable_logging_stderr (bool): Enables logging to stderr.
		password_store_basic (bool): Uses a basic password store.
		use_mock_keychain (bool): Uses a mock keychain for testing.
		enable_crash_reporter_for_testing (bool): Enables crash reporter for testing purposes.
		metrics_recording_only (bool): Records metrics without sending them.
		no_pings (bool): Disables sending pings.
		allow_pre_commit_input (bool): Allows pre-commit input.
		deterministic_mode (bool): Runs the browser in a more deterministic mode.
		run_all_compositor_stages_before_draw (bool): Runs all compositor stages before drawing.
		enable_begin_frame_control (bool): Enables begin frame control.
		in_process_gpu (bool): Runs the GPU process in-process.
		block_new_web_contents (bool): Blocks new web contents (e.g., pop-ups).
		new_window (bool): Opens a new window instead of a new tab.
		no_service_autorun (bool): Disables service autorun.
		process_per_tab (bool): Runs each tab in its own process.
		single_process (bool): Runs the browser in a single process (less stable).
		no_sandbox (bool): Disables the sandbox (less secure, but can fix some issues).
		user_agent (Optional[str]): Sets a custom user agent string.
		user_data_dir (Optional[str]): Specifies the user data directory.
		proxy_server (Optional[str]): Specifies a proxy server to use.
		remote_debugging_port (Optional[int]): Specifies the remote debugging port.
		remote_debugging_address (Optional[str]): Specifies the remote debugging address.
		use_file_for_fake_video_capture (Optional[PATH_TYPEHINT]): Uses a file for fake video capture.
		autoplay_policy (Optional[AutoplayPolicyType]): Sets the autoplay policy.
		log_level (Optional[LogLevelType]): Sets the browser's log level.
		use_gl (Optional[UseGLType]): Specifies the GL backend to use.
		force_color_profile (Optional[str]): Forces a specific color profile.
	"""
	
	headless_mode: Optional[bool] = None
	mute_audio: Optional[bool] = None
	no_first_run: Optional[bool] = None
	disable_background_timer_throttling: Optional[bool] = None
	disable_backgrounding_occluded_windows: Optional[bool] = None
	disable_hang_monitor: Optional[bool] = None
	disable_ipc_flooding_protection: Optional[bool] = None
	disable_renderer_backgrounding: Optional[bool] = None
	disable_back_forward_cache: Optional[bool] = None
	disable_notifications: Optional[bool] = None
	disable_popup_blocking: Optional[bool] = None
	disable_prompt_on_repost: Optional[bool] = None
	disable_sync: Optional[bool] = None
	disable_background_networking: Optional[bool] = None
	disable_breakpad: Optional[bool] = None
	disable_component_update: Optional[bool] = None
	disable_domain_reliability: Optional[bool] = None
	disable_new_content_rendering_timeout: Optional[bool] = None
	disable_threaded_animation: Optional[bool] = None
	disable_threaded_scrolling: Optional[bool] = None
	disable_checker_imaging: Optional[bool] = None
	disable_image_animation_resync: Optional[bool] = None
	disable_partial_raster: Optional[bool] = None
	disable_skia_runtime_opts: Optional[bool] = None
	disable_dev_shm_usage: Optional[bool] = None
	disable_gpu: Optional[bool] = None
	aggressive_cache_discard: Optional[bool] = None
	allow_running_insecure_content: Optional[bool] = None
	no_process_per_site: Optional[bool] = None
	enable_precise_memory_info: Optional[bool] = None
	use_fake_device_for_media_stream: Optional[bool] = None
	use_fake_ui_for_media_stream: Optional[bool] = None
	deny_permission_prompts: Optional[bool] = None
	disable_external_intent_requests: Optional[bool] = None
	noerrdialogs: Optional[bool] = None
	enable_automation: Optional[bool] = None
	test_type: Optional[bool] = None
	remote_debugging_pipe: Optional[bool] = None
	silent_debugger_extension_api: Optional[bool] = None
	enable_logging_stderr: Optional[bool] = None
	password_store_basic: Optional[bool] = None
	use_mock_keychain: Optional[bool] = None
	enable_crash_reporter_for_testing: Optional[bool] = None
	metrics_recording_only: Optional[bool] = None
	no_pings: Optional[bool] = None
	allow_pre_commit_input: Optional[bool] = None
	deterministic_mode: Optional[bool] = None
	run_all_compositor_stages_before_draw: Optional[bool] = None
	enable_begin_frame_control: Optional[bool] = None
	in_process_gpu: Optional[bool] = None
	block_new_web_contents: Optional[bool] = None
	new_window: Optional[bool] = None
	no_service_autorun: Optional[bool] = None
	process_per_tab: Optional[bool] = None
	single_process: Optional[bool] = None
	no_sandbox: Optional[bool] = None
	user_agent: Optional[str] = None
	user_data_dir: Optional[str] = None
	proxy_server: Optional[str] = None
	remote_debugging_port: Optional[int] = None
	remote_debugging_address: Optional[str] = None
	use_file_for_fake_video_capture: Optional[PATH_TYPEHINT] = None
	autoplay_policy: Optional[AUTOPLAY_POLICY_TYPEHINT] = None
	log_level: Optional[LOG_LEVEL_TYPEHINT] = None
	use_gl: Optional[USE_GL_TYPEHINT] = None
	force_color_profile: Optional[str] = None


class BlinkFlags(BrowserFlags):
	"""
	Typed dictionary representing a collection of all flag types for Blink-based browsers.

	Attributes:
		argument (BlinkArguments): Command-line arguments for the browser.
		experimental_option (BlinkExperimentalOptions): Experimental options for WebDriver.
		attribute (BlinkAttributes): WebDriver attributes.
		blink_feature (BlinkFeatures): Blink-specific feature flags.
	"""
	
	argument: BlinkArguments = Field(default_factory=BlinkArguments)
	experimental_option: BlinkExperimentalOptions = Field(default_factory=BlinkExperimentalOptions)
	attribute: BlinkAttributes = Field(default_factory=BlinkAttributes)
	blink_feature: BlinkFeatures = Field(default_factory=BlinkFeatures)


BlinkArguments.model_rebuild()
BlinkExperimentalOptions.model_rebuild()
BlinkAttributes.model_rebuild()
BlinkFeatures.model_rebuild()
BlinkFlags.model_rebuild()
