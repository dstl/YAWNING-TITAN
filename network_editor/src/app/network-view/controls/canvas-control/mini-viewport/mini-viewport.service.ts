import { ElementRef, Injectable, Renderer2, RendererFactory2 } from '@angular/core';
import { CytoscapeService } from '../../../../services/cytoscape/cytoscape.service';
import { NetworkService } from '../../../../network-class/network.service';
import { CyBoundingBox, DisplayValue, ViewportOptions } from './viewport-objects';
import * as cytoscape from 'cytoscape';

@Injectable()
export class MiniViewportService {

  private renderer: Renderer2;

  constructor(
    private rendererFactory: RendererFactory2,
    private cytoscapeService: CytoscapeService,
    private networkService: NetworkService
  ) {
    this.renderer = this.rendererFactory.createRenderer(null, null);
  }

  // cytoscape instance
  private _cy: cytoscape.Core;

  // viewport element
  private _viewportPanel: ElementRef;

  private _viewportView: HTMLElement;

  // image to display on viewport element
  private _viewportDisplay: HTMLElement;

  // display values
  private _displayVal: DisplayValue = { zoom: null, pan: null }

  // bounding box that contains all elements
  private _displayBoundingBox: CyBoundingBox;

  // prevent the display from overwriting when one is in progress
  private _updatingDisplay = false;

  // padding for the viewport
  private _viewportPadding = 0;

  /**
   * Initialises the viewport
   * @param viewportElement
   */
  public init(viewportElement: ElementRef, options?: ViewportOptions): void {
    // set the viewport element
    this._viewportPanel = viewportElement;

    // set the cytoscape instance
    this._cy = this.cytoscapeService.cy;

    if (options) {
      this.parseOptions(options);
    }

    // get the bounding box for cytoscape elements
    this.updateCyBoundingBox();

    // initialise viewport items
    this.initViewportDisplay();

    // listen to network changes
    this.listenToUpdates();
  }

  /**
   * Listen to any updates to cytoscape
   */
  private listenToUpdates(): void {
    this.networkService.networkObservable.subscribe(() => this.updateDisplayImage());

    this._cy.on('render ', (evt) => {
      this.updateDisplayImage()
      // console.log(evt)
    });
  }

  /**
   * Parse the options for the viewport
   * @param options
   */
  private parseOptions(options: ViewportOptions): void {
    this._viewportPadding = options["padding"];
  }

  /**
   * Sets the bounding box that contains all the cytoscape elements
   */
  private updateCyBoundingBox(): void {
    // set the cytoscape bounding box
    this._displayBoundingBox = this._cy.elements().boundingBox();
  }

  /**
   * Initialise the viewport display
   */
  private initViewportDisplay(): void {
    // create image tag
    this._viewportDisplay = document.createElement('img');
    this._viewportDisplay.setAttribute('class', 'viewport-display');

    // attach to the panel
    this.renderer.appendChild(this._viewportPanel.nativeElement, this._viewportDisplay);

    this.updateDisplayValues();
    this.updateDisplayImage();
  }

  /**
   * Set up the size of the display
   */
  private updateDisplayValues(): void {
    // update bounding box
    this.updateCyBoundingBox();

    // get the lower zoom value
    this._displayVal['zoom'] = Math.min(
      this._viewportPanel.nativeElement.offsetHeight / this._displayBoundingBox.h,
      this._viewportPanel.nativeElement.offsetWidth / this._displayBoundingBox.w
    )

    if (!isNaN(this._displayVal.zoom)) {
      this._displayVal.zoom = 1;
    }

    // get the pan value
    this._displayVal['pan'] = {
      x: (this._viewportPanel.nativeElement.offsetWidth - this._displayVal.zoom * (this._displayBoundingBox.x1 + this._displayBoundingBox.x2)) / 2,
      y: (this._viewportPanel.nativeElement.offsetHeight - this._displayVal.zoom * (this._displayBoundingBox.y1 + this._displayBoundingBox.y2)) / 2,
    }
  }

  /**
   * Updates the display
   */
  private updateDisplayImage(): void {
    // do nothing if already updating
    if (this._updatingDisplay) {
      return;
    }

    this._updatingDisplay = true;

    // update display values
    this.updateDisplayValues();

    const w = this._viewportPanel.nativeElement.offsetWidth - (this._viewportPadding * 2);
    const h = this._viewportPanel.nativeElement.offsetHeight - (this._viewportPadding * 2);
    const bb = this._displayBoundingBox;
    const zoom = Math.min(w / bb.w, h / bb.h);

    const png = this._cy.png({
      full: true,
      scale: zoom,
      maxHeight: h,
      maxWidth: w
    });

    if (png.indexOf('image/png') < 0) {
      this._viewportDisplay.removeAttribute('src');
    } else {
      this._viewportDisplay.setAttribute('src', png);
    }

    var translate = {
      x: (w - zoom * (bb.w)) / 2,
      y: (h - zoom * (bb.h)) / 2
    };

    this._viewportDisplay.style['position'] = 'relative';
    this._viewportDisplay.style['left'] = (translate.x + this._viewportPadding) + 'px';
    this._viewportDisplay.style['top'] = (translate.y + this._viewportPadding) + 'px';
    this._updatingDisplay = false;
  }

  /**
   * Updates the box where the current view is
   */
  private updateViewBox(): void {

  }
}
