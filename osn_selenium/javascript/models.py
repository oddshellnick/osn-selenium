from osn_selenium._base_models import DictModel


__all__ = ["JS_Scripts"]


class JS_Scripts(DictModel):
	"""
	Represents a collection of JavaScript script snippets for use with WebDriver.

	Attributes:
		check_element_in_viewport (str): JS to check if element is in the viewport.
		get_document_scroll_size (str): JS to get total scrollable dimensions.
		get_element_css (str): JS to get computed CSS styles of an element.
		get_element_rect_in_viewport (str): JS to get element bounds in viewport.
		get_random_element_point_in_viewport (str): JS to get a random visible point in element.
		get_viewport_position (str): JS to get scroll position of viewport.
		get_viewport_rect (str): JS to get viewport scroll offset and dimensions.
		get_viewport_size (str): JS to get dimensions of the viewport.
		open_new_tab (str): JS to open a new tab.
		start_fingerprint_detection (str): JS to initialize fingerprint detection hooks.
		stop_window_loading (str): JS to stop the page from loading.
	"""
	
	check_element_in_viewport: str
	get_document_scroll_size: str
	get_element_css: str
	get_element_rect_in_viewport: str
	get_random_element_point_in_viewport: str
	get_viewport_position: str
	get_viewport_rect: str
	get_viewport_size: str
	open_new_tab: str
	start_fingerprint_detection: str
	stop_window_loading: str
