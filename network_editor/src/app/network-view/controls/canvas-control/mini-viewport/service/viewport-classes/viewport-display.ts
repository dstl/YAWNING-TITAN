import { ViewportElement } from "./viewport-element";

export class ViewportDisplay extends ViewportElement {

  /**
   * Create an instance of Viewport Display
   * @param el
   * @param parent
   * @param vpOpts
   */
  constructor(el: HTMLElement, parent: HTMLElement) {
    // set the class for the element
    el.setAttribute('class', 'viewport-display');

    super(el, parent);
  }

  /**
   * Update the image to display in  the element
   * @param base64Png
   */
  public updateImage(base64Png: string) {
    // update the image source if there is any
    var img = new Image();
    if (!base64Png || base64Png.indexOf('image/png') < 0) {
      this._element.removeAttribute('src');
    } else {
      img.src = base64Png;
      this._element.setAttribute('src', base64Png);
    }

    img.onload = () => this.handleImageLoad(img.height, img.width)
  }

  /**
   *
   * @param h
   * @param w
   */
  private handleImageLoad(h: number, w: number): void {
    // calculate where the element should be so that it is centered
    this._bb.h = h ? h : this._bb.h;
    this._bb.w = w ? w : this._bb.w;
    this._bb.x1 = (this._parent.clientWidth - this._bb.w) / 2
    this._bb.x2 = this._bb.x1 + this._bb.w;
    this._bb.y1 = (this._parent.clientHeight - this._bb.h) / 2
    this._bb.y2 = this._bb.y1 + this._bb.h;

    // update the element bounds
    this.updateElementStyles();
  }
}
