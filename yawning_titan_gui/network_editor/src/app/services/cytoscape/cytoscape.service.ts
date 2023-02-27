import { Inject, Injectable } from '@angular/core';
import * as cytoscape from 'cytoscape';
import { Observable, Subject } from 'rxjs';
import { Network } from '../../../app/network-class/network';
import { NetworkJson, Node } from '../../../app/network-class/network-interfaces';
import { v4 as uuid } from 'uuid';

import { ElementType, NodeColourKey } from '../cytoscape/graph-objects';
import { NODE_KEY_CONFIG } from 'src/app/app.tokens';

@Injectable()
export class CytoscapeService {

  constructor(@Inject(NODE_KEY_CONFIG) private nodeKey: NodeColourKey[]) { }

  private nodeCount = 0;

  private cy: cytoscape.Core = cytoscape();

  private _network: Network;

  get network(): Network {
    return this._network;
  }

  // html element where the graph is rendered
  private renderElement: HTMLElement | undefined;

  // id of the current selected node
  private selectedElement: { id: string, type: ElementType };

  // used to update the application what node/edge is currently selected
  private selectedElementSubject = new Subject<{ id: string, type: ElementType }>();
  get selectedElementEvent(): Observable<{ id: string, type: ElementType }> {
    return this.selectedElementSubject.asObservable();
  }

  // used to update the x and y positions in the node properties component
  private elementDragSubject = new Subject<{ id: string, position: { x: number, y: number } }>();
  get elementDragEvent(): Observable<{ id: string, position: { x: number, y: number } }> {
    return this.elementDragSubject.asObservable();
  }

  /**
   * Initialise service
   */
  public init(
    element: HTMLElement
  ) {
    // set the element the network will render on
    this.renderElement = element;

    this._network = new Network();

    // re render the network
    this.renderUpdate();
  }

  /**
   * Returns a JSON representation of the current network graph
   * @returns
   */
  public getNetworkJson(): NetworkJson {
    return this._network.toJson();
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
    this.cy.elements().remove();

    // set network
    this._network = network;

    // load all nodes
    network.nodeList.forEach(node => this.createNode(node.x_pos, node.y_pos, node));

    // load all edges
    network.edgeList.forEach(edge => this.createEdge(null, edge.nodeA, edge.nodeB));

    // TODO: should only do this if set to auto layout/nodes have no pos
    this.cy.layout({ name: 'cose' }).run();

    // fit to screen
    this.cy.fit();
  }

  /**
   * Update a node using the given details
   * @param nodeId
   * @param nodeDetails
   * @returns
   */
  public updateNode(nodeDetails: Node): void {
    // check if node with id exists
    const node = this.cy.getElementById(nodeDetails?.uuid);

    if (!node || !node.isNode || !node.isNode()) {
      return;
    }

    // update position
    node.position('x', Number(nodeDetails.x_pos));
    node.position('y', Number(nodeDetails.y_pos));

    const data = Object.keys(nodeDetails);
    data.forEach(key => node.data(key, nodeDetails[`${key}`]));

    this._network.editNodeDetails(nodeDetails.uuid, nodeDetails)
  }

  /**
   * Deletes the currently selected item
   */
  public deleteItem() {
    if (!this.selectedElement || !this.selectedElement.id || !this.selectedElement.type) {
      // nothing to delete
      return;
    }

    const item = this.cy.$id(this.selectedElement.id);
    // if node, delete any edges going to it
    if (this.selectedElement.type == ElementType.NODE) {
      // delete all edges connected to node
      item.connectedEdges().remove();
      this._network.removeNode(this.selectedElement.id);
    } else {
      this._network.removeEdge(this.selectedElement.id);
    }

    this.cy.$id(this.selectedElement.id).remove();
    this.setSelectedItem(null);
  }

  /**
   * Update the graph render
   */
  private renderUpdate(): void {
    this.cy = cytoscape({
      container: this.renderElement, // container to render in
      elements: [],
      style: this.nodeKey.map(key => key.cytoscapeStyleSheet)
    });

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
    this.cy.on('drag', (evt) => {
      this.elementDragSubject.next({
        id: evt.target.id(),
        position: evt.target.position()
      })
    })
  }

  /**
   * Function that listens to double clicks on the canvas
   */
  private listenToCanvasDoubleClick(): void {
    this.cy.on('dbltap', (evt) => {
      // check if there is a node/edge targeted
      if (Array.isArray(evt.target) || !!evt.target.length) {
        return;
      }
      // generate a new node
      this.createNode(evt.position.x, evt.position.y)
    });
  }

  /**
   * Function that listens to clicks on the canvas
   */
  private listenToSingleClick(): void {
    this.cy.bind('tap', (evt) => {
      // clicked on a node
      if (evt.target?.isNode && evt.target?.isNode()) {
        // current selected target
        this.handleNodeSingleClick(evt);
      }

      // set the clicked node/edge as the selected item
      this.setSelectedItem(evt)
    });
  }

  /**
   * Bring the whole network into view
   */
  public resetView(): void {
    this.cy.fit(null, 200);
  }

  /**
   * Handle a single click event
   * @param evt
   */
  private handleNodeSingleClick(evt: cytoscape.EventObject): void {
    // create an edge if the selected item was a node
    if (this.selectedElement?.type == ElementType.NODE) {
      this.createEdge(null, this.selectedElement.id, evt.target?.id())
    }
  }

  /**
   * Adds a node to the network
   * @param x
   * @param y
   * @param node
   * @returns
   */
  private createNode(x: number, y: number, node?: Node): void {
    this.nodeCount++;

    // if no node properties are provided, create an empty node and add to network
    if (!node) {
      const nodeProperties = {
        uuid: uuid(),
        name: `node ${this.nodeCount}`,
        entry_node: false,
        high_value_node: false,
        x_pos: x,
        y_pos: y,
        vulnerability: 0
      }

      // add to network
      this.cy.add({
        data: {
          id: nodeProperties.uuid,
          name: nodeProperties.name
        },
        position: { x: x, y: y }
      });

      // add node to network
      this._network.addNode(nodeProperties);
      return;
    }

    // add the node onto cytoscape
    this.cy.add({
      data: {
        id: node?.uuid,
        name: node?.name
      },
      position: { x: x, y: y }
    });
  }

  /**
   * Create an edge between 2 nodes
   * @param nodeA
   * @param nodeB
   * @returns
   */
  private createEdge(edgeId: string, nodeA: string, nodeB: string): void {
    // check if nodes already have connection
    if (this.areNodesConnected(nodeA, nodeB)) {
      return;
    }

    // if no id provided, generate one
    edgeId = edgeId ? edgeId : uuid();

    this.cy.add({
      data: { id: edgeId, source: nodeA, target: nodeB }
    });

    this.network.addEgde(edgeId, nodeA, nodeB);

    this.setSelectedItem(null);
  }

  /**
   * Highlights a node/edge
   * @param elementId
   */
  private setSelectedItem(evt: cytoscape.EventObject) {
    // check if an element was clicked
    if (!evt || !evt.target || !evt.target.isNode || !evt.target.isEdge) {
      // clicked on background
      this.selectedElement = null;
      this.selectedElementSubject.next(this.selectedElement);
      return;
    }

    // set element as selected
    this.selectedElement = {
      id: evt.target?.id(),
      type: evt.target.isNode() ? ElementType.NODE : ElementType.EDGE
    }
    this.selectedElementSubject.next(this.selectedElement);
  }

  /**
   * Function used to check if both nodes are connected
   * @param nodeA
   * @param nodeB
   * @returns
   */
  private areNodesConnected(nodeA: string, nodeB: string): boolean {
    // check if node is being connected to itself
    if (nodeA == nodeB) {
      // node is always going to be connected to itself
      return true;
    }

    const cyNodeA = this.cy.getElementById(nodeA);
    const cyNodeB = this.cy.getElementById(nodeB);

    // make sure we're checking nodes
    if (!cyNodeA?.isNode && !cyNodeB?.isNode && !cyNodeA?.isNode() && !cyNodeB?.isNode()) {
      return;
    }

    // return true if there are edges connecting both nodes
    return !cyNodeA.edgesWith(cyNodeB).empty()
  }
}
