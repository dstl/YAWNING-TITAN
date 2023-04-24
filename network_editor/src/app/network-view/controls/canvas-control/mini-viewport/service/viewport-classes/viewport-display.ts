import { ViewportOptions } from "../viewport-objects";
import { ViewportElement } from "./viewport-element";

export class ViewportDisplay extends ViewportElement {

  /**
   * Create an instance of Viewport Display
   * @param el
   * @param parent
   * @param vpOpts
   */
  constructor(el: HTMLElement, parent: HTMLElement, vpOpts?: ViewportOptions) {
    // set the class for the element
    el.setAttribute('class', 'viewport-display');

    super(el, parent, vpOpts);
  }

  /**
   * Update the image to display in  the element
   * @param base64Png
   */
  public updateImage(base64Png: string) {
    // update the image source if there is any
    var img = new Image();
    if (base64Png.indexOf('image/png') < 0) {
      this._element.removeAttribute('src');
    } else {
      img.src = base64Png;
      this._element.setAttribute('src', base64Png);
    }

    // calculate where the element should be so that it is centered
    this._bb.h = img.height ? img.height : this._bb.h;
    this._bb.w = img.width ? img.width : this._bb.w;
    this._bb.x1 = (((this._parent.offsetWidth - this._parent.offsetLeft) - (this._bb.w + this.vpOpts.padding / 2)) / 2)
    this._bb.x2 = this._bb.x1 + this._bb.w;
    this._bb.y1 = (((this._parent.offsetHeight - this._parent.offsetTop) - (this._bb.h + this.vpOpts.padding / 2)) / 2)
    this._bb.y2 = this._bb.y1 + this._bb.h;

    // update the element bounds
    this.updateElementStyles();
  }
}
