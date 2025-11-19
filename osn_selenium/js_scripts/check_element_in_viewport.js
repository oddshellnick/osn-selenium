var element = arguments[0];

if (!element) {
    return false;
}

var rect = element.getBoundingClientRect();
var viewportWidth = window.innerWidth || document.documentElement.clientWidth;
var viewportHeight = window.innerHeight || document.documentElement.clientHeight;

var isVisible = (
  rect.top >= 0 &&
  rect.left >= 0 &&
  rect.bottom <= viewportHeight &&
  rect.right <= viewportWidth
);

return isVisible;