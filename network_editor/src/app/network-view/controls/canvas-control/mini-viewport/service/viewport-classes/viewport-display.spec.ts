import { fakeAsync, tick } from "@angular/core/testing";
import { ViewportDisplay } from "./viewport-display";

describe('ViewportDisplay', () => {
  let display: ViewportDisplay

  let parentElement;

  beforeEach(() => {
    parentElement = document.createElement('img');
    parentElement.setAttribute('class', 'test-element');
    parentElement.style['width'] = '600px';
    parentElement.style['height'] = '300px';
    parentElement.style['border'] = '1px solid red';
    parentElement.style['position'] = 'fixed';
    // add parent element to page for testing
    document.body.appendChild(parentElement);

    display = new ViewportDisplay(
      document.createElement('div'),
      parentElement
    )
  });

  afterEach(() => {
    document.body.removeChild(parentElement);
  });

  describe('METHOD: updateImage', () => {
    it('should remove the source if no image is provded', fakeAsync(() => {
      display.updateImage(null);
      tick(100);
      expect(display.element.hasAttribute('src')).toBeFalsy();
    }));

    it('should set the source if there is an image', fakeAsync(() => {
      display.updateImage('data:image/png;');
      tick(100);
      expect(display.element.hasAttribute('src')).toBeTruthy();
    }));
  });

  describe('METHOD: handleImageLoad', () => {
    it('should update the display bounding box', () => {
      const expectedBB = {
        w: 200,
        h: 200,
        x1: 200,
        x2: 400,
        y1: 50,
        y2: 250
      }

      display['handleImageLoad'](200, 200);
      expect(display.bb.w).toBe(expectedBB.w);
      expect(display.bb.h).toBe(expectedBB.h);
      expect(display.bb.x1).toBe(expectedBB.x1);
      expect(display.bb.x2).toBe(expectedBB.x2);
      expect(display.bb.y1).toBe(expectedBB.y1);
      expect(display.bb.y2).toBe(expectedBB.y2);
    });
  });
});
