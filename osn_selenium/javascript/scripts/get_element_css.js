var items = {};
var computedStyle = getComputedStyle(arguments[0]);
for (var i = 0; i < computedStyle.length; i++) {
    items[computedStyle[i]] = computedStyle.getPropertyValue(computedStyle[i]);
}
return items;