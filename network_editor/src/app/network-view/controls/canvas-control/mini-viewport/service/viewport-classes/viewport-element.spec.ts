import { ViewportElement } from "./viewport-element";

describe('ViewportElement', () => {
  let viewportElement: ViewportElement;

  beforeEach(() => {
    viewportElement = new ViewportElement(
      document.createElement('div'),
      document.createElement('div')
    )
  });

  describe('METHOD: updateElementStyles', () => {
    it('should set the element style according to the element bounds', () => {
      viewportElement['_bb'] = {
        w: 10,
        h: 10,
        x1: 10,
        x2: 0,
        y1: 10,
        y2: 0
      }

      viewportElement['updateElementStyles']();

      expect(viewportElement.element.style['left']).toBe(viewportElement['_bb'].x1 + 'px')
      expect(viewportElement.element.style['top']).toBe(viewportElement['_bb'].y1 + 'px')
      expect(viewportElement.element.style['width']).toBe(viewportElement['_bb'].w + 'px')
      expect(viewportElement.element.style['height']).toBe(viewportElement['_bb'].h + 'px')
    });
  });
});
