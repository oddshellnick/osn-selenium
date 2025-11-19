from typing import Dict
from osn_selenium.javascript.fingerprint.registry.models import RegistryItem
from osn_selenium.javascript.fingerprint.registry._utils import (
	MATCH_MEDIA_SETTINGS,
	WRAP_ARG_0
)
from osn_selenium.javascript.fingerprint.registry._core_functions import (
	register_key_methods,
	register_keys_methods,
	register_target_methods,
	register_targets,
	register_targets_methods
)


__all__ = [
	"create_registry",
	"register_advanced_web_apis",
	"register_audio",
	"register_browser_environment",
	"register_dom_layout",
	"register_fonts",
	"register_graphics_rendering",
	"register_hardware_sensors",
	"register_intl",
	"register_media_devices",
	"register_media_elements",
	"register_navigator_identity",
	"register_network",
	"register_screen_properties",
	"register_storage",
	"register_system_utils",
	"register_touch_events"
]


def register_browser_environment(registry: Dict[str, RegistryItem]) -> Dict[str, RegistryItem]:
	"""
	Registers general browser environment APIs.

	Args:
		registry (Dict[str, RegistryItem]): The registry to update.

	Returns:
		Dict[str, RegistryItem]: The updated registry.
	"""
	
	registry = register_key_methods(
			registry=registry,
			key="SpeechSynthesis",
			target="window.speechSynthesis",
			type_="method",
			api="speech",
			methods=["getVoices", "speak"]
	)
	registry = register_key_methods(
			registry=registry,
			key="CredentialsContainer",
			target="window.navigator.credentials",
			type_="method",
			api="auth",
			methods=["create", "get", "store", "preventSilentAccess"]
	)
	registry = register_key_methods(
			registry=registry,
			key="History",
			target="window.history",
			type_="prop",
			api="history",
			methods=["length", "scrollRestoration", "state"]
	)
	registry = register_key_methods(
			registry=registry,
			key="Notification",
			target="window.Notification",
			type_="prop",
			api="notification",
			methods=["permission", "maxActions"]
	)
	registry = register_key_methods(
			registry=registry,
			key="Chrome",
			target="window.chrome",
			type_="prop",
			api="browser_specific",
			methods=["runtime", "loadTimes", "csi"]
	)
	registry = register_key_methods(
			registry=registry,
			key="IdleDetector",
			target="window.IdleDetector",
			type_="method",
			api="idle",
			methods=["requestPermission"]
	)
	
	registry = register_keys_methods(
			registry=registry,
			keys={
				"LocationBar": "window.locationbar",
				"MenuBar": "window.menubar",
				"PersonalBar": "window.personalbar",
				"ScrollBars": "window.scrollbars",
				"StatusBar": "window.statusbar",
				"ToolBar": "window.toolbar",
			},
			type_="prop",
			api="ui_bars",
			methods=["visible"]
	)
	
	return registry


def register_advanced_web_apis(registry: Dict[str, RegistryItem]) -> Dict[str, RegistryItem]:
	"""
	Registers advanced Web APIs like ServiceWorkers and WebXR.

	Args:
		registry (Dict[str, RegistryItem]): The registry to update.

	Returns:
		Dict[str, RegistryItem]: The updated registry.
	"""
	
	registry = register_key_methods(
			registry=registry,
			key="ServiceWorkerContainer",
			target="window.navigator.serviceWorker",
			type_="method",
			api="service_worker",
			methods=["register", "getRegistration", "getRegistrations"]
	)
	registry = register_key_methods(
			registry=registry,
			key="CacheStorage",
			target="window.caches",
			type_="method",
			api="cache_api",
			methods=["has", "open", "match", "keys"]
	)
	registry = register_key_methods(
			registry=registry,
			key="XRSystem",
			target="window.navigator.xr",
			type_="method",
			api="webxr",
			methods=["isSessionSupported", "requestSession"]
	)
	
	return registry


def register_media_elements(registry: Dict[str, RegistryItem]) -> Dict[str, RegistryItem]:
	"""
	Registers media element APIs (Audio/Video).

	Args:
		registry (Dict[str, RegistryItem]): The registry to update.

	Returns:
		Dict[str, RegistryItem]: The updated registry.
	"""
	
	registry = register_targets_methods(
			registry=registry,
			targets=["HTMLMediaElement", "HTMLAudioElement", "HTMLVideoElement"],
			type_="method",
			api="media_element",
			methods=["canPlayType"]
	)
	
	return registry


def register_media_devices(registry: Dict[str, RegistryItem]) -> Dict[str, RegistryItem]:
	"""
	Registers media device APIs like Microphones and Cameras.

	Args:
		registry (Dict[str, RegistryItem]): The registry to update.

	Returns:
		Dict[str, RegistryItem]: The updated registry.
	"""
	
	registry = register_key_methods(
			registry=registry,
			key="MediaDevices",
			target="window.navigator.mediaDevices",
			type_="method",
			api="media_devices",
			methods=["enumerateDevices", "getUserMedia"]
	)
	registry = register_key_methods(
			registry=registry,
			key="MediaCapabilities",
			target="window.navigator.mediaCapabilities",
			type_="method",
			api="media_capabilities",
			methods=["decodingInfo", "encodingInfo"]
	)
	registry = register_key_methods(
			registry=registry,
			key="MediaSession",
			target="window.navigator.mediaSession",
			type_="method",
			api="media_session",
			methods=["setActionHandler"]
	)
	
	return registry


def register_intl(registry: Dict[str, RegistryItem]) -> Dict[str, RegistryItem]:
	"""
	Registers Internationalization API methods.

	Args:
		registry (Dict[str, RegistryItem]): The registry to update.

	Returns:
		Dict[str, RegistryItem]: The updated registry.
	"""
	
	registry = register_targets_methods(
			registry=registry,
			targets=[
				"Intl.Collator",
				"Intl.NumberFormat",
				"Intl.DateTimeFormat",
				"Intl.ListFormat",
				"Intl.PluralRules",
				"Intl.RelativeTimeFormat"
			],
			type_="method",
			api="intl",
			methods=["supportedLocalesOf", "resolvedOptions"]
	)
	
	return registry


def register_system_utils(registry: Dict[str, RegistryItem]) -> Dict[str, RegistryItem]:
	"""
	Registers system utility APIs like Date, Performance, and Math.

	Args:
		registry (Dict[str, RegistryItem]): The registry to update.

	Returns:
		Dict[str, RegistryItem]: The updated registry.
	"""
	
	registry = register_target_methods(
			registry=registry,
			target="Date",
			type_="method",
			api="time",
			methods=["now", "getTime", "getTimezoneOffset"]
	)
	registry = register_target_methods(
			registry=registry,
			target="Performance",
			type_="method",
			api="performance",
			methods=["now", "getEntriesByType", "timeOrigin"]
	)
	registry = register_target_methods(
			registry=registry,
			target="Math",
			type_="method",
			api="math",
			methods=[
				"sin",
				"cos",
				"tan",
				"acos",
				"asin",
				"atan",
				"pow",
				"sqrt",
				"random",
				"hypot"
			]
	)
	registry = register_target_methods(
			registry=registry,
			target="WebAssembly",
			type_="method",
			api="wasm",
			methods=["instantiate", "compile", "validate"]
	)
	registry = register_target_methods(
			registry=registry,
			target="Navigator",
			type_="method",
			api="drm",
			methods=["requestMediaKeySystemAccess"]
	)
	
	registry = register_key_methods(
			registry=registry,
			key="Permissions",
			target="window.navigator.permissions",
			type_="method",
			api="permissions",
			methods=["query"]
	)
	registry = register_key_methods(
			registry=registry,
			key="Clipboard",
			target="window.navigator.clipboard",
			type_="method",
			api="clipboard",
			methods=["readText", "writeText"]
	)
	registry = register_key_methods(
			registry=registry,
			key="PerformanceMemory",
			target="performance.memory",
			type_="prop",
			api="performance",
			methods=["jsHeapSizeLimit", "totalJSHeapSize", "usedJSHeapSize"]
	)
	
	registry = register_targets(
			registry=registry,
			targets=[
				"ResizeObserver",
				"IntersectionObserver",
				"PerformanceObserver",
				"MutationObserver"
			],
			type_="constructor",
			api="observer",
			settings=WRAP_ARG_0
	)
	
	registry = register_target_methods(
			registry=registry,
			target="Error",
			type_="prop",
			api="error",
			methods=["stack"]
	)
	registry = register_target_methods(
			registry=registry,
			target="Error",
			type_="method",
			api="error",
			methods=["toString"]
	)
	
	return registry


def register_storage(registry: Dict[str, RegistryItem]) -> Dict[str, RegistryItem]:
	"""
	Registers storage APIs like IndexedDB and LocalStorage.

	Args:
		registry (Dict[str, RegistryItem]): The registry to update.

	Returns:
		Dict[str, RegistryItem]: The updated registry.
	"""
	
	registry = register_key_methods(
			registry=registry,
			key="IndexedDB",
			target="window.indexedDB",
			type_="method",
			api="indexedDB",
			methods=["open", "cmp", "deleteDatabase"]
	)
	registry = register_key_methods(
			registry=registry,
			key="StorageManager",
			target="window.navigator.storage",
			type_="method",
			api="storage",
			methods=["estimate", "persist"]
	)
	registry = register_keys_methods(
			registry=registry,
			keys={
				"LocalStorage": "window.localStorage",
				"SessionStorage": "window.sessionStorage"
			},
			type_="method",
			api="storage",
			methods=["getItem", "setItem", "removeItem", "clear"]
	)
	
	return registry


def register_network(registry: Dict[str, RegistryItem]) -> Dict[str, RegistryItem]:
	"""
	Registers network and WebRTC related APIs.

	Args:
		registry (Dict[str, RegistryItem]): The registry to update.

	Returns:
		Dict[str, RegistryItem]: The updated registry.
	"""
	
	registry = register_key_methods(
			registry=registry,
			key="Window",
			target="window",
			type_="method",
			api="network",
			methods=["fetch"]
	)
	registry = register_key_methods(
			registry=registry,
			key="XMLHttpRequest",
			target="window.XMLHttpRequest",
			type_="method",
			api="network",
			methods=["open", "send", "setRequestHeader"]
	)
	registry = register_key_methods(
			registry=registry,
			key="RTCPeerConnection",
			target="window.RTCPeerConnection",
			type_="method",
			api="webrtc",
			methods=[
				"createOffer",
				"createAnswer",
				"setLocalDescription",
				"setRemoteDescription",
				"createDataChannel",
				"addIceCandidate"
			]
	)
	registry = register_key_methods(
			registry=registry,
			key="NetworkInformation",
			target="window.navigator.connection",
			type_="prop",
			api="network_info",
			methods=["downlink", "effectiveType", "rtt", "saveData", "type"]
	)
	
	return registry


def register_touch_events(registry: Dict[str, RegistryItem]) -> Dict[str, RegistryItem]:
	"""
	Registers touch-related API events.

	Args:
		registry (Dict[str, RegistryItem]): The registry to update.

	Returns:
		Dict[str, RegistryItem]: The updated registry.
	"""
	
	registry = register_target_methods(
			registry=registry,
			target="Document",
			type_="method",
			api="touch",
			methods=["createTouch", "createTouchList"]
	)
	
	return registry


def register_hardware_sensors(registry: Dict[str, RegistryItem]) -> Dict[str, RegistryItem]:
	"""
	Registers hardware sensor APIs like Battery, Bluetooth, and Geolocation.

	Args:
		registry (Dict[str, RegistryItem]): The registry to update.

	Returns:
		Dict[str, RegistryItem]: The updated registry.
	"""
	
	registry = register_key_methods(
			registry=registry,
			key="Battery",
			target="Navigator",
			type_="method",
			api="battery",
			methods=["getBattery"]
	)
	registry = register_key_methods(
			registry=registry,
			key="Gamepads",
			target="Navigator",
			type_="method",
			api="gamepad",
			methods=["getGamepads"]
	)
	registry = register_key_methods(
			registry=registry,
			key="Geolocation",
			target="window.navigator.geolocation",
			type_="method",
			api="geolocation",
			methods=["getCurrentPosition", "watchPosition"],
			settings=WRAP_ARG_0
	)
	registry = register_key_methods(
			registry=registry,
			key="Bluetooth",
			target="window.navigator.bluetooth",
			type_="method",
			api="bluetooth",
			methods=["requestDevice", "getAvailability"]
	)
	registry = register_key_methods(
			registry=registry,
			key="USB",
			target="window.navigator.usb",
			type_="method",
			api="usb",
			methods=["requestDevice", "getDevices"]
	)
	registry = register_key_methods(
			registry=registry,
			key="Keyboard",
			target="window.navigator.keyboard",
			type_="method",
			api="keyboard",
			methods=["getLayoutMap", "lock", "unlock"]
	)
	
	return registry


def register_navigator_identity(registry: Dict[str, RegistryItem]) -> Dict[str, RegistryItem]:
	"""
	Registers browser identity properties in the Navigator object.

	Args:
		registry (Dict[str, RegistryItem]): The registry to update.

	Returns:
		Dict[str, RegistryItem]: The updated registry.
	"""
	
	registry = register_target_methods(
			registry=registry,
			target="Navigator",
			type_="prop",
			api="navigator",
			methods=[
				"userAgent",
				"appName",
				"appVersion",
				"appCodeName",
				"language",
				"languages",
				"platform",
				"cookieEnabled",
				"product",
				"productSub",
				"vendor",
				"vendorSub",
				"hardwareConcurrency",
				"deviceMemory",
				"maxTouchPoints",
				"webdriver",
				"doNotTrack",
				"oscpu",
				"plugins",
				"mimeTypes",
				"pdfViewerEnabled"
			]
	)
	registry = register_target_methods(
			registry=registry,
			target="Navigator",
			type_="method",
			api="navigator",
			methods=["registerProtocolHandler", "javaEnabled", "vibrate", "sendBeacon"]
	)
	
	return registry


def register_fonts(registry: Dict[str, RegistryItem]) -> Dict[str, RegistryItem]:
	"""
	Registers font loading APIs.

	Args:
		registry (Dict[str, RegistryItem]): The registry to update.

	Returns:
		Dict[str, RegistryItem]: The updated registry.
	"""
	
	registry = register_key_methods(
			registry=registry,
			key="FontFaceSet",
			target="document.fonts",
			type_="method",
			api="fonts",
			methods=["load", "check"]
	)
	
	return registry


def register_dom_layout(registry: Dict[str, RegistryItem]) -> Dict[str, RegistryItem]:
	"""
	Registers DOM layout and positioning APIs.

	Args:
		registry (Dict[str, RegistryItem]): The registry to update.

	Returns:
		Dict[str, RegistryItem]: The updated registry.
	"""
	
	registry = register_targets_methods(
			registry=registry,
			targets=["HTMLElement", "Element"],
			type_="method",
			api="layout",
			methods=["getBoundingClientRect", "getClientRects"]
	)
	
	registry = register_target_methods(
			registry=registry,
			target="HTMLElement",
			type_="prop",
			api="layout",
			methods=[
				"offsetWidth",
				"offsetHeight",
				"offsetLeft",
				"offsetTop",
				"clientWidth",
				"clientHeight",
				"scrollWidth",
				"scrollHeight"
			]
	)
	
	registry = register_key_methods(
			registry=registry,
			key="Window",
			target="window",
			type_="method",
			api="css",
			methods=["getComputedStyle"]
	)
	
	return registry


def register_screen_properties(registry: Dict[str, RegistryItem]) -> Dict[str, RegistryItem]:
	"""
	Registers screen and viewport related APIs.

	Args:
		registry (Dict[str, RegistryItem]): The registry to update.

	Returns:
		Dict[str, RegistryItem]: The updated registry.
	"""
	
	registry = register_target_methods(
			registry=registry,
			target="Screen",
			type_="prop",
			api="screen",
			methods=[
				"width",
				"height",
				"availWidth",
				"availHeight",
				"colorDepth",
				"pixelDepth",
				"orientation",
				"availTop",
				"availLeft",
				"isExtended"
			]
	)
	
	registry = register_key_methods(
			registry=registry,
			key="ScreenOrientation",
			target="window.screen.orientation",
			type_="prop",
			api="screen",
			methods=["type", "angle"]
	)
	registry = register_key_methods(
			registry=registry,
			key="Window",
			target="window",
			type_="prop",
			api="screen",
			methods=["devicePixelRatio"]
	)
	registry = register_key_methods(
			registry=registry,
			key="Window",
			target="window",
			type_="method",
			api="mediaQuery",
			methods=["matchMedia"],
			settings=MATCH_MEDIA_SETTINGS
	)
	registry = register_key_methods(
			registry=registry,
			key="Window",
			target="window",
			type_="prop",
			api="layout",
			methods=[
				"innerWidth",
				"innerHeight",
				"outerWidth",
				"outerHeight",
				"screenX",
				"screenY"
			]
	)
	registry = register_key_methods(
			registry=registry,
			key="VisualViewport",
			target="window.visualViewport",
			type_="prop",
			api="screen",
			methods=[
				"scale",
				"width",
				"height",
				"offsetLeft",
				"offsetTop",
				"pageLeft",
				"pageTop"
			]
	)
	
	return registry


def register_audio(registry: Dict[str, RegistryItem]) -> Dict[str, RegistryItem]:
	"""
	Registers AudioContext and related audio processing APIs.

	Args:
		registry (Dict[str, RegistryItem]): The registry to update.

	Returns:
		Dict[str, RegistryItem]: The updated registry.
	"""
	
	targets = [
		"AudioContext",
		"OfflineAudioContext",
		"BaseAudioContext",
		"webkitAudioContext"
	]
	
	registry = register_targets_methods(
			registry=registry,
			targets=targets,
			type_="method",
			api="audio_context",
			methods=[
				"createOscillator",
				"createAnalyser",
				"createDynamicsCompressor",
				"createScriptProcessor",
				"createMediaElementSource",
				"createMediaStreamSource",
				"decodeAudioData",
				"startRendering",
				"createBuffer",
				"createBufferSource",
				"createGain",
				"createBiquadFilter"
			]
	)
	registry = register_targets_methods(
			registry=registry,
			targets=targets,
			type_="prop",
			api="audio_context",
			methods=["sampleRate", "baseLatency", "outputLatency", "state", "destination"]
	)
	
	return registry


def register_graphics_rendering(registry: Dict[str, RegistryItem]) -> Dict[str, RegistryItem]:
	"""
	Registers graphics APIs including Canvas, WebGL, and SVG.

	Args:
		registry (Dict[str, RegistryItem]): The registry to update.

	Returns:
		Dict[str, RegistryItem]: The updated registry.
	"""
	
	registry = register_target_methods(
			registry=registry,
			target="HTMLCanvasElement",
			type_="method",
			api="canvas",
			methods=["toDataURL", "toBlob", "getContext"]
	)
	registry = register_target_methods(
			registry=registry,
			target="SVGGraphicsElement",
			type_="method",
			api="svg",
			methods=["getBBox"]
	)
	registry = register_target_methods(
			registry=registry,
			target="SVGTextContentElement",
			type_="method",
			api="svg",
			methods=[
				"getComputedTextLength",
				"getSubStringLength",
				"getStartPositionOfChar"
			]
	)
	
	registry = register_key_methods(
			registry=registry,
			key="CanvasRenderingContext2D",
			target="window.CanvasRenderingContext2D",
			type_="method",
			api="canvas",
			methods=[
				"getImageData",
				"measureText",
				"isPointInPath",
				"fillText",
				"strokeText",
				"createLinearGradient",
				"createRadialGradient"
			]
	)
	registry = register_key_methods(
			registry=registry,
			key="CanvasRenderingContext2D",
			target="window.CanvasRenderingContext2D",
			type_="prop",
			api="canvas",
			methods=["globalCompositeOperation", "font"]
	)
	
	registry = register_keys_methods(
			registry=registry,
			keys={
				"WebGLRenderingContext": "window.WebGLRenderingContext",
				"WebGL2RenderingContext": "window.WebGL2RenderingContext"
			},
			type_="method",
			api="webgl",
			methods=[
				"getParameter",
				"getExtension",
				"getSupportedExtensions",
				"readPixels",
				"compileShader",
				"linkProgram",
				"getShaderPrecisionFormat",
				"getContextAttributes",
				"checkFramebufferStatus",
				"clear",
				"drawArrays"
			]
	)
	registry = register_key_methods(
			registry=registry,
			key="GPU",
			target="window.navigator.gpu",
			type_="method",
			api="webgpu",
			methods=["requestAdapter", "getPreferredCanvasFormat"]
	)
	
	return registry


def create_registry() -> Dict[str, RegistryItem]:
	"""
	Creates and populates the complete fingerprint registry with all supported APIs.

	Returns:
		Dict[str, RegistryItem]: A dictionary mapping unique keys to registry items.
	"""
	
	registry = {}
	
	registry = register_graphics_rendering(registry=registry)
	registry = register_audio(registry=registry)
	registry = register_screen_properties(registry=registry)
	registry = register_dom_layout(registry=registry)
	registry = register_fonts(registry=registry)
	registry = register_navigator_identity(registry=registry)
	registry = register_hardware_sensors(registry=registry)
	registry = register_touch_events(registry=registry)
	registry = register_network(registry=registry)
	registry = register_storage(registry=registry)
	registry = register_system_utils(registry=registry)
	registry = register_intl(registry=registry)
	registry = register_media_devices(registry=registry)
	registry = register_media_elements(registry=registry)
	registry = register_advanced_web_apis(registry=registry)
	registry = register_browser_environment(registry=registry)
	
	return registry
