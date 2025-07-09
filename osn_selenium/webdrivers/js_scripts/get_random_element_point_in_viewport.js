function get_random_point_in_element_shape_grid(targetElement, step) {
    try {
        const rect = targetElement.getBoundingClientRect();

        if (rect.width <= 0 || rect.height <= 0) {
            return null;
        }

        const points = [];

        for (let xOffset = 0; xOffset < rect.width; xOffset += step) {
            for (let yOffset = 0; yOffset < rect.height; yOffset += step) {
                points.push(
                    {
                        viewportX: Math.floor(rect.left + xOffset),
                        viewportY: Math.floor(rect.top + yOffset),
                        elementOffsetX: xOffset,
                        elementOffsetY: yOffset
                    }
                );
            }
        }

        if (points.length === 0) {
             const centerX = rect.left + rect.width / 2;
             const centerY = rect.top + rect.height / 2;

             const hitElement = document.elementFromPoint(Math.floor(centerX), Math.floor(centerY));

             if (hitElement && (hitElement === targetElement || targetElement.contains(hitElement))) {
                  return { x: rect.width / 2, y: rect.height / 2 };
             }

             return null;
        }

        for (let i = points.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [points[i], points[j]] = [points[j], points[i]];
        }

        for (const point of points) {
            const hitElement = document.elementFromPoint(point.viewportX, point.viewportY);

            if (hitElement && (hitElement === targetElement || targetElement.contains(hitElement))) {
                return {
                    x: point.elementOffsetX,
                    y: point.elementOffsetY
                };
            }
        }

        return null;
    } catch (error) {
        return null;
    }
}

return get_random_point_in_element_shape_grid(arguments[0], arguments[1]);