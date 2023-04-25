import { ElementRef, Injectable, Renderer2, RendererFactory2 } from '@angular/core';
import { CytoscapeService } from '../../../../../services/cytoscape/cytoscape.service';
import { NetworkService } from '../../../../../network-class/network.service';
import { CyBoundingBox, DisplayValue, ViewportOptions } from './viewport-objects';
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

  /********************************************************************
   * Viewport Options
   ********************************************************************/
  // viewport options
  private vpOpts: ViewportOptions;

  /**
   * Initialises the viewport
   * @param viewportElement
   */
  public init(viewportElement: HTMLElement, options?: ViewportOptions): void {
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

    // initialise viewport view
    this.initViewportView();

    // listen to network changes
    this.listenToUpdates();
  }

  /**
   * Listen to any updates to cytoscape
   */
  private listenToUpdates(): void {
    this.networkService.networkObservable.subscribe(() => this.updateDisplayImage());

    this._cy.on('render', (evt) => {
      this.updateDisplayImage();
    });

    this._cy.on('add remove pan zoom render resize', (evt) => {
      this.updateView();
    });
  }

  /**
   * Parse the options for the viewport
   * @param options
   */
  private parseOptions(options: ViewportOptions): void {
    this.vpOpts = options;
  }

  /**
   * Sets the bounding box that contains all the cytoscape elements
   */
  private updateCyBoundingBox(): void {
    // set the cytoscape bounding box
    this._displayBoundingBox = this._cy.elements().boundingBox();

    // get the lower zoom value
    this._displayVal['zoom'] = Math.min(
      this._viewportPanel.offsetHeight / this._displayBoundingBox.h,
      this._viewportPanel.offsetWidth / this._displayBoundingBox.w
    )

    if (!isNaN(this._displayVal.zoom)) {
      this._displayVal.zoom = 1;
    }

    // get the pan value
    this._displayVal['pan'] = {
      x: (this._viewportPanel.offsetWidth - this._displayVal.zoom * (this._displayBoundingBox.x1 + this._displayBoundingBox.x2)) / 2,
      y: (this._viewportPanel.offsetHeight - this._displayVal.zoom * (this._displayBoundingBox.y1 + this._displayBoundingBox.y2)) / 2,
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
    this._viewportDisplay = new ViewportDisplay(document.createElement('img'), this._viewportPanel, this.vpOpts);

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
    const w = this._viewportPanel.offsetWidth - (this.vpOpts.padding * 2);
    const h = this._viewportPanel.offsetHeight - (this.vpOpts.padding * 2);
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
      this._viewportDisplay.element,
      this.vpOpts
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

    this._viewportView.updateViewPosition({
      zoom: this._cy.zoom(),
      pan: this._cy.pan(),
      bb: this._cy.extent()
    }, {
      zoom: 1,
      pan: { x: renderedBounds.x1, y: renderedBounds.y1 },
      bb: renderedBounds
    })
  }
}
