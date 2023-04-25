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

    this._bb = updatedExtent.bb;

    // draw the view box
    // TODO uncomment
    this.updateElementStyles();
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

    this.debug(extentB.bb, 'fixed', { 'z-index': 5 });

    console.log('a: ' + JSON.stringify(extentA))
    console.log('b: ' + JSON.stringify(extentB))

    // ratio between extentB and the parent container
    const viewZoom = Math.min(
      (this._parent.offsetWidth + this._parent.offsetLeft) / extentB.bb.w,
      (this._parent.offsetHeight + this._parent.offsetTop) / extentB.bb.h
    );

    console.log(viewZoom)

    // if graph is too far left of the screen
    if (extentB.bb.x1 < extentA.bb.x1) {
      // calculate how far in the graph the view is
      bb.x1 = -((extentB.bb.x1) * viewZoom);
      console.log('left: ' + bb.x1)
    } else {
      // set x1 to 0
      bb.x1 = extentA.bb.x1;
    }

    // if graph is too far above the screen
    if (extentB.bb.y1 < extentA.bb.y1) {
      // calculate how far in the graph the view is
      bb.y1 = -(extentB.bb.y1 * viewZoom);
      console.log('top: ' + bb.y1)
    } else {
      bb.y1 = extentA.bb.y1;
    }

    // if graph is too far right of the screen
    if (extentB.bb.x2 > (extentA.bb.x2 * extentA.zoom) + extentA.pan.x) {
      // calculate how far in the graph the view is
      bb.x2 = (extentB.bb.w - (extentB.bb.x2 - extentA.bb.x2)) * viewZoom
      console.log('right: ' + bb.x2)
    } else {
      // if in screen set x2 to
      bb.x2 = this._parent.getBoundingClientRect().right - this._parent.offsetLeft;
    }

    // if graph is too far below the screen
    if (extentB.bb.y2 > (extentA.bb.y2 * extentA.zoom) + extentA.pan.y) {
      // calculate how far in the graph the view is
      bb.y2 = (extentB.bb.h - (extentB.bb.y2 - extentA.bb.y2)) * viewZoom
      console.log('bot: ' + bb.y2)
    } else {
      bb.y2 = this._parent.getBoundingClientRect().bottom - this._parent.offsetTop;
    }

    console.log('')

    // get the height and width of the bounding box
    bb.w = bb.x2 - bb.x1;
    bb.h = bb.y2 - bb.y1;

    return {
      zoom: viewZoom,
      pan: { x: bb.x1, y: bb.y1 },
      bb
    };
  }

  /**
   * Multiply bounds by the zoom value
   * @param bb
   * @param zoom
   * @returns
   */
  private multiplyBounds(bb: CyBoundingBox, zoom: number, zoomFromCenter = true): CyBoundingBox {
    let x1 = 0, x2 = 0, y1 = 0, y2 = 0, w = 0, h = 0;

    if (zoomFromCenter) {
      x1 = bb.x1 - ((bb.w * zoom) - bb.w) / 2;
      x2 = bb.x2 + ((bb.w * zoom) - bb.w) / 2;
      y1 = bb.y1 - ((bb.h * zoom) - bb.h) / 2;
      y2 = bb.y2 + ((bb.h * zoom) - bb.h) / 2;
    } else {
      x1 = bb.x1 * zoom;
      x2 = bb.x2 * zoom;
      y1 = bb.y1 * zoom;
      y2 = bb.y2 * zoom;
    }

    return { w, h, x1, x2, y1, y2 };
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
      displayExtent.bb.w / this.displayElement.offsetWidth,
      displayExtent.bb.h / this.displayElement.offsetHeight
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
