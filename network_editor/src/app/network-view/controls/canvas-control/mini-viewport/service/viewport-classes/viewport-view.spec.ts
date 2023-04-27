import { ViewportDisplay } from "./viewport-display";
import { ViewportView } from "./viewport-view";

describe('ViewportView', () => {
  let viewportView: ViewportView;

  let parentEl: HTMLElement;
  let display: ViewportDisplay;

  beforeEach(() => {
    parentEl = document.createElement('div');
    parentEl.setAttribute('class', 'test-element');
    parentEl.style['width'] = '600px';
    parentEl.style['height'] = '300px';
    parentEl.style['left'] = '10px';
    parentEl.style['top'] = '10px';
    parentEl.style['border'] = '1px solid red';
    parentEl.style['position'] = 'fixed';
    // add parent element to page for testing
    document.body.appendChild(parentEl);

    display = new ViewportDisplay(
      document.createElement('img'),
      parentEl
    )

    viewportView = new ViewportView(
      document.createElement('div'),
      parentEl,
      display.element,
      0
    )
  });

  afterEach(() => {
    document.body.removeChild(parentEl);
  });

  describe('METHOD: updateViewPosition', () => {
    it('should hide the element if there are no bounds to show', () => {
      spyOn<any>(viewportView, 'calculateViewBounds').and.callFake(() => null);

      viewportView.updateViewPosition(null, null);
      expect(viewportView.element.style['display']).toBe('none');
    });

    it('should update the style of the view so that it can be seen on screen', () => {
      const updateElSpy = spyOn<any>(viewportView, 'updateElementStyles');
      spyOn<any>(viewportView, 'calculateViewBounds').and.callFake(() => {
        return { bb: {} }
      });

      viewportView.updateViewPosition({ bb: {} } as any, { bb: {} } as any);

      expect(viewportView.element.style['display']).toBe('flex');
      expect(updateElSpy).toHaveBeenCalled();
    });
  });

  describe('METHOD: isEmptyBounds', () => {
    it('should return true if the bounding box has height or width', () => {
      expect(viewportView['isEmptyBounds']({
        x1: 0, x2: 10, y1: 0, y2: 10, w: 10, h: 10
      })).toBeFalsy();
    });

    it('should return false if the bounding box has no height or width', () => {
      expect(viewportView['isEmptyBounds']({
        x1: 0, x2: 0, y1: 0, y2: 0, w: 0, h: 0
      })).toBeTruthy();
    });
  });

  describe('METHOD: isNotOnScreen', () => {
    it('should return true if the graph bounds is within the current view', () => {
      expect(
        viewportView['isNotOnScreen'](
          { x1: 10, x2: 20, y1: 10, y2: 20, w: 10, h: 10 },
          { x1: 0, x2: 30, y1: 0, y2: 30, w: 30, h: 30 }
        )
      ).toBeFalsy();
    });

    it('should return true if the graph bounds is within the current view but at the edge on the left', () => {
      expect(
        viewportView['isNotOnScreen'](
          { x1: 0, x2: 10, y1: 10, y2: 20, w: 10, h: 10 },
          { x1: 0, x2: 30, y1: 0, y2: 30, w: 30, h: 30 }
        )
      ).toBeFalsy();
    });

    it('should return true if the graph bounds is within the current view but at the edge on the right', () => {
      expect(
        viewportView['isNotOnScreen'](
          { x1: 20, x2: 30, y1: 10, y2: 20, w: 10, h: 10 },
          { x1: 0, x2: 30, y1: 0, y2: 30, w: 30, h: 30 }
        )
      ).toBeFalsy();
    });

    it('should return true if the graph bounds is within the current view but at the edge on the top', () => {
      expect(
        viewportView['isNotOnScreen'](
          { x1: 10, x2: 10, y1: 0, y2: 10, w: 10, h: 10 },
          { x1: 0, x2: 30, y1: 0, y2: 30, w: 30, h: 30 }
        )
      ).toBeFalsy();
    });

    it('should return true if the graph bounds is within the current view but at the edge on the bottom', () => {
      expect(
        viewportView['isNotOnScreen'](
          { x1: 10, x2: 10, y1: 20, y2: 30, w: 10, h: 10 },
          { x1: 0, x2: 30, y1: 0, y2: 30, w: 30, h: 30 }
        )
      ).toBeFalsy();
    });

    it('should return true if the graph bounds is within the current view but at the edge on the bottom', () => {
      expect(
        viewportView['isNotOnScreen'](
          { x1: 10, x2: 10, y1: 20, y2: 30, w: 10, h: 10 },
          { x1: 0, x2: 30, y1: 0, y2: 30, w: 30, h: 30 }
        )
      ).toBeFalsy();
    });

    it('should return false if the graph bounds outside of the current view', () => {
      expect(
        viewportView['isNotOnScreen'](
          { x1: -10, x2: -20, y1: -10, y2: -20, w: 10, h: 10 },
          { x1: 0, x2: 30, y1: 0, y2: 30, w: 30, h: 30 }
        )
      ).toBeTruthy();
    });
  });

  describe('METHOD: emptyView', () => {
    it('should return an extent that fills the parent container', () => {
      const ext = viewportView['emptyView']();

      expect(ext.bb.w).toBe(602);
      expect(ext.bb.h).toBe(302);
      expect(ext.bb.x1).toBe(10);
      expect(ext.bb.y1).toBe(10);
    });
  });

  describe('METHOD: getDisplayExtent', () => {
    it('should return the extent if the extent is empty', () => {
      const extent = {
        zoom: 1, pan: { x: 0, y: 0 },
        bb: { x1: 0, y1: 0, x2: 0, y2: 0, w: 0, h: 0 }
      }

      expect(viewportView['getDisplayExtent'](extent)).toEqual(extent);
    });


  });
});
