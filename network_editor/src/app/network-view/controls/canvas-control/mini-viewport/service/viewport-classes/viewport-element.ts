import { CyBoundingBox } from "../viewport-objects";

export class ViewportElement {

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

  constructor(el: HTMLElement, parent: HTMLElement) {
    // set element
    this._element = el;

    this._parent = parent;

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
    this._element.style['left'] = `${this._bb.x1}px`;
    this._element.style['top'] = `${this._bb.y1}px`;
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
  }
}
