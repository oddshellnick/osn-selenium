var element = arguments[0];
var rect = element.getBoundingClientRect();

return {
    x: rect.x,
    y: rect.y,
    width: rect.width,
    height: rect.height
};