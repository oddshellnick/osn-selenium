import pathlib
from typing import Dict, List, Optional
from osn_selenium._functions import validate_path
from osn_selenium._typehints import PATH_TYPEHINT
from osn_selenium.flags.base import BrowserFlagsManager
from osn_selenium.exceptions.flags import FlagNotDefinedError
from osn_selenium.flags._functions import (
	build_first_start_argument
)
from osn_selenium.exceptions.logic import (
	AbstractImplementationError
)
from osn_selenium.flags._typehints import (
	BLINK_WEBDRIVER_OPTION_TYPEHINT
)
from osn_selenium.flags.models.base import (
	FlagDefinition,
	FlagNotDefined,
	FlagType
)
from osn_selenium.flags.models.blink import (
	BlinkArguments,
	BlinkAttributes,
	BlinkExperimentalOptions,
	BlinkFeatures,
	BlinkFlags
)
from osn_selenium.flags._validators import (
	bool_adding_validation_function,
	int_adding_validation_function,
	optional_bool_adding_validation_function,
	path_adding_validation_function,
	str_adding_validation_function
)


__all__ = ["BlinkFlagsManager"]


class BlinkFlagsManager(BrowserFlagsManager):
	"""
	Manages browser flags specifically for Blink-based browsers (like Chrome, Edge), adding support for Blink Features.

	This class extends `BrowserFlagsManager` to handle Blink-specific features,
	such as `--enable-blink-features` and `--disable-blink-features`, and provides
	a comprehensive set of predefined flags for these browsers.
	"""
	
	def __init__(
			self,
			browser_exe: Optional[PATH_TYPEHINT] = None,
			start_page_url: Optional[str] = None,
			flags_types: Optional[Dict[str, FlagType]] = None,
			flags_definitions: Optional[Dict[str, FlagDefinition]] = None
	):
		"""
		Initializes the BlinkFlagsManager.

		Args:
			browser_exe (Optional[PATH_TYPEHINT]): Path to the browser executable file.
			start_page_url (Optional[str]): Initial URL to open on browser startup.
			flags_types (Optional[Dict[str, FlagType]]): Custom flag types to add or override.
			flags_definitions (Optional[Dict[str, FlagDefinition]]): Custom flag definitions to add or override.
		"""
		
		blink_flags_types = {
			"blink_feature": FlagType(
					set_flag_function=self.set_blink_feature,
					remove_flag_function=self.remove_blink_feature,
					set_flags_function=self.set_blink_features,
					update_flags_function=self.update_blink_features,
					clear_flags_function=self.clear_blink_features,
					build_options_function=self._build_options_blink_features,
					build_start_args_function=self._build_start_args_blink_features
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
		
		self._browser_exe = validate_path(path=browser_exe)
		
		self._start_page_url = start_page_url
		self._enable_blink_features: Dict[str, str] = {}
		self._disable_blink_features: Dict[str, str] = {}
	
	def _build_start_args_blink_features(self) -> List[str]:
		"""
		Builds a List of Blink feature arguments for browser startup.

		Returns:
			List[str]: A List of startup arguments for Blink features.
		"""
		
		start_args = []
		
		enable_blink_features = dict(
				filter(
						lambda item: self._flags_definitions_by_types["blink_feature"][item[0]].mode in ["startup_argument", "both"],
						self._enable_blink_features.items()
				)
		)
		disable_blink_features = dict(
				filter(
						lambda item: self._flags_definitions_by_types["blink_feature"][item[0]].mode in ["startup_argument", "both"],
						self._disable_blink_features.items()
				)
		)
		
		if enable_blink_features:
			start_args.append("--enable-blink-features=" + ",".join(enable_blink_features.values()))
		
		if disable_blink_features:
			start_args.append("--disable-blink-features=" + ",".join(disable_blink_features.values()))
		
		return start_args
	
	def _build_options_blink_features(self, options: BLINK_WEBDRIVER_OPTION_TYPEHINT) -> BLINK_WEBDRIVER_OPTION_TYPEHINT:
		"""
		Adds configured Blink features (`--enable-blink-features` and `--disable-blink-features`) to the WebDriver options.

		Args:
			options (blink_webdriver_option_type): The WebDriver options object to modify.

		Returns:
			blink_webdriver_option_type: The modified WebDriver options object.
		"""
		
		enable_blink_features = dict(
				filter(
						lambda item: self._flags_definitions_by_types["blink_feature"][item[0]].mode in ["webdriver_option", "both"],
						self._enable_blink_features.items()
				)
		)
		disable_blink_features = dict(
				filter(
						lambda item: self._flags_definitions_by_types["blink_feature"][item[0]].mode in ["webdriver_option", "both"],
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
		
		blink_feature_name = blink_feature.name
		blink_feature_command = blink_feature.command
		adding_validation_function = blink_feature.adding_validation_function
		
		self.remove_blink_feature(blink_feature_command)
		
		if adding_validation_function(enable):
			if enable:
				self._enable_blink_features[blink_feature_name] = blink_feature_command
			else:
				self._disable_blink_features[blink_feature_name] = blink_feature_command
	
	def update_blink_features(self, blink_features: BlinkFeatures):
		"""
		Updates Blink features from a dictionary without clearing existing ones.

		Args:
			blink_features (BlinkFeatures): A dictionary of Blink features to set or update.

		Raises:
			ValueError: If an unknown Blink feature key is provided.
		"""
		
		for key, value in blink_features.model_dump(exclude_none=True).items():
			flag_definition = self._flags_definitions_by_types["blink_feature"].get(key, FlagNotDefined())
		
			if isinstance(flag_definition, FlagNotDefined):
				raise FlagNotDefinedError(flag_name=key, flag_type="blink features")
		
			self.set_blink_feature(flag_definition, value)
	
	def set_blink_features(self, blink_features: BlinkFeatures):
		"""
		Clears existing and sets new Blink features from a dictionary.

		Args:
			blink_features (BlinkFeatures): A dictionary of Blink features to set.
		"""
		
		self.clear_blink_features()
		self.update_blink_features(blink_features)
	
	def _build_options_arguments(self, options: BLINK_WEBDRIVER_OPTION_TYPEHINT) -> BLINK_WEBDRIVER_OPTION_TYPEHINT:
		"""
		Adds configured command-line arguments to the WebDriver options.

		Args:
			options (blink_webdriver_option_type): The WebDriver options object.

		Returns:
			blink_webdriver_option_type: The modified WebDriver options object.
		"""
		
		return super()._build_options_arguments(options)
	
	def _build_options_attributes(self, options: BLINK_WEBDRIVER_OPTION_TYPEHINT) -> BLINK_WEBDRIVER_OPTION_TYPEHINT:
		"""
		Applies configured attributes to the WebDriver options.

		Args:
			options (blink_webdriver_option_type): The WebDriver options object.

		Returns:
			blink_webdriver_option_type: The modified WebDriver options object.
		"""
		
		return super()._build_options_attributes(options)
	
	def _build_options_experimental_options(self, options: BLINK_WEBDRIVER_OPTION_TYPEHINT) -> BLINK_WEBDRIVER_OPTION_TYPEHINT:
		"""
		Adds experimental options to the WebDriver options.

		Args:
			options (blink_webdriver_option_type): The WebDriver options object.

		Returns:
			blink_webdriver_option_type: The modified WebDriver options object.
		"""
		
		return super()._build_options_experimental_options(options)
	
	def _build_start_args_arguments(self) -> List[str]:
		"""
		Builds a List of command-line arguments for browser startup.

		Returns:
			List[str]: A List of startup arguments.
		"""
		
		return super()._build_start_args_arguments()
	
	def _renew_webdriver_options(self) -> BLINK_WEBDRIVER_OPTION_TYPEHINT:
		"""
		Abstract method to renew WebDriver options. Must be implemented in child classes.

		This method is intended to be overridden in subclasses to provide
		browser-specific WebDriver options instances (e.g., ChromeOptions, EdgeOptions).

		Returns:
			blink_webdriver_option_type: A new instance of WebDriver options (e.g., ChromeOptions, EdgeOptions).

		Raises:
			NotImplementedError: If the method is not implemented in a subclass.
		"""
		
		raise AbstractImplementationError(
				method_name="_renew_webdriver_options",
				class_name=self.__class__.__name__
		)
	
	@property
	def browser_exe(self) -> Optional[pathlib.Path]:
		"""
		Returns the browser executable path.

		This property retrieves the path to the browser executable that will be used to start the browser instance.

		Returns:
			Optional[pathlib.Path]: The path to the browser executable.
		"""
		
		return self._browser_exe
	
	@browser_exe.setter
	def browser_exe(self, value: Optional[PATH_TYPEHINT]):
		"""
		Sets the path to the browser executable.

		Args:
			value (Optional[pathlib.Path]): The new path for the browser executable.
		"""
		
		self._browser_exe = validate_path(path=value)
	
	def clear_flags(self):
		"""Clears all configured flags and resets the start page URL."""
		
		super().clear_flags()
		self._start_page_url = None
	
	@property
	def options(self) -> BLINK_WEBDRIVER_OPTION_TYPEHINT:
		"""
		Builds and returns a Blink-specific WebDriver options object.

		Returns:
			blink_webdriver_option_type: A configured Blink-based WebDriver options object.
		"""
		
		return super().options
	
	def set_arguments(self, arguments: BlinkArguments):
		"""
		Clears existing and sets new command-line arguments from a dictionary.

		Args:
			arguments (BlinkArguments): A dictionary of arguments to set.

		Raises:
			ValueError: If an unknown argument key is provided.
		"""
		
		super().set_arguments(arguments)
	
	def set_attributes(self, attributes: BlinkAttributes):
		"""
		Clears existing and sets new browser attributes from a dictionary.

		Args:
			attributes (BlinkAttributes): A dictionary of attributes to set.
		"""
		
		super().set_attributes(attributes)
	
	def set_experimental_options(self, experimental_options: BlinkExperimentalOptions):
		"""
		Clears existing and sets new experimental options from a dictionary.

		Args:
			experimental_options (BlinkExperimentalOptions): A dictionary of experimental options to set.
		"""
		
		super().set_experimental_options(experimental_options)
	
	def set_flags(self, flags: BlinkFlags):
		"""
		Clears all existing flags and sets new ones, including Blink features.

		This method delegates to the parent `set_flags` method, allowing it to handle
		all flag types defined in this manager, including 'arguments', 'experimental_options',
		'attributes', and 'blink_features'.

		Args:
			flags (BlinkFlags): A dictionary where keys are flag types
				and values are dictionaries of flags to set for that type.
		"""
		
		super().set_flags(flags)
	
	@property
	def start_args(self) -> List[str]:
		"""
		Builds and returns a List of all command-line arguments for browser startup.

		Returns:
			List[str]: A List of startup arguments.
		"""
		
		args = []
		
		for type_name, type_functions in self._flags_types.items():
			args += type_functions.build_start_args_function()
		
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
	
	def update_arguments(self, arguments: BlinkArguments):
		"""
		Updates command-line arguments from a dictionary without clearing existing ones.

		Args:
			arguments (BlinkArguments): A dictionary of arguments to set or update.
		"""
		
		super().update_arguments(arguments)
	
	def update_attributes(self, attributes: BlinkAttributes):
		"""
		Updates browser attributes from a dictionary without clearing existing ones.

		Args:
			attributes (BlinkAttributes): A dictionary of attributes to set or update.
		"""
		
		super().update_attributes(attributes)
	
	def update_experimental_options(self, experimental_options: BlinkExperimentalOptions):
		"""
		Updates experimental options from a dictionary without clearing existing ones.

		Args:
			experimental_options (BlinkExperimentalOptions): A dictionary of experimental options to set or update.
		"""
		
		super().update_experimental_options(experimental_options)
	
	def update_flags(self, flags: BlinkFlags):
		"""
		Updates all flags, including Blink features, without clearing existing ones.

		This method delegates to the parent `update_flags` method, allowing it to handle
		all flag types defined in this manager, including 'arguments', 'experimental_options',
		'attributes', and 'blink_features'.

		Args:
			flags (BlinkFlags): A dictionary where keys are flag types
				and values are dictionaries of flags to update for that type.
		"""
		
		super().update_flags(flags)


BlinkArguments.model_rebuild()
BlinkExperimentalOptions.model_rebuild()
BlinkAttributes.model_rebuild()
BlinkFeatures.model_rebuild()
BlinkFlags.model_rebuild()
