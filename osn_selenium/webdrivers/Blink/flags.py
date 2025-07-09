import pathlib
from typing import (
	Any,
	Optional,
	TypedDict,
	Union
)
from osn_selenium.webdrivers.BaseDriver.flags import (
	BrowserArguments,
	BrowserAttributes,
	BrowserExperimentalOptions,
	BrowserFlagsManager
)
from osn_selenium.webdrivers.types import (
	AutoplayPolicyType,
	FlagDefinition,
	FlagNotDefined,
	FlagType,
	LogLevelType,
	UseGLType,
	_blink_webdriver_option_type
)
from osn_selenium.webdrivers._functions import (
	bool_adding_validation_function,
	build_first_start_argument,
	int_adding_validation_function,
	optional_bool_adding_validation_function,
	path_adding_validation_function,
	str_adding_validation_function
)


class BlinkExperimentalOptions(BrowserExperimentalOptions, total=False):
	"""
	Typed dictionary for experimental options specific to Blink-based browsers.

	Attributes:
		debugger_address (Optional[str]): The address (IP:port) of the remote debugger.
	"""
	
	debugger_address: Optional[str]


class BlinkFeatures(TypedDict, total=False):
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
	
	calculate_native_win_occlusion: Optional[bool]
	accept_ch_frame: Optional[bool]
	avoid_unload_check_sync: Optional[bool]
	bfcache_feature: Optional[bool]
	heavy_ad_mitigations: Optional[bool]
	isolate_origins: Optional[bool]
	lazy_frame_loading: Optional[bool]
	script_streaming: Optional[bool]
	global_media_controls: Optional[bool]
	improved_cookie_controls: Optional[bool]
	privacy_sandbox_settings4: Optional[bool]
	media_router: Optional[bool]
	autofill_server_comm: Optional[bool]
	cert_transparency_updater: Optional[bool]
	optimization_hints: Optional[bool]
	dial_media_route_provider: Optional[bool]
	paint_holding: Optional[bool]
	destroy_profile_on_browser_close: Optional[bool]
	site_per_process: Optional[bool]
	automation_controlled: Optional[bool]


class BlinkAttributes(BrowserAttributes, total=False):
	"""
	Typed dictionary for WebDriver attributes specific to Blink-based browsers.

	Attributes:
		enable_bidi (Optional[bool]): Enables/disables BiDi (Bidirectional) protocol mapper.
	"""
	
	pass


class BlinkArguments(BrowserArguments, total=False):
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
		use_file_for_fake_video_capture (Optional[Union[str, pathlib.Path]]): Uses a file for fake video capture.
		autoplay_policy (Optional[AutoplayPolicyType]): Sets the autoplay policy.
		log_level (Optional[LogLevelType]): Sets the browser's log level.
		use_gl (Optional[UseGLType]): Specifies the GL backend to use.
		force_color_profile (Optional[str]): Forces a specific color profile.
	"""
	
	headless_mode: bool
	mute_audio: bool
	no_first_run: bool
	disable_background_timer_throttling: bool
	disable_backgrounding_occluded_windows: bool
	disable_hang_monitor: bool
	disable_ipc_flooding_protection: bool
	disable_renderer_backgrounding: bool
	disable_back_forward_cache: bool
	disable_notifications: bool
	disable_popup_blocking: bool
	disable_prompt_on_repost: bool
	disable_sync: bool
	disable_background_networking: bool
	disable_breakpad: bool
	disable_component_update: bool
	disable_domain_reliability: bool
	disable_new_content_rendering_timeout: bool
	disable_threaded_animation: bool
	disable_threaded_scrolling: bool
	disable_checker_imaging: bool
	disable_image_animation_resync: bool
	disable_partial_raster: bool
	disable_skia_runtime_opts: bool
	disable_dev_shm_usage: bool
	disable_gpu: bool
	aggressive_cache_discard: bool
	allow_running_insecure_content: bool
	no_process_per_site: bool
	enable_precise_memory_info: bool
	use_fake_device_for_media_stream: bool
	use_fake_ui_for_media_stream: bool
	deny_permission_prompts: bool
	disable_external_intent_requests: bool
	noerrdialogs: bool
	enable_automation: bool
	test_type: bool
	remote_debugging_pipe: bool
	silent_debugger_extension_api: bool
	enable_logging_stderr: bool
	password_store_basic: bool
	use_mock_keychain: bool
	enable_crash_reporter_for_testing: bool
	metrics_recording_only: bool
	no_pings: bool
	allow_pre_commit_input: bool
	deterministic_mode: bool
	run_all_compositor_stages_before_draw: bool
	enable_begin_frame_control: bool
	in_process_gpu: bool
	block_new_web_contents: bool
	new_window: bool
	no_service_autorun: bool
	process_per_tab: bool
	single_process: bool
	no_sandbox: bool
	user_agent: Optional[str]
	user_data_dir: Optional[str]
	proxy_server: Optional[str]
	remote_debugging_port: Optional[int]
	remote_debugging_address: Optional[str]
	use_file_for_fake_video_capture: Optional[Union[str, pathlib.Path]]
	autoplay_policy: Optional[AutoplayPolicyType]
	log_level: Optional[LogLevelType]
	use_gl: Optional[UseGLType]
	force_color_profile: Optional[str]


class BlinkFlags(TypedDict, total=False):
	"""
	Typed dictionary representing a collection of all flag types for Blink-based browsers.

	Attributes:
		argument (BlinkArguments): Command-line arguments for the browser.
		experimental_option (BlinkExperimentalOptions): Experimental options for WebDriver.
		attribute (BlinkAttributes): WebDriver attributes.
		blink_feature (BlinkFeatures): Blink-specific feature flags.
	"""
	
	argument: BlinkArguments
	experimental_option: BlinkExperimentalOptions
	attribute: BlinkAttributes
	blink_feature: BlinkFeatures


class BlinkFlagsManager(BrowserFlagsManager):
	"""
	Manages browser flags specifically for Blink-based browsers (like Chrome, Edge), adding support for Blink Features.

	This class extends `BrowserFlagsManager` to handle Blink-specific features,
	such as `--enable-blink-features` and `--disable-blink-features`, and provides
	a comprehensive set of predefined flags for these browsers.

	Attributes:
		_browser_exe (Optional[Union[str, pathlib.Path]]): Path to the browser executable.
		_start_page_url (Optional[str]): The URL to open when the browser starts.
		_enable_blink_features (dict[str, str]): Stores enabled Blink feature commands.
		_disable_blink_features (dict[str, str]): Stores disabled Blink feature commands.
	"""
	
	def __init__(
			self,
			browser_exe: Optional[Union[str, pathlib.Path]] = None,
			start_page_url: Optional[str] = None,
			flags_types: Optional[dict[str, FlagType]] = None,
			flags_definitions: Optional[dict[str, FlagDefinition]] = None
	):
		"""
		Initializes the BlinkFlagsManager.

		Args:
			browser_exe (Optional[Union[str, pathlib.Path]]): Path to the browser executable file.
			start_page_url (Optional[str]): Initial URL to open on browser startup.
			flags_types (Optional[dict[str, FlagType]]): Custom flag types to add or override.
			flags_definitions (Optional[dict[str, FlagDefinition]]): Custom flag definitions to add or override.
		"""
		
		blink_flags_types = {
			"blink_feature": FlagType(
					set_flag_function=self.set_blink_feature,
					remove_flag_function=self.remove_blink_feature,
					set_flags_function=self.set_blink_features,
					update_flags_function=self.update_blink_features,
					clear_flags_function=self.clear_blink_features,
					build_options_function=self.build_options_blink_features,
					build_start_args_function=self.build_start_args_blink_features
			),
		}
		
		if flags_types is not None:
			blink_flags_types.update(flags_types)
		
		blink_flags_definitions = {
			"debugger_address": FlagDefinition(
					name="debugger_address",
					command="debuggerAddress",
					type="experimental_option",
					mode="webdriver_option",
					adding_validation_function=str_adding_validation_function
			),
			"remote_debugging_port": FlagDefinition(
					name="remote_debugging_port",
					command='--remote-debugging-port={value}',
					type="argument",
					mode="startup_argument",
					adding_validation_function=int_adding_validation_function
			),
			"remote_debugging_address": FlagDefinition(
					name="remote_debugging_address",
					command='--remote-debugging-address="{value}"',
					type="argument",
					mode="startup_argument",
					adding_validation_function=str_adding_validation_function
			),
			"user_agent": FlagDefinition(
					name="user_agent",
					command='--user-agent="{value}"',
					type="argument",
					mode="both",
					adding_validation_function=str_adding_validation_function
			),
			"user_data_dir": FlagDefinition(
					name="user_data_dir",
					command='--user-data-dir="{value}"',
					type="argument",
					mode="startup_argument",
					adding_validation_function=str_adding_validation_function
			),
			"proxy_server": FlagDefinition(
					name="proxy_server",
					command='--proxy-server="{value}"',
					type="argument",
					mode="webdriver_option",
					adding_validation_function=str_adding_validation_function
			),
			"headless_mode": FlagDefinition(
					name="headless_mode",
					command="--headless",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"mute_audio": FlagDefinition(
					name="mute_audio",
					command="--mute-audio",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"disable_background_timer_throttling": FlagDefinition(
					name="disable_background_timer_throttling",
					command="--disable-background-timer-throttling",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"disable_backgrounding_occluded_windows": FlagDefinition(
					name="disable_backgrounding_occluded_windows",
					command="--disable-backgrounding-occluded-windows",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"disable_hang_monitor": FlagDefinition(
					name="disable_hang_monitor",
					command="--disable-hang-monitor",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"disable_ipc_flooding_protection": FlagDefinition(
					name="disable_ipc_flooding_protection",
					command="--disable-ipc-flooding-protection",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"disable_renderer_backgrounding": FlagDefinition(
					name="disable_renderer_backgrounding",
					command="--disable-renderer-backgrounding",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"aggressive_cache_discard": FlagDefinition(
					name="aggressive_cache_discard",
					command="--aggressive-cache-discard",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"allow_running_insecure_content": FlagDefinition(
					name="allow_running_insecure_content",
					command="--allow-running-insecure-content",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"disable_back_forward_cache": FlagDefinition(
					name="disable_back_forward_cache",
					command="--disable-back-forward-cache",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"no_process_per_site": FlagDefinition(
					name="no_process_per_site",
					command="--no-process-per-site",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"enable_precise_memory_info": FlagDefinition(
					name="enable_precise_memory_info",
					command="--enable-precise-memory-info",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"use_fake_device_for_media_stream": FlagDefinition(
					name="use_fake_device_for_media_stream",
					command="--use-fake-device-for-media-stream",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"use_fake_ui_for_media_stream": FlagDefinition(
					name="use_fake_ui_for_media_stream",
					command="--use-fake-ui-for-media-stream",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"use_file_for_fake_video_capture": FlagDefinition(
					name="use_file_for_fake_video_capture",
					command='--use-file-for-fake-video-capture={value}',
					type="argument",
					mode="both",
					adding_validation_function=path_adding_validation_function
			),
			"autoplay_policy": FlagDefinition(
					name="autoplay_policy",
					command='--autoplay-policy={value}',
					type="argument",
					mode="both",
					adding_validation_function=str_adding_validation_function
			),
			"deny_permission_prompts": FlagDefinition(
					name="deny_permission_prompts",
					command="--deny-permission-prompts",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"disable_external_intent_requests": FlagDefinition(
					name="disable_external_intent_requests",
					command="--disable-external-intent-requests",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"disable_notifications": FlagDefinition(
					name="disable_notifications",
					command="--disable-notifications",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"disable_popup_blocking": FlagDefinition(
					name="disable_popup_blocking",
					command="--disable-popup-blocking",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"disable_prompt_on_repost": FlagDefinition(
					name="disable_prompt_on_repost",
					command="--disable-prompt-on-repost",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"noerrdialogs": FlagDefinition(
					name="noerrdialogs",
					command="--noerrdialogs",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"enable_automation": FlagDefinition(
					name="enable_automation",
					command="--enable-automation",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"test_type": FlagDefinition(
					name="test_type",
					command="--test-type",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"remote_debugging_pipe": FlagDefinition(
					name="remote_debugging_pipe",
					command="--remote-debugging-pipe",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"silent_debugger_extension_api": FlagDefinition(
					name="silent_debugger_extension_api",
					command="--silent-debugger-extension-api",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"enable_logging_stderr": FlagDefinition(
					name="enable_logging_stderr",
					command="enable-logging=stderr",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"log_level": FlagDefinition(
					name="log_level",
					command='--log-level={value}',
					type="argument",
					mode="both",
					adding_validation_function=str_adding_validation_function
			),
			"password_store_basic": FlagDefinition(
					name="password_store_basic",
					command="--password-store=basic",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"use_mock_keychain": FlagDefinition(
					name="use_mock_keychain",
					command="--use-mock-keychain",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"disable_background_networking": FlagDefinition(
					name="disable_background_networking",
					command="--disable-background-networking",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"disable_breakpad": FlagDefinition(
					name="disable_breakpad",
					command="--disable-breakpad",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"disable_component_update": FlagDefinition(
					name="disable_component_update",
					command="--disable-component-update",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"disable_domain_reliability": FlagDefinition(
					name="disable_domain_reliability",
					command="--disable-domain-reliability",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"disable_sync": FlagDefinition(
					name="disable_sync",
					command="--disable-sync",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"enable_crash_reporter_for_testing": FlagDefinition(
					name="enable_crash_reporter_for_testing",
					command="--enable-crash-reporter-for-testing",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"metrics_recording_only": FlagDefinition(
					name="metrics_recording_only",
					command="--metrics-recording-only",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"no_pings": FlagDefinition(
					name="no_pings",
					command="--no-pings",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"allow_pre_commit_input": FlagDefinition(
					name="allow_pre_commit_input",
					command="--allow-pre-commit-input",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"deterministic_mode": FlagDefinition(
					name="deterministic_mode",
					command="--deterministic-mode",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"run_all_compositor_stages_before_draw": FlagDefinition(
					name="run_all_compositor_stages_before_draw",
					command="--run-all-compositor-stages-before-draw",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"disable_new_content_rendering_timeout": FlagDefinition(
					name="disable_new_content_rendering_timeout",
					command="--disable-new-content-rendering-timeout",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"enable_begin_frame_control": FlagDefinition(
					name="enable_begin_frame_control",
					command="--enable-begin-frame-control",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"disable_threaded_animation": FlagDefinition(
					name="disable_threaded_animation",
					command="--disable-threaded-animation",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"disable_threaded_scrolling": FlagDefinition(
					name="disable_threaded_scrolling",
					command="--disable-threaded-scrolling",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"disable_checker_imaging": FlagDefinition(
					name="disable_checker_imaging",
					command="--disable-checker-imaging",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"disable_image_animation_resync": FlagDefinition(
					name="disable_image_animation_resync",
					command="--disable-image-animation-resync",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"disable_partial_raster": FlagDefinition(
					name="disable_partial_raster",
					command="--disable-partial-raster",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"disable_skia_runtime_opts": FlagDefinition(
					name="disable_skia_runtime_opts",
					command="--disable-skia-runtime-opts",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"in_process_gpu": FlagDefinition(
					name="in_process_gpu",
					command="--in-process-gpu",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"use_gl": FlagDefinition(
					name="use_gl",
					command='--use-gl={value}',
					type="argument",
					mode="both",
					adding_validation_function=str_adding_validation_function
			),
			"block_new_web_contents": FlagDefinition(
					name="block_new_web_contents",
					command="--block-new-web-contents",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"force_color_profile": FlagDefinition(
					name="force_color_profile",
					command='--force-color-profile={value}',
					type="argument",
					mode="both",
					adding_validation_function=str_adding_validation_function
			),
			"new_window": FlagDefinition(
					name="new_window",
					command="--new-window",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"no_service_autorun": FlagDefinition(
					name="no_service_autorun",
					command="--no-service-autorun",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"process_per_tab": FlagDefinition(
					name="process_per_tab",
					command="--process-per-tab",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"single_process": FlagDefinition(
					name="single_process",
					command="--single-process",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"no_sandbox": FlagDefinition(
					name="no_sandbox",
					command="--no-sandbox",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"disable_dev_shm_usage": FlagDefinition(
					name="disable_dev_shm_usage",
					command="--disable-dev-shm-usage",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"disable_gpu": FlagDefinition(
					name="disable_gpu",
					command="--disable-gpu",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"no_first_run": FlagDefinition(
					name="no_first_run",
					command="--no-first-run",
					type="argument",
					mode="both",
					adding_validation_function=bool_adding_validation_function
			),
			"calculate_native_win_occlusion": FlagDefinition(
					name="calculate_native_win_occlusion",
					command="CalculateNativeWinOcclusion",
					type="blink_feature",
					mode="both",
					adding_validation_function=optional_bool_adding_validation_function
			),
			"accept_ch_frame": FlagDefinition(
					name="accept_ch_frame",
					command="AcceptCHFrame",
					type="blink_feature",
					mode="both",
					adding_validation_function=optional_bool_adding_validation_function
			),
			"avoid_unload_check_sync": FlagDefinition(
					name="avoid_unload_check_sync",
					command="AvoidUnnecessaryBeforeUnloadCheckSync",
					type="blink_feature",
					mode="both",
					adding_validation_function=optional_bool_adding_validation_function
			),
			"bfcache_feature": FlagDefinition(
					name="bfcache_feature",
					command="BackForwardCache",
					type="blink_feature",
					mode="both",
					adding_validation_function=optional_bool_adding_validation_function
			),
			"heavy_ad_mitigations": FlagDefinition(
					name="heavy_ad_mitigations",
					command="HeavyAdPrivacyMitigations",
					type="blink_feature",
					mode="both",
					adding_validation_function=optional_bool_adding_validation_function
			),
			"isolate_origins": FlagDefinition(
					name="isolate_origins",
					command="IsolateOrigins",
					type="blink_feature",
					mode="both",
					adding_validation_function=optional_bool_adding_validation_function
			),
			"lazy_frame_loading": FlagDefinition(
					name="lazy_frame_loading",
					command="LazyFrameLoading",
					type="blink_feature",
					mode="both",
					adding_validation_function=optional_bool_adding_validation_function
			),
			"script_streaming": FlagDefinition(
					name="script_streaming",
					command="ScriptStreaming",
					type="blink_feature",
					mode="both",
					adding_validation_function=optional_bool_adding_validation_function
			),
			"global_media_controls": FlagDefinition(
					name="global_media_controls",
					command="GlobalMediaControls",
					type="blink_feature",
					mode="both",
					adding_validation_function=optional_bool_adding_validation_function
			),
			"improved_cookie_controls": FlagDefinition(
					name="improved_cookie_controls",
					command="ImprovedCookieControls",
					type="blink_feature",
					mode="both",
					adding_validation_function=optional_bool_adding_validation_function
			),
			"privacy_sandbox_settings4": FlagDefinition(
					name="privacy_sandbox_settings4",
					command="PrivacySandboxSettings4",
					type="blink_feature",
					mode="both",
					adding_validation_function=optional_bool_adding_validation_function
			),
			"media_router": FlagDefinition(
					name="media_router",
					command="MediaRouter",
					type="blink_feature",
					mode="both",
					adding_validation_function=optional_bool_adding_validation_function
			),
			"autofill_server_comm": FlagDefinition(
					name="autofill_server_comm",
					command="AutofillServerCommunication",
					type="blink_feature",
					mode="both",
					adding_validation_function=optional_bool_adding_validation_function
			),
			"cert_transparency_updater": FlagDefinition(
					name="cert_transparency_updater",
					command="CertificateTransparencyComponentUpdater",
					type="blink_feature",
					mode="both",
					adding_validation_function=optional_bool_adding_validation_function
			),
			"optimization_hints": FlagDefinition(
					name="optimization_hints",
					command="OptimizationHints",
					type="blink_feature",
					mode="both",
					adding_validation_function=optional_bool_adding_validation_function
			),
			"dial_media_route_provider": FlagDefinition(
					name="dial_media_route_provider",
					command="DialMediaRouteProvider",
					type="blink_feature",
					mode="both",
					adding_validation_function=optional_bool_adding_validation_function
			),
			"paint_holding": FlagDefinition(
					name="paint_holding",
					command="PaintHolding",
					type="blink_feature",
					mode="both",
					adding_validation_function=optional_bool_adding_validation_function
			),
			"destroy_profile_on_browser_close": FlagDefinition(
					name="destroy_profile_on_browser_close",
					command="DestroyProfileOnBrowserClose",
					type="blink_feature",
					mode="both",
					adding_validation_function=optional_bool_adding_validation_function
			),
			"site_per_process": FlagDefinition(
					name="site_per_process",
					command="site-per-process",
					type="blink_feature",
					mode="both",
					adding_validation_function=optional_bool_adding_validation_function
			),
			"automation_controlled": FlagDefinition(
					name="automation_controlled",
					command="AutomationControlled",
					type="blink_feature",
					mode="both",
					adding_validation_function=optional_bool_adding_validation_function
			),
		}
		
		if flags_definitions is not None:
			blink_flags_definitions.update(flags_definitions)
		
		super().__init__(
				flags_types=blink_flags_types,
				flags_definitions=blink_flags_definitions
		)
		
		self._browser_exe = browser_exe
		self._start_page_url = start_page_url
		self._enable_blink_features: dict[str, str] = {}
		self._disable_blink_features: dict[str, str] = {}
	
	def build_start_args_blink_features(self) -> list[str]:
		"""
		Builds a list of Blink feature arguments for browser startup.

		Returns:
			list[str]: A list of startup arguments for Blink features.
		"""
		
		start_args = []
		
		enable_blink_features = dict(
				filter(
						lambda item: self._flags_definitions_by_types["blink_feature"][item[0]]["mode"] in ["startup_argument", "both"],
						self._enable_blink_features.items()
				)
		)
		disable_blink_features = dict(
				filter(
						lambda item: self._flags_definitions_by_types["blink_feature"][item[0]]["mode"] in ["startup_argument", "both"],
						self._disable_blink_features.items()
				)
		)
		
		if enable_blink_features:
			start_args.append("--enable-blink-features=" + ",".join(enable_blink_features.values()))
		
		if disable_blink_features:
			start_args.append("--disable-blink-features=" + ",".join(disable_blink_features.values()))
		
		return start_args
	
	def build_options_blink_features(self, options: _blink_webdriver_option_type) -> _blink_webdriver_option_type:
		"""
		Adds configured Blink features (`--enable-blink-features` and `--disable-blink-features`) to the WebDriver options.

		Args:
			options (_blink_webdriver_option_type): The WebDriver options object to modify.

		Returns:
			_blink_webdriver_option_type: The modified WebDriver options object.
		"""
		
		enable_blink_features = dict(
				filter(
						lambda item: self._flags_definitions_by_types["blink_feature"][item[0]]["mode"] in ["webdriver_option", "both"],
						self._enable_blink_features.items()
				)
		)
		disable_blink_features = dict(
				filter(
						lambda item: self._flags_definitions_by_types["blink_feature"][item[0]]["mode"] in ["webdriver_option", "both"],
						self._disable_blink_features.items()
				)
		)
		
		if enable_blink_features:
			options.add_argument("--enable-blink-features=" + ",".join(enable_blink_features.values()))
		
		if disable_blink_features:
			options.add_argument("--disable-blink-features=" + ",".join(disable_blink_features.values()))
		
		return options
	
	def clear_blink_features(self):
		"""Clears all configured Blink features."""
		
		self._enable_blink_features = {}
		self._disable_blink_features = {}
	
	def remove_blink_feature(self, blink_feature_name: str):
		"""
		Removes a configured Blink feature.

		This removes the feature from both the enabled and disabled lists.

		Args:
			blink_feature_name (str): The name of the Blink feature to remove.
		"""
		
		self._enable_blink_features.pop(blink_feature_name, None)
		self._disable_blink_features.pop(blink_feature_name, None)
	
	def set_blink_feature(self, blink_feature: FlagDefinition, enable: Optional[bool]):
		"""
		Sets a Blink feature to be either enabled or disabled.

		Args:
			blink_feature (FlagDefinition): The definition of the Blink feature.
			enable (Optional[bool]): `True` to enable, `False` to disable. If `None`, the feature is removed.
		"""
		
		blink_feature_name = blink_feature["name"]
		blink_feature_command = blink_feature["command"]
		adding_validation_function = blink_feature["adding_validation_function"]
		
		self.remove_blink_feature(blink_feature_command)
		
		if adding_validation_function(enable):
			if enable:
				self._enable_blink_features[blink_feature_name] = blink_feature_command
			else:
				self._disable_blink_features[blink_feature_name] = blink_feature_command
	
	def update_blink_features(self, blink_features: Union[BlinkFeatures, dict[str, Optional[bool]]]):
		"""
		Updates Blink features from a dictionary without clearing existing ones.

		Args:
			blink_features (Union[BlinkFeatures, dict[str, Optional[bool]]]): A dictionary of Blink features to set or update.

		Raises:
			ValueError: If an unknown Blink feature key is provided.
		"""
		
		for key, value in blink_features.items():
			flag_definition = self._flags_definitions_by_types["blink_feature"].get(key, FlagNotDefined())
		
			if isinstance(flag_definition, FlagNotDefined):
				raise ValueError(f"Unknown blink feature: {key}.")
		
			self.set_blink_feature(flag_definition, value)
	
	def set_blink_features(self, blink_features: Union[BlinkFeatures, dict[str, Optional[bool]]]):
		"""
		Clears existing and sets new Blink features from a dictionary.

		Args:
			blink_features (Union[BlinkFeatures, dict[str, Optional[bool]]]): A dictionary of Blink features to set.

		Raises:
			ValueError: If an unknown Blink feature key is provided.
		"""
		
		self.clear_blink_features()
		self.update_blink_features(blink_features)
	
	def _renew_webdriver_options(self) -> _blink_webdriver_option_type:
		"""
		Abstract method to renew WebDriver options. Must be implemented in child classes.

		This method is intended to be overridden in subclasses to provide
		browser-specific WebDriver options instances (e.g., ChromeOptions, EdgeOptions).

		Returns:
			_blink_webdriver_option_type: A new instance of WebDriver options (e.g., ChromeOptions, EdgeOptions).

		Raises:
			NotImplementedError: If the method is not implemented in a subclass.
		"""
		
		raise NotImplementedError("This function must be implemented in child classes.")
	
	@property
	def browser_exe(self) -> Optional[Union[str, pathlib.Path]]:
		"""
		Returns the browser executable path.

		This property retrieves the path to the browser executable that will be used to start the browser instance.

		Returns:
			Optional[Union[str, pathlib.Path]]: The path to the browser executable.
		"""
		
		return self._browser_exe
	
	@browser_exe.setter
	def browser_exe(self, value: Optional[Union[str, pathlib.Path]]):
		"""
		Sets the path to the browser executable.

		Args:
			value (Optional[Union[str, pathlib.Path]]): The new path for the browser executable.
		"""
		
		self._browser_exe = value
	
	def build_options_arguments(self, options: _blink_webdriver_option_type) -> _blink_webdriver_option_type:
		"""
		Adds configured command-line arguments to the WebDriver options.

		Args:
			options (_blink_webdriver_option_type): The WebDriver options object.

		Returns:
			_blink_webdriver_option_type: The modified WebDriver options object.
		"""
		
		return super().build_options_arguments(options)
	
	def build_options_attributes(self, options: _blink_webdriver_option_type) -> _blink_webdriver_option_type:
		"""
		Applies configured attributes to the WebDriver options.

		Args:
			options (_blink_webdriver_option_type): The WebDriver options object.

		Returns:
			_blink_webdriver_option_type: The modified WebDriver options object.
		"""
		
		return super().build_options_attributes(options)
	
	def build_options_experimental_options(self, options: _blink_webdriver_option_type) -> _blink_webdriver_option_type:
		"""
		Adds experimental options to the WebDriver options.

		Args:
			options (_blink_webdriver_option_type): The WebDriver options object.

		Returns:
			_blink_webdriver_option_type: The modified WebDriver options object.
		"""
		
		return super().build_options_experimental_options(options)
	
	def build_start_args_arguments(self) -> list[str]:
		"""
		Builds a list of command-line arguments for browser startup.

		Returns:
			list[str]: A list of startup arguments.
		"""
		
		return super().build_start_args_arguments()
	
	def clear_flags(self):
		"""Clears all configured flags and resets the start page URL."""
		
		super().clear_flags()
		self._start_page_url = None
	
	@property
	def options(self) -> _blink_webdriver_option_type:
		"""
		Builds and returns a Blink-specific WebDriver options object.

		Returns:
			_blink_webdriver_option_type: A configured Blink-based WebDriver options object.
		"""
		
		return super().options
	
	def set_arguments(self, arguments: Union[BlinkArguments, dict[str, Any]]):
		"""
		Clears existing and sets new command-line arguments from a dictionary.

		Args:
			arguments (Union[BlinkArguments, dict[str, Any]]): A dictionary of arguments to set.

		Raises:
			ValueError: If an unknown argument key is provided.
		"""
		
		super().set_arguments(arguments)
	
	def set_attributes(self, attributes: Union[BlinkAttributes, dict[str, Any]]):
		"""
		Clears existing and sets new browser attributes from a dictionary.

		Args:
			attributes (Union[BlinkAttributes, dict[str, Any]]): A dictionary of attributes to set.

		Raises:
			ValueError: If an unknown attribute key is provided.
		"""
		
		super().set_attributes(attributes)
	
	def set_experimental_options(
			self,
			experimental_options: Union[BlinkExperimentalOptions, dict[str, Any]]
	):
		"""
		Clears existing and sets new experimental options from a dictionary.

		Args:
			experimental_options (Union[BlinkExperimentalOptions, dict[str, Any]]): A dictionary of experimental options to set.

		Raises:
			ValueError: If an unknown experimental option key is provided.
		"""
		
		super().set_experimental_options(experimental_options)
	
	def set_flags(self, flags: Union[BlinkFlags, dict[str, dict[str, Any]]]):
		"""
		Clears all existing flags and sets new ones, including Blink features.

		This method delegates to the parent `set_flags` method, allowing it to handle
		all flag types defined in this manager, including 'arguments', 'experimental_options',
		'attributes', and 'blink_features'.

		Args:
			flags (Union[BlinkFlags, dict[str, dict[str, Any]]]): A dictionary where keys are flag types
				and values are dictionaries of flags to set for that type.
		"""
		
		super().set_flags(flags)
	
	@property
	def start_args(self) -> list[str]:
		"""
		Builds and returns a list of all command-line arguments for browser startup.

		Returns:
			list[str]: A list of startup arguments.
		"""
		
		args = []
		
		for type_name, type_functions in self._flags_types.items():
			args += type_functions["build_start_args_function"]()
		
		return args
	
	@property
	def start_command(self) -> str:
		"""
		Generates the full browser start command.

		Composes the command line arguments based on the current settings
		(debugging port, profile directory, headless mode, etc.) and the browser executable path.

		Returns:
			str: The complete command string to start the browser with specified arguments.
		"""
		
		start_args = [build_first_start_argument(self._browser_exe)]
		start_args += self.start_args
		
		if self._start_page_url is not None:
			start_args.append(self._start_page_url)
		
		return " ".join(start_args)
	
	@property
	def start_page_url(self) -> Optional[str]:
		"""
		Gets the initial URL to open when the browser starts.

		Returns:
			Optional[str]: The start page URL.
		"""
		
		return self._start_page_url
	
	@start_page_url.setter
	def start_page_url(self, value: Optional[str]):
		"""
		Sets the initial URL to open when the browser starts.

		Args:
			value (Optional[str]): The URL to set as the start page.
		"""
		
		self._start_page_url = value
	
	def update_arguments(self, arguments: Union[BlinkArguments, dict[str, Any]]):
		"""
		Updates command-line arguments from a dictionary without clearing existing ones.

		Args:
			arguments (Union[BlinkArguments, dict[str, Any]]): A dictionary of arguments to set or update.

		Raises:
			ValueError: If an unknown argument key is provided.
		"""
		
		super().update_arguments(arguments)
	
	def update_attributes(self, attributes: Union[BlinkAttributes, dict[str, Any]]):
		"""
		Updates browser attributes from a dictionary without clearing existing ones.

		Args:
			attributes (Union[BlinkAttributes, dict[str, Any]]): A dictionary of attributes to set or update.

		Raises:
			ValueError: If an unknown attribute key is provided.
		"""
		
		super().update_attributes(attributes)
	
	def update_experimental_options(
			self,
			experimental_options: Union[BlinkExperimentalOptions, dict[str, Any]]
	):
		"""
		Updates experimental options from a dictionary without clearing existing ones.

		Args:
			experimental_options (Union[BlinkExperimentalOptions, dict[str, Any]]): A dictionary of experimental options to set or update.

		Raises:
			ValueError: If an unknown experimental option key is provided.
		"""
		
		super().update_experimental_options(experimental_options)
	
	def update_flags(self, flags: Union[BlinkFlags, dict[str, dict[str, Any]]]):
		"""
		Updates all flags, including Blink features, without clearing existing ones.

		This method delegates to the parent `update_flags` method, allowing it to handle
		all flag types defined in this manager, including 'arguments', 'experimental_options',
		'attributes', and 'blink_features'.

		Args:
			flags (Union[BlinkFlags, dict[str, dict[str, Any]]]): A dictionary where keys are flag types
				and values are dictionaries of flags to update for that type.
		"""
		
		super().update_flags(flags)
