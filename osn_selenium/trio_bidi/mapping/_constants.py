from selenium.webdriver.common.by import By


__all__ = ["BY_MAPPING_DICT"]

BY_MAPPING_DICT = {
	By.CSS_SELECTOR: "css",
	By.ID: "css",
	By.XPATH: "xpath",
	By.LINK_TEXT: "linkText",
	By.PARTIAL_LINK_TEXT: "partialLinkText",
	By.TAG_NAME: "css",
	By.CLASS_NAME: "css"
}
