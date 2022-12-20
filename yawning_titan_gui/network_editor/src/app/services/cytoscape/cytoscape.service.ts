import { HostListener, Injectable } from '@angular/core';
import * as cytoscape from 'cytoscape';
import { Subject } from 'rxjs';
import { Network } from '../../../app/network-class/network';
import { NetworkJson, Node } from '../../../app/network-class/network-interfaces';
import { v4 as uuid } from 'uuid';

import { ElementType } from '../cytoscape/graph-objects';

@Injectable()
export class CytoscapeService {

  private cy: cytoscape.Core = cytoscape();

  private network: Network;

  get cytoscapeObj(): cytoscape.Core {
    return this.cy;
  }

  // html element where the graph is rendered
  private renderElement: HTMLElement | undefined;

  // list of elements in the network
  private elementsArr: cytoscape.ElementDefinition[] | undefined = [];

  private defaultNodeStyle = {
    'label': 'data(name)',
    'background-color': '#f0f0f0',
    'border-color': '#909090',
    'border-width': 1,
    'color': '#fff',
    'line-color': '#909090'
  };

  private highlightedNodeStyle = {
    'label': 'data(name)',
    'background-color': '#009eff',
    'border-color': '#005e97',
    'border-width': 1,
    'line-color': '#009eff'
  }

  // the stylesheet for the graph
  private style: cytoscape.Stylesheet[] = [
    {
      selector: 'node',
      style: this.defaultNodeStyle
    },
    {
      selector: 'edge',
      style: {
        'width': 3,
        'line-color': '#505050',
        'target-arrow-color': '#ccc',
        'curve-style': 'bezier'
      }
    }
  ]

  // id of the current selected node
  private selectedElement: { id: string, type: ElementType };

  public selectedElementSubject = new Subject<{ id: string, type: ElementType }>();

  /**
   * Initialise service
   */
  public init(
    element: HTMLElement
  ) {
    // set the element the network will render on
    this.renderElement = element;

    this.network = new Network();

    // re render the network
    this.renderUpdate();
  }

  /**
   * Returns a JSON representation of the current network graph
   * @returns
   */
  public getNetworkJson(): NetworkJson {
    return this.network.toJson();
  }

  /**
   * Load the network into cytoscape
   * @param network
   */
  public loadNetwork(network: Network): void {
    // reset cytoscape
    this.cy.elements().remove();

    // set network
    this.network = network;

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
   * Deletes the currently selected item
   */
  public deleteItem() {
    if (!this.selectedElement || !this.selectedElement.id || !this.selectedElement.type) {
      // nothing to delete
      return;
    }

    const item = this.cy.getElementById(this.selectedElement.id);
    // if node, delete any edges going to it
    if (this.selectedElement.type == ElementType.NODE) {
      // delete all edges connected to node
      item.connectedEdges().remove();
      this.network.removeNode(this.selectedElement.id);
    } else {
      this.network.removeEdge(this.selectedElement.id);
    }

    item.remove();
    this.setSelectedItem(null);
  }

  /**
   * Update the graph render
   */
  private renderUpdate(): void {
    // save layout
    var layout = this.cy.layout({
      name: 'random'
    });

    this.cy = cytoscape({
      container: this.renderElement, // container to render in
      elements: this.elementsArr,
      style: this.style,
      layout: { name: 'random' }
    });

    cytoscape.warnings(false);

    //this.cy.layout = layout;
    layout.run();

    // set up listeners
    this.listenToCanvasDoubleClick();
    this.listenToSingleClick();
  }

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

  private listenToSingleClick(): void {
    this.cy.bind('tap', (evt) => {


      // clicked on a node
      if (evt.target?.isNode && evt.target?.isNode()) {
        // current selected target
        this.handleNodeSingleClick(evt);
      }

      // clicked on an edge
      if (evt.target?.isEdge && evt.target?.isEdge()) {
      }

      this.setSelectedItem(evt)
    });
  }

  /**
   * Bring the whole network into view
   */
  public resetView(): void {
    this.cy.fit(null, 200);
  }

  private handleNodeSingleClick(evt: cytoscape.EventObject): void {// create edge if current selection was a node
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

    if (!node) {
      const nodeId: string = uuid();
      // add to network

      this.cy.add({
        data: {
          id: nodeId,
          x_pos: x,
          y_pos: y
        },
        position: { x: x, y: y }
      });

      // add node to network
      this.network.addNode(nodeId, x, y)
      return;
    }

    this.cy.add({
      data: {
        id: node?.uuid,
        name: node?.name,
        high_value_node: node?.high_value_node,
        entry_node: node?.entry_node,
        classes: node?.classes,
        x_pos: node?.x_pos,
        y_pos: node?.y_pos
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
  public createEdge(edgeId: string, nodeA: string, nodeB: string): void {
    // check if nodes already have connection
    if (this.areNodesConnected(nodeA, nodeB)) {
      return;
    }

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
    // if there is an existing selected item, restore its style
    if (this.selectedElement) {
      this.cy.getElementById(this.selectedElement.id).style(this.defaultNodeStyle)
    }

    // check if an element was clicked
    if (!evt || !evt.target || !evt.target.isNode || !evt.target.isEdge) {
      // clicked on background
      this.selectedElement = null;
      this.selectedElementSubject.next(this.selectedElement);
      return;
    }

    // highlight element
    evt.target.style(this.highlightedNodeStyle);

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
