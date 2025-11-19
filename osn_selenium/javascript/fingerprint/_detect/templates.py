__all__ = [
	"ARG_WRAPPER_LOGIC",
	"CALL_ORIGINAL_METHOD",
	"CALL_ORIGINAL_PROP",
	"DESCRIPTOR_LOOKUP_METHOD",
	"DESCRIPTOR_LOOKUP_PROP",
	"HOOK_IIFE_WRAPPER",
	"METADATA_PRESERVATION",
	"PART_ARG_WRAPPER",
	"PART_REPORT",
	"PART_SPOOF_METHOD",
	"PART_SPOOF_PROP",
	"REPORT_LOGIC",
	"TARGET_RESOLUTION",
	"WRAPPER_CONSTRUCTOR_SKELETON",
	"WRAPPER_METHOD_SKELETON",
	"WRAPPER_PROP_SKELETON"
]

HOOK_IIFE_WRAPPER = """
guard(
	() => {{
{hook_body}
	}}
);
""".strip("\n")

TARGET_RESOLUTION = """
const target = ({target_object}.prototype || {target_object});
let descriptor, current = target;

{descriptor_lookup}
""".strip("\n")

DESCRIPTOR_LOOKUP_METHOD = """
let original;
try {{ original = target['{method_name}']; }} catch(e) {{ return; }}

if (!original || typeof original !== 'function' || hookedRegistry.has(original)) return;
""".strip("\n")

DESCRIPTOR_LOOKUP_PROP = """
while (current && !descriptor) {{
	descriptor = Object.getOwnPropertyDescriptor(current, '{prop_name}');
	current = Object.getPrototypeOf(current);
}}

if (!descriptor || !descriptor.get || hookedRegistry.has(descriptor.get)) return;

const originalGet = descriptor.get;
""".strip("\n")

WRAPPER_METHOD_SKELETON = """
const wrapper = function(...args) {{
{wrapper_body}

	return result;
}};

hookedRegistry.add(wrapper);
hookedRegistry.add(original);

target['{method_name}'] = wrapper;
""".strip("\n")

WRAPPER_PROP_SKELETON = """
const wrapperGet = function() {{
{wrapper_body}

	return result;
}};

hookedRegistry.add(wrapperGet);
hookedRegistry.add(originalGet);

Object.defineProperty(
	target,
	'{prop_name}',
	{{
		...descriptor,
		get: wrapperGet
	}}
);
""".strip("\n")

WRAPPER_CONSTRUCTOR_SKELETON = """
if (hookedRegistry.has(originalClass)) return;

const handler = {{
	construct(target, args) {{
{wrapper_body}

		return new target(...args);
	}}
}};

try {{
	const wrapped = new Proxy(originalClass, handler);
	window['{class_name}'] = wrapped;
	hookedRegistry.add(wrapped);
}} catch (e) {{}}
""".strip("\n")

METADATA_PRESERVATION = """
try {{ Object.defineProperty(wrapper, 'name', {{ value: '{method_name}' }}); }} catch (e) {{}}
try {{ Object.defineProperty(wrapper, 'toString', {{ value: () => original.toString() }}); }} catch (e) {{}}
""".strip("\n")

CALL_ORIGINAL_METHOD = "let result; try { result = original.apply(this, args); } catch(e) {}"
CALL_ORIGINAL_PROP = "let result; try { result = originalGet.call(this); } catch(e) {}"

PART_REPORT = "{report_logic}"
PART_ARG_WRAPPER = "{arg_wrapper_logic}"
PART_SPOOF_METHOD = "if (MODIFIERS['{path}']) {{ result = MODIFIERS['{path}'](result, args); }}"
PART_SPOOF_PROP = "if (MODIFIERS['{path}']) {{ result = MODIFIERS['{path}'](result); }}"

REPORT_LOGIC = "Reporter.send('{api}', '{target}', '{name}');"

ARG_WRAPPER_LOGIC = """
if (typeof args[{index}] === 'function') {{
	const origCb = args[{index}];

	args[{index}] = function(...cbArgs) {{
		Reporter.send('{api}', '{name}_cb');
		return origCb.apply(this, cbArgs);
	}};
}}
""".strip("\n")
