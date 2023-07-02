import { ElementRef, Injectable, Renderer2, RendererFactory2 } from '@angular/core';
import { CytoscapeService } from '../../../../../services/cytoscape/cytoscape.service';
import { NetworkService } from '../../../../../network-class/network.service';
import { CyBoundingBox, DisplayValue } from './viewport-objects';
import * as cytoscape from 'cytoscape';
import { ViewportView } from './viewport-classes/viewport-view';
import { ViewportDisplay } from './viewport-classes/viewport-display';

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

  /********************************************************************
   * Viewport Elements
   ********************************************************************/
  // parent container for all viewport elements
  private _viewportPanel: HTMLElement;

  // image to display on viewport element
  private _viewportDisplay: ViewportDisplay;

  // box that highlights where on the overall network the user is focused on
  private _viewportView: ViewportView;

  /********************************************************************
   *
   ********************************************************************/
  // display values
  private _displayVal: DisplayValue = { zoom: null, pan: null }

  // bounding box that contains all elements
  private _displayBoundingBox: CyBoundingBox;

  // prevent the display from overwriting when one is in progress
  private _updatingDisplay = false;

  /**
   * Initialises the viewport
   * @param viewportElement
   */
  public init(viewportElement: HTMLElement): void {
    // set the viewport element
    this._viewportPanel = viewportElement;

    // set the cytoscape instance
    this._cy = this.cytoscapeService.cy;

    // get the bounding box for cytoscape elements
    this.updateCyBoundingBox();

    // initialise viewport items
    this.initViewportDisplay();

    // initialise viewport view
    this.initViewportView();

    // listen to network changes
    this.listenToUpdates();
  }

  /**
   * Listen to any updates to cytoscape
   */
  private listenToUpdates(): void {
    this.networkService.networkObservable.subscribe(() => {
      this.updateDisplayImage();
      this.updateView();
    });

    this._cy.on('add remove pan zoom render resize', (evt) => {
      this.updateDisplayImage();
      this.updateView();
    });
  }

  /**
   * Sets the bounding box that contains all the cytoscape elements
   */
  private updateCyBoundingBox(): void {
    // set the cytoscape bounding box
    this._displayBoundingBox = this.applyPaddingToBoundingBox(
      this._cy.elements().boundingBox(),
      this.cytoscapeService.graphPadding
    );

    // get the lower zoom value
    this._displayVal['zoom'] = {
      w: this._viewportPanel.offsetWidth / this._displayBoundingBox.w,
      h: this._viewportPanel.offsetHeight / this._displayBoundingBox.h
    }

    if (isNaN(this._displayVal.zoom.h)) {
      this._displayVal.zoom.h = 1;
    }

    if (isNaN(this._displayVal.zoom.w)) {
      this._displayVal.zoom.w = 1;
    }

    // get the pan value
    this._displayVal['pan'] = {
      x: (this._viewportPanel.offsetWidth - this._displayVal.zoom.w * (this._displayBoundingBox.x1 + this._displayBoundingBox.x2)) / 2,
      y: (this._viewportPanel.offsetHeight - this._displayVal.zoom.h * (this._displayBoundingBox.y1 + this._displayBoundingBox.y2)) / 2,
    }
  }

  /********************************************************************
   * Viewport Display
   ********************************************************************/
  /**
   * Initialise the viewport display
   */
  private initViewportDisplay(): void {
    // create viewport display
    this._viewportDisplay = new ViewportDisplay(document.createElement('img'), this._viewportPanel);

    // attach to the panel
    this.renderer.appendChild(this._viewportPanel, this._viewportDisplay.element);

    // update the display
    this.updateDisplayImage();
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
    this.updateCyBoundingBox();

    // calculate the size of the png
    const w = this._viewportPanel.offsetWidth;
    const h = this._viewportPanel.offsetHeight;
    const bb = this._displayBoundingBox;
    const zoom = Math.min(w / bb.w, h / bb.h);

    // create the png
    const png = this._cy.png({
      full: true,
      scale: zoom,
      maxHeight: h,
      maxWidth: w
    });

    this._viewportDisplay.updateImage(png);

    this._updatingDisplay = false;
  }

  /********************************************************************
   * Viewport View
   ********************************************************************/
  private initViewportView(): void {
    // create viewport view
    this._viewportView = new ViewportView(
      document.createElement('div'),
      this._viewportPanel,
      this._viewportDisplay.element
    );

    // attach to the panel
    this.renderer.appendChild(this._viewportPanel, this._viewportView.element);

    // update the view
    this.updateView();
  }

  /**
   * Updates the viewport view
   */
  private updateView(): void {
    // get the actual rendered bounding box of the whole graph
    const renderedBounds = this._cy.elements().renderedBoundingBox();

    // get viewport rendered bounds
    const zoom = this._cy.zoom();
    const pan = this._cy.pan();
    const extent = this._cy.extent();
    const x1 = (extent.x1 * zoom) + pan.x;
    const x2 = (extent.x2 * zoom) + pan.x;
    const y1 = (extent.y1 * zoom) + pan.y;
    const y2 = (extent.y2 * zoom) + pan.y;

    this._viewportView.updateViewPosition({
      zoom: 1,
      pan: { x: x1, y: y1 },
      bb: { x1, x2, y1, y2, w: x2 - x1, h: y2 - y1 }
    }, {
      zoom: 1,
      pan: { x: renderedBounds.x1, y: renderedBounds.y1 },
      bb: renderedBounds
    })
  }

  /**
   * Applies the cytoscape padding to the bounding box
   * @param bb
   * @param padding
   * @returns
   */
  private applyPaddingToBoundingBox(bb: CyBoundingBox, padding?: number, zoom = 1): CyBoundingBox {
    padding = padding ? (padding * zoom) : 0;
    return {
      w: bb.w + padding,
      h: bb.h + padding,
      x1: bb.x1 - padding,
      x2: bb.x2 + padding,
      y1: bb.y1 - padding,
      y2: bb.y2 + padding
    }
  }
}
