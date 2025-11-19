__all__ = [
	"ABSOLUTE_FREQUENCY",
	"ARRAY_CHANNEL_BLOCK",
	"ARRAY_GLOBAL_BLOCK",
	"ARRAY_LOOP_WRAPPER",
	"CUSTOM_RULE",
	"INDEX_CALCULATION_PERIODIC",
	"INDEX_CALCULATION_RAW",
	"INDEX_INCLUSION_LIST_CHECK",
	"INDEX_INCLUSION_SINGLE_CHECK",
	"PERSISTED_RANDOM_ITEM_NOISE",
	"PERSISTED_RANDOM_ITEM_SET",
	"PERSISTENCE_CHECK_NOISE",
	"PERSISTENCE_CHECK_RETURN",
	"PERSISTENCE_SAVE_NOISE",
	"PERSISTENCE_SAVE_RESULT",
	"RANDOM_ITEM_NOISE",
	"RANDOM_ITEM_SET",
	"STATIC_ITEM_NOISE",
	"STATIC_ITEM_SET",
	"VARIABLE_FREQUENCY"
]

CUSTOM_RULE = """
(originalValue, args) => {{
	{custom_javascript_code}
}}
""".strip("\n")

STATIC_ITEM_SET = """
(originalValue) => {{
	return {result_value};
}}
""".strip("\n")

STATIC_ITEM_NOISE = """
(originalValue) => {{
	return {math_expression};
}}
""".strip("\n")

RANDOM_ITEM_SET = """
(originalValue) => {{
	const randomResult = {calculation_expression};

	return randomResult;
}}
""".strip("\n")

PERSISTED_RANDOM_ITEM_SET = """
(originalValue) => {{
{persistence_check_code}
	const randomResult = {calculation_expression};
	{persistence_save_code}

	return randomResult;
}}
""".strip("\n")

RANDOM_ITEM_NOISE = """
(originalValue) => {{
	const noiseValue = {calculation_expression};

	return {math_expression};
}}
""".strip("\n")

PERSISTED_RANDOM_ITEM_NOISE = """
(originalValue) => {{
{persistence_check_code}
	const noiseValue = {calculation_expression};
	{persistence_save_code}

	return {math_expression};
}}
""".strip("\n")

PERSISTENCE_CHECK_RETURN = """
if (STORAGE.has('{storage_key}')) {{
	return STORAGE.get('{storage_key}');
}}
""".strip("\n")
PERSISTENCE_SAVE_RESULT = "STORAGE.set('{storage_key}', randomResult);"

PERSISTENCE_CHECK_NOISE = """
if (STORAGE.has('{storage_key}')) {{
	const noiseValue = STORAGE.get('{storage_key}');

	return {math_expression_with_noise};
}}
""".strip("\n")
PERSISTENCE_SAVE_NOISE = "STORAGE.set('{storage_key}', noiseValue);"

ARRAY_LOOP_WRAPPER = """
(originalObject) => {{
	const dataArray = originalObject.data || originalObject;

	for (let i = 0; i < dataArray.length; i++) {{
		const indexInCycle = {index_calculation};

{loop_body_logic}
	}}

	return originalObject;
}}
""".strip("\n")

ARRAY_CHANNEL_BLOCK = """
if (indexInCycle === {target_index}) {{
{frequency_logic}

	continue;
}}
""".strip("\n")

ARRAY_GLOBAL_BLOCK = """
if ({index_inclusion_check}) {{
{frequency_logic}
}}
""".strip("\n")

INDEX_CALCULATION_RAW = "i"
INDEX_CALCULATION_PERIODIC = "i % {cycle_length}"

VARIABLE_FREQUENCY = """
if (Math.random() <= {frequency}) {{
	dataArray[i] = {assignment_expression};
}}
""".strip("\n")

ABSOLUTE_FREQUENCY = "dataArray[i] = {assignment_expression};"

INDEX_INCLUSION_LIST_CHECK = "[{index_list}].includes(indexInCycle)"
INDEX_INCLUSION_SINGLE_CHECK = "indexInCycle === {channel_index}"
