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

  /**
   * Draws a bounding box on the screen
   *
   * (FOR DEBUGGING ONLY)
   * @param bb
   * @param position default relative to the parent box, use 'fixed' to show its placement exactly on screen
   */
  protected debug(bb: CyBoundingBox, position = 'relative', opts?: any): void {
    const div = document.createElement('div');
    div.style['border'] = opts && opts['border'] ? opts['border'] : '1px solid red';
    div.style['z-index'] = opts && opts['z-index'] ? opts['z-index'] : 4;
    div.style['background-color'] = opts && opts['background-color'] ? opts['background-color'] : 'transparent';

    div.style['left'] = `${bb.x1}px`;
    div.style['top'] = `${bb.y1}px`;
    div.style['width'] = `${bb.w}px`;
    div.style['height'] = `${bb.h}px`;

    div.style['position'] = position;
    div.style['pointer-events'] = opts && opts['pointer-events'] ? opts['pointer-events'] : 'none';

    div.className = 'debugBox';

    const debugEl = document.getElementsByClassName('debugBox');
    if (debugEl.length) {
      while (debugEl[0]) {
        debugEl[0].parentNode.removeChild(debugEl[0])
      }
    }
    document.body.appendChild(div);
  }
}
