import { CyBoundingBox, ViewportOptions } from "../viewport-objects";

export class ViewportElement {
  // padding for any elements
  protected vpOpts: ViewportOptions;

  // element which will display the relevant viewport item
  protected _element: HTMLElement;
  get element(): HTMLElement {
    return this._element;
  }

  // element which contains this element
  protected _parent: HTMLElement;

  // bounding box of the element
  protected _bb: CyBoundingBox;
  get bb(): CyBoundingBox {
    return this._bb;
  }

  constructor(el: HTMLElement, parent: HTMLElement, opts?: ViewportOptions) {
    // set element
    this._element = el;

    this._parent = parent;

    this.vpOpts = opts;

    // set absolute position
    this._element.style['position'] = 'relative';

    // set empty bounds
    this._bb = {
      h: 0, w: 0,
      x1: 0, x2: 0,
      y1: 0, y2: 0
    }
  }

  /**
   * Updates the element styles to match the set bounds
   */
  protected updateElementStyles(): void {
    this._element.style['left'] = `${this._bb.x1 + this._parent.offsetLeft}px`;
    this._element.style['top'] = `${this._bb.y1 + this._parent.offsetTop}px`;
    this._element.style['width'] = `${this._bb.w}px`;
    this._element.style['height'] = `${this._bb.h}px`;

    // get parent computed style
    if (!getComputedStyle) {
      return;
    }
    const computedParentStyle = window.getComputedStyle(this._parent, null);
    let pHeight = this._parent.clientHeight;
    let pWidth = this._parent.clientWidth;

    pHeight -= parseFloat(computedParentStyle.paddingTop) + parseFloat(computedParentStyle.paddingBottom);
    pWidth -= parseFloat(computedParentStyle.paddingLeft) + parseFloat(computedParentStyle.paddingRight);

    // set max height and width to parent container inner height and width
    this._element.style['max-height'] = `${pHeight}px`;
    this._element.style['max-width'] = `${pWidth}px`;
  }
}
