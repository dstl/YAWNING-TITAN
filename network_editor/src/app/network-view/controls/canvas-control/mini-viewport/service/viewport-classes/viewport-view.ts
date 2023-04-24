import { CyBoundingBox, ViewExtent, ViewportOptions } from "../viewport-objects";
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
  }

  /**
   * Update the position of the viewport view
   */
  public updateViewPosition(viewExtent: ViewExtent, displayExtent: ViewExtent): void {
    // calculate what the view extent should be
    const updatedExtent = this.calculateViewBounds(viewExtent, displayExtent, this._bb);

    this._bb = updatedExtent.bb;

    this.updateElementStyles();
  }

  /**
   * The display extent does not have the same width and height as the
   * parent container, so we will need to extrapolate what the parent
   * extent would be if it were overlaid on the display on the screen
   * @param displayExtent
   * @returns
   */
  private transformDisplayExtent(displayExtent: ViewExtent): ViewExtent {
    // convert parent into the display extent
    let zoomRatio = Math.min(
      this.displayElement.offsetHeight / displayExtent.bb.h,
      this.displayElement.offsetWidth / displayExtent.bb.w
    )

    // if zoom is not a number, set to 1
    zoomRatio = isNaN(zoomRatio) ? 1 : zoomRatio;

    // set new bounds
    const newBBounds = this.multiplyBounds(displayExtent.bb, zoomRatio);
    displayExtent.pan = {
      x: newBBounds.x1,
      y: newBBounds.y1,
    }
    displayExtent.bb = newBBounds;

    return displayExtent;
  }

  /**
   * Standardise an extent so that the zoom level is equal to 1
   * @param extent
   * @returns
   */
  private standardiseExtent(extent: ViewExtent): ViewExtent {
    const bounds = this.multiplyBounds(extent.bb, 1 / extent.zoom);

    return {
      zoom: 1,
      pan: {
        x: bounds.x1,
        y: bounds.y1
      },
      bb: bounds
    }
  }

  /**
   *
   * @param extentA extent of the current viewport
   * @param extentB extent of the bounds containing the whole graph
   * @param bb bounding box for the view in viewport
   * @returns
   */
  private calculateViewBounds(extentA: ViewExtent, extentB: ViewExtent, bb: CyBoundingBox): ViewExtent {
    // width and height that is off the display screen
    let offsetLeft = 0,
      offsetTop = 0,
      offsetRight = 0,
      offsetBottom = 0;

    extentB = this.transformDisplayExtent(extentB);

    const viewZoom = extentA.zoom;
    extentA = this.standardiseExtent(extentA);
    extentB = this.standardiseExtent(extentB);

    console.log(extentB)

    // calculate offsets
    if (extentA.bb.x1 < extentB.bb.x1) {
      // set offset left
      offsetLeft = Math.abs(extentB.bb.x1 - extentA.bb.x1)

      // set x1 to 0
      bb.x1 = 0;

      // remove the width that is off the screen
      bb.w -= Math.abs(extentB.bb.x1 - extentA.bb.x1)
    } else {
      // x1 will be the difference between the view and the display
      bb.x1 = Math.abs(extentA.bb.x1 - extentB.bb.x1);
    }

    if (extentA.bb.x2 > extentB.bb.x2) {
      // set offset right
      offsetRight = Math.abs(extentA.bb.x2 - extentB.bb.x2);

      // remove the width that is off the screen
      bb.w -= Math.abs(extentB.bb.x2 - extentA.bb.x2);

      //set x2 to width
      bb.x2 = bb.w;
    } else {
      bb.x2 = Math.abs(extentB.bb.x2 - extentA.bb.x2);
    }

    if (extentA.bb.y1 < extentB.bb.y1) {
      // set offset top
      offsetTop = Math.abs(extentB.bb.y1 - extentA.bb.y1);

      // set y1 to 0
      bb.y1 = 0;

      // remove the height that is off screen
      bb.h -= Math.abs(extentB.bb.y1 - extentA.bb.y1)
    } else {
      bb.y1 = Math.abs(extentA.bb.y1 - extentB.bb.y1);
    }

    if (extentA.bb.y2 > extentB.bb.y2) {
      // set offset bottom
      offsetBottom = Math.abs(extentA.bb.y2 - extentB.bb.y2);

      // remove the height that is off screen
      bb.h -= Math.abs(extentB.bb.y2 - extentA.bb.y2)

      // set y2 to height
      bb.y2 = bb.h;
    } else {
      bb.y2 = Math.abs(extentB.bb.y2 - extentA.bb.h);
    }


    const ext = this.standardiseExtent({
      zoom: viewZoom,
      pan: { x: bb.x1, y: bb.y1 },
      bb
    });

    return ext;
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
   * Multiply bounds by the zoom value
   * @param bb
   * @param zoom
   * @returns
   */
  private multiplyBounds(bb: CyBoundingBox, zoom: number): CyBoundingBox {
    const x1 = ((bb.x1 * zoom) / 2) - (bb.x1 / 2);
    const y1 = ((bb.y1 * zoom) / 2) - (bb.y1 / 2);

    return {
      w: bb.w * zoom,
      h: bb.h * zoom,
      x1: x1,
      y1: y1,
      x2: x1 + (bb.w * zoom),
      y2: y1 + (bb.h * zoom)
    }
  }

  /**
   * Get the difference between 2 number but return as positive value
   * @param a
   * @param b
   * @returns
   */
  private diff(a: number, b: number): number {
    return Math.abs(a - b);
  }
}
