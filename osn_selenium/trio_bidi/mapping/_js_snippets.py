__all__ = ["CAPTURE", "NAVIGATION", "WEB_ELEMENT", "WINDOW"]


class WINDOW:
	"""
	JavaScript snippets for window-related operations.

	Attributes:
		SET_ORIENTATION (str): Snippet to lock screen orientation.
		GET_ORIENTATION (str): Snippet to retrieve the current screen orientation type.
	"""
	
	SET_ORIENTATION = "screen.orientation.lock('{orientation}')"
	GET_ORIENTATION = "screen.orientation.type"


class WEB_ELEMENT:
	"""
	JavaScript snippets for web element interactions with internal guards for W3C compatibility.

	Attributes:
		SEND_KEYS_TO (str): Snippet to focus and append text with input validation.
		IS_SELECTED (str): Snippet to check if an element is selectable and selected.
		IS_ENABLED (str): Snippet to check enablement state.
		GET_TEXT (str): Snippet to retrieve inner text.
		GET_TAG (str): Snippet to retrieve tag name.
		GET_SHADOW_ROOT (str): Snippet to retrieve shadow root with existence check.
		GET_RECT (str): Snippet to retrieve dimensions.
		GET_PROPERTY (str): Snippet to retrieve element property.
		GET_CSS (str): Snippet to retrieve CSS value.
		GET_ATTRIBUTE (str): Snippet to retrieve attribute.
		GET_ARIA_ROLE (str): Snippet to retrieve ARIA role.
		GET_ARIA_LABEL (str): Snippet to retrieve accessible label.
		CLICK (str): Snippet to perform click with interactability guards.
		CLEAR (str): Snippet to clear value with state guards.
	"""
	
	_GUARDS = """
	const guards = {
		stale: (el) => {
			if (!el.isConnected) throw new Error('stale element reference');
		},
		interactable: (el) => {
			const rects = el.getClientRects();
			const style = window.getComputedStyle(el);
			
			if (rects.length === 0 || style.visibility === 'hidden' || style.display === 'none') {
				throw new Error('element not interactable');
			}
		},
		state: (el) => {
			if (el.disabled || el.readOnly) throw new Error('invalid element state');
		},
		selectable: (el) => {
			const tag = el.tagName.toLowerCase();
			const type = (el.getAttribute('type') || '').toLowerCase();
			const canSelect = tag === 'option' || type === 'checkbox' || type === 'radio';
			
			if (!canSelect) throw new Error('element not selectable');
		},
		intercepted: (el) => {
			const rect = el.getBoundingClientRect();
			const x = rect.left + rect.width / 2;
			const y = rect.top + rect.height / 2;
			const topEl = document.elementFromPoint(x, y);
			
			if (topEl && topEl !== el && !el.contains(topEl)) {
				throw new Error('element click intercepted: Element is obscured by ' + topEl.tagName);
			}
		}
	};
	"""
	
	CLICK = f"""
function(el){{
	{_GUARDS}
	guards.stale(el);
	guards.interactable(el);
	guards.state(el);
	guards.intercepted(el);
	
	el.click();
}}
"""
	
	CLEAR = f"""
function(el){{
	{_GUARDS}
	guards.stale(el);
	guards.interactable(el);
	guards.state(el);
	
	el.value = '';
	
	el.dispatchEvent(new InputEvent('input', {{bubbles: true}}));
	el.dispatchEvent(new Event('change', {{bubbles: true}}));
}}
"""
	
	GET_ARIA_ROLE = f"""
function(el){{
	{_GUARDS}
	guards.stale(el);
	
	try {{
		return el.getAttribute && el.getAttribute('role');
	}} catch(e) {{
		return '';
	}}
}}
"""
	
	GET_ARIA_LABEL = f"""
function(el){{
	{_GUARDS}
	guards.stale(el);
	
	try {{
		var v = null;
		
		if (el.getAttribute) v = el.getAttribute('aria-label');
		if (!v) v = el.getAttribute && el.getAttribute('alt');
		
		if (!v) {{
			var txt = (el.textContent || '').trim();
			if (txt) v = txt;
		}}
		
		return v || '';
	}} catch(e) {{
		return '';
	}}
}}
"""
	
	GET_TEXT = f"""
function(el){{
	{_GUARDS}
	guards.stale(el);
	
	return el.innerText || '';
}}
"""
	
	GET_TAG = f"""
function(el){{
	{_GUARDS}
	guards.stale(el);
	
	return (el.tagName || '').toLowerCase();
}}
"""
	
	GET_RECT = f"""
function(el){{
	{_GUARDS}
	guards.stale(el);
	
	var r = el.getBoundingClientRect();
	
	return {{
		x: Number(r.x || r.left || 0),
		y: Number(r.y || r.top || 0),
		width: Number(r.width || 0),
		height: Number(r.height || 0)
	}};
}}
"""
	
	GET_SHADOW_ROOT = f"""
function(el){{
	{_GUARDS}
	guards.stale(el);
	
	const sr = el.shadowRoot;
	
	if (!sr) throw new Error('no such shadow root');
	
	return sr;
}}
"""
	
	IS_SELECTED = f"""
function(el){{
	{_GUARDS}
	guards.stale(el);
	guards.selectable(el);
	
	return Boolean(el.selected || el.checked);
}}
"""
	
	IS_ENABLED = f"""
function(el){{
	{_GUARDS}
	guards.stale(el);
	
	return !el.disabled;
}}
"""
	
	GET_PROPERTY = f"""
function(el, prop){{
	{_GUARDS}
	guards.stale(el);
	
	try {{
		return el[prop];
	}} catch(e) {{
		return null;
	}}
}}
"""
	
	GET_ATTRIBUTE = f"""
function(el, attr){{
	{_GUARDS}
	guards.stale(el);
	
	try {{
		return el.getAttribute(attr);
	}} catch(e) {{
		return null;
	}}
}}
"""
	
	GET_CSS = f"""
function(el, prop){{
	{_GUARDS}
	guards.stale(el);
	
	try {{
		return window.getComputedStyle(el).getPropertyValue(prop);
	}} catch(e) {{
		return null;
	}}
}}
"""
	
	SEND_KEYS_TO = f"""
function(el, text){{
	{_GUARDS}
	guards.stale(el);
	guards.interactable(el);
	guards.state(el);
	
	try {{
		el.focus();
		el.value = (el.value || '') + String(text || '');
		
		try {{
			el.dispatchEvent(new InputEvent('input', {{bubbles: true}}));
		}} catch(e) {{
			el.dispatchEvent(new Event('input', {{bubbles: true}}));
		}}
		
		try {{
			el.dispatchEvent(new Event('change', {{bubbles: true}}));
		}} catch(e) {{ }}
	}} catch (e) {{ }}
}}
"""


class NAVIGATION:
	"""
	JavaScript snippets for navigation and page information.

	Attributes:
		GET_TITLE (str): Snippet to retrieve the document title.
	"""
	
	GET_TITLE = "document.title"


class CAPTURE:
	"""
	JavaScript snippets for capturing page state.

	Attributes:
		GET_PAGE_SOURCE (str): Snippet to retrieve the full outer HTML of the document.
	"""
	
	GET_PAGE_SOURCE = "document.documentElement.outerHTML"
