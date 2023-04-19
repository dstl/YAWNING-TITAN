import { Inject, Injectable } from '@angular/core';
import * as cytoscape from 'cytoscape';
import { Observable, Subject, of } from 'rxjs';
import { Network } from '../../../app/network-class/network';
import { Node } from '../../../app/network-class/network-interfaces';

import { NodeColourKey } from '../cytoscape/graph-objects';
import { NODE_KEY_CONFIG } from '../../app.tokens';

@Injectable()
export class CytoscapeService {

  constructor(
    @Inject(NODE_KEY_CONFIG) private nodeKey: NodeColourKey[]
  ) { }

  // constant number for padding
  private CYTOSCAPE_GRAPH_PADDING = 50;

  private _cy: cytoscape.Core = cytoscape();
  get cy(): cytoscape.Core {
    return this._cy;
  }

  private cytoscapeInstanceUpdate = new Subject<cytoscape.Core>();
  get cytoscapeInstance(): Observable<cytoscape.Core> {
    return this.cytoscapeInstanceUpdate.asObservable();
  }

  // html element where the graph is rendered
  private renderElement: HTMLElement | undefined;

  /**
   * Emit when canvas is double clicked
   */
  private doubleClickSubject = new Subject<cytoscape.EventObject>();
  get doubleClickEvent(): Observable<cytoscape.EventObject> {
    return this.doubleClickSubject.asObservable();
  }

  /**
   * Emit when canvas is clicked
   */
  private singleClickSubject = new Subject<cytoscape.EventObject>();
  get singleClickEvent(): Observable<cytoscape.EventObject> {
    return this.singleClickSubject.asObservable();
  }

  /**
   * Emit when items are dragged
   */
  private dragSubject = new Subject<cytoscape.EventObject>();
  get dragEvent(): Observable<cytoscape.EventObject> {
    return this.dragSubject.asObservable();
  }

  /**
   * Initialise service
   */
  public init(
    element: HTMLElement
  ) {
    // set the element the network will render on
    this.renderElement = element;

    // re render the network
    this.renderUpdate();
  }

  /**
   * Load the network into cytoscape
   * @param network
   */
  public loadNetwork(network: Network): void {
    if (!network) {
      return;
    }

    // reset cytoscape
    this._cy.elements().remove();

    // load all nodes
    network.nodeList.forEach(node => this.createCytoscapeNode(node.x_pos, node.y_pos, node));

    // load all edges
    network.edgeList.forEach(edge => this.createCytoscapeEdge(edge.edgeId, edge.nodeA, edge.nodeB));

    // fit to screen
    this._cy.fit(null, this.CYTOSCAPE_GRAPH_PADDING);
  }

  /**
   * Update the graph render
   */
  private renderUpdate(): void {
    this._cy = cytoscape({
      headless: false,
      container: this.renderElement, // container to render in
      elements: [],
      style: this.nodeKey.map(key => key.cytoscapeStyleSheet)
    });

    this.cytoscapeInstanceUpdate.next(this._cy);

    cytoscape.warnings(false);

    // set up listeners
    this.listenToCanvasDoubleClick();
    this.listenToSingleClick();
    this.listenToDragEvent();
  }

  /**
   * Listens to any events regarding a node being dragged
   */
  private listenToDragEvent(): void {
    this._cy.on('drag', (evt) => {
      this.dragSubject.next(evt);
    })
  }

  /**
   * Function that listens to double clicks on the canvas
   */
  private listenToCanvasDoubleClick(): void {
    this._cy.on('dbltap', (evt) => {
      this.doubleClickSubject.next(evt);
    });
  }

  /**
   * Function that listens to clicks on the canvas
   */
  private listenToSingleClick(): void {
    this._cy.bind('tap', (evt) => {
      this.singleClickSubject.next(evt);
    });
  }

  /**
   * Bring the whole network into view
   */
  public resetView(): void {
    this._cy.fit(null, this.CYTOSCAPE_GRAPH_PADDING);
  }

  /**
   * Creates and renders a cytoscape node
   * @param x
   * @param y
   * @param nodeProp
   */
  public createCytoscapeNode(x: number, y: number, nodeProp?: Node): void {
    // add the node onto cytoscape
    this._cy.add({
      data: {
        id: nodeProp?.uuid,
        name: nodeProp?.name
      },
      position: { x: x, y: y }
    });
  }

  /**
   * Remove a node with matching id as well as any edges connected to it
   * @param id
   */
  public removeCytoscapeNode(id: string): void {
    const item = this._cy.$id(id);
    // delete all edges connected to node
    item.connectedEdges().remove();

    // delete node
    item.remove();
  }

  /**
   * Update the cytoscape node data
   * @param node
   */
  public updateCytoscapeNode(node: Node) {
    const cyNode = this._cy.$id(node.uuid);

    // update position
    cyNode.position('x', Number(node.x_pos));
    cyNode.position('y', Number(node.y_pos));

    const data = Object.keys(node);
    data.forEach(key => cyNode.data(key, node[`${key}`]));
  }

  /**
   * Creates and renders an edge between 2 nodes
   * @param edgeId
   * @param nodeA
   * @param nodeB
   */
  public createCytoscapeEdge(edgeId: string, nodeA: string, nodeB: string) {
    // add edge to cytoscape
    this._cy.add({
      data: { id: edgeId, source: nodeA, target: nodeB }
    });
  }

  /**
   * Remove an edge with a matching id
   * @param id
   */
  public removeCytoscapeEdge(id: string) {
    this._cy.$id(id).remove();
  }

  /**
   * Highlights a node
   * Used when selecting a node from the node list
   * @param id
   */
  public selectNode(id: string) {
    // unselect all other nodes
    this._cy.nodes().unselect();

    // set the given id to selected
    this._cy.$id(id).select();

    // center on the node
    const viewportZoom = this._cy.animation({
      zoom: 2,
      center: { eles: `#${id}` },
      easing: 'ease-out-circ'
    });

    viewportZoom.play();
  }
}
