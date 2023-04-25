import { CyBoundingBox, Extent, ViewportOptions } from "../viewport-objects";
import { ViewportElement } from "./viewport-element";

export class ViewportView extends ViewportElement {

  // the element used to display the whole graph view
  private displayElement: HTMLElement;

  /**
   * Create an instance of Viewport View
   * @param el
   * @param parent
   * @param vpOpts
   */
  constructor(el: HTMLElement, parent: HTMLElement, display: HTMLElement, vpOpts?: ViewportOptions) {
    // set class for the element
    el.setAttribute('class', 'viewport-view');

    super(el, parent, vpOpts);

    this.displayElement = display;
    el.style['position'] = 'absolute';
  }

  /**
   * Update the position of the viewport view
   */
  public updateViewPosition(viewExtent: Extent, displayExtent: Extent): void {
    // calculate what the view extent should be
    const updatedExtent = this.calculateViewBounds(viewExtent, displayExtent, this._bb);


    // draw the view box
    if (updatedExtent && updatedExtent.bb) {
      // set new bounds
      this._element.style['display'] = 'flex';
      this._bb = updatedExtent.bb;
      this.updateElementStyles();
    } else {
      // hide the element
      this._element.style['display'] = 'none';
    }
  }

  /**
   *
   * @param extentA extent of the current viewport
   * @param extentB extent of the bounds containing the whole graph
   * @param bb bounding box for the view in viewport
   * @returns
   */
  private calculateViewBounds(extentA: Extent, extentB: Extent, bb: CyBoundingBox): Extent {
    // if extentB is empty, return a full view
    if (this.isEmptyBounds(extentB.bb)) {
      return this.emptyView();
    }

    // get the proper graph extent that includes the padding from the viewport box
    extentB = this.getDisplayExtent(extentB);

    // if the graph is not on screen at all
    if (this.isNotOnScreen(extentB.bb, extentA.bb)) {
      return;
    }

    // ratio between extentB and the parent container
    const viewZoomW = (this._parent.offsetWidth) / extentB.bb.w;
    const viewZoomH = (this._parent.offsetHeight) / extentB.bb.h;

    // if graph is too far left of the screen
    if (extentB.bb.x1 < extentA.bb.x1) {
      // calculate how far in the graph the view is
      bb.x1 = -((extentB.bb.x1) * viewZoomW);
    } else {
      // set x1 to 0
      bb.x1 = extentA.bb.x1;
    }

    // if graph is too far above the screen
    if (extentB.bb.y1 < extentA.bb.y1) {
      // calculate how far in the graph the view is
      bb.y1 = -(extentB.bb.y1 * viewZoomH);
    } else {
      bb.y1 = extentA.bb.y1;
    }

    // if graph is too far right of the screen
    if (extentB.bb.x2 > (extentA.bb.x2 * extentA.zoom) + extentA.pan.x) {
      // calculate how far in the graph the view is
      bb.x2 = (extentB.bb.w - (extentB.bb.x2 - extentA.bb.x2)) * viewZoomW;
    } else {
      // if in screen set x2 to
      bb.x2 = this._parent.getBoundingClientRect().right - this._parent.getBoundingClientRect().left;
    }

    // if graph is too far below the screen
    if (extentB.bb.y2 > (extentA.bb.y2 * extentA.zoom) + extentA.pan.y) {
      // calculate how far in the graph the view is
      bb.y2 = (extentB.bb.h - (extentB.bb.y2 - extentA.bb.y2)) * viewZoomH;
    } else {
      bb.y2 = (this._parent.getBoundingClientRect().bottom - this._parent.getBoundingClientRect().top);
    }

    // get the height and width of the bounding box
    bb.w = bb.x2 - bb.x1;
    bb.h = bb.y2 - bb.y1;

    // add offsets
    bb.x1 += this._parent.offsetLeft;
    bb.x2 += this._parent.offsetLeft;
    bb.y1 += this._parent.offsetTop;
    bb.y2 += this._parent.offsetTop;

    return {
      zoom: Math.min(viewZoomW, viewZoomH),
      pan: { x: bb.x1, y: bb.y1 },
      bb
    };
  }

  /**
   * Returns true if the bounds has no height or width
   * @param bb
   * @returns
   */
  private isEmptyBounds(bb: CyBoundingBox): boolean {
    return bb.h == 0 || bb.w == 0 || isNaN(bb.h) || isNaN(bb.w);
  }

  /**
   * Return true if any part of the graph is not on screen
   * @param viewBox
   * @param currentView
   */
  private isNotOnScreen(graphBounds: CyBoundingBox, currentView: CyBoundingBox): boolean {
    return graphBounds.x2 < currentView.x1 || // the whole graph is to the left of the screen
      graphBounds.x1 > currentView.x2 || // the whole graph is to the right of the screen
      graphBounds.y2 < currentView.x1 || // the whole graph is above the screen
      graphBounds.y1 > currentView.x2; // the whole graph is below the screen
  }

  /**
   * Returns an extent that should cover the full view
   * @returns
   */
  private emptyView(): Extent {
    return {
      zoom: 0,
      pan: { x: 0, y: 0 },
      bb: {
        w: this._parent.offsetWidth,
        h: this._parent.offsetHeight,
        x1: this._parent.offsetLeft, y1: this._parent.offsetTop,
        x2: this._parent.offsetWidth,
        y2: this._parent.offsetHeight
      }
    }
  }

  /**
   * The display extent does not have the same width and height as the
   * parent container, so we will need to extrapolate what the parent
   * extent would be if it were overlaid on the display on the screen
   * @param displayExtent
   * @returns
   */
  private getDisplayExtent(displayExtent: Extent): Extent {
    if (!displayExtent.bb.h || !displayExtent.bb.w) {
      return displayExtent;
    }

    // calculate the difference between the display and the actual bounds
    const zoomRatio = Math.min(
      displayExtent.bb.w / (this.displayElement.offsetWidth - this._parent.offsetLeft),
      displayExtent.bb.h / (this.displayElement.offsetHeight - this._parent.offsetTop)
    )

    // calculate x and y values
    const x1 = displayExtent.bb.x1 - (this.displayElement.offsetLeft * zoomRatio);
    const y1 = displayExtent.bb.y1 - (this.displayElement.offsetTop * zoomRatio);
    const x2 = displayExtent.bb.x2 + (this.displayElement.offsetLeft * zoomRatio);
    const y2 = displayExtent.bb.y2 + (this.displayElement.offsetTop * zoomRatio);

    return {
      zoom: zoomRatio,
      pan: { x: x1, y: y1 },
      bb: {
        w: x2 - x1,
        h: y2 - y1,
        x1, x2, y1, y2
      }
    }
  }
}
