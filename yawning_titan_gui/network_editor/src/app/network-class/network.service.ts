import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { Network } from './network';
import { NetworkJson, NetworkSettings, Node } from './network-interfaces';
import { CytoscapeService } from '../services/cytoscape/cytoscape.service';
import { EdgeObj, ElementType, SelectedGraphRef } from '../services/cytoscape/graph-objects';

@Injectable({
  providedIn: 'root'
})
export class NetworkService {

  // instance of network
  private _network = new Network();

  // keep count of the number of nodes in the network
  private nodeCount = 0;

  /**
   * Observable for network and its updates
   */
  private _networkSubject = new BehaviorSubject<Network>(this._network);
  get networkObservable(): Observable<Network> {
    return this._networkSubject.asObservable();
  }

  constructor(
    private cytoscapeService: CytoscapeService
  ) { }

  /**
   * Set the passed network as the new network
   * @param network
   */
  public loadNetwork(network: Network): void {
    this.nodeCount = 0;
    this._network = network;
    this.cytoscapeService.loadNetwork(network);
    this._networkSubject.next(this._network);
  }

  /**
   * Updates the current network's settings
   * @param networkSettings
   */
  public updateNetworkSettings(networkSettings: NetworkSettings) {
    if (!networkSettings) {
      return;
    }

    this._network.updateNetworkSettings(networkSettings);

    // apply settings to nodes
    this.applyNetworkSettingsToNodes(networkSettings);

    this._networkSubject.next(this._network);
  }

  /**
   * Sets relevant node properties to false depending on network settings
   */
  private applyNetworkSettingsToNodes(networkSettings: NetworkSettings): void {
    this._network.nodeList.forEach(node => {
      node = {
        uuid: node.uuid,
        name: node.name,
        x_pos: node.x_pos,
        y_pos: node.y_pos,
        vulnerability: networkSettings.vulnerability.set_random_vulnerabilities ?
          networkSettings.vulnerability.node_vulnerability_lower_bound : node.vulnerability,
        entry_node: networkSettings.entryNode.set_random_entry_nodes ? false : node.entry_node,
        high_value_node: networkSettings.highValueNode.set_random_high_value_nodes ? false : node.high_value_node
      }

      this.editNodeDetails(node);
    });
  }

  /**
   * Adds a node to the network
   * @param x
   * @param y
   * @param nodeCount
   * @param node
   * @returns
   */
  public addNode(x: number, y: number, node?: Node): Node {
    this.nodeCount++;
    const result = this._network.addNode(x, y, this.nodeCount, node);

    // check if node was created
    if (!result) {
      return;
    }

    // render node
    this.cytoscapeService.createCytoscapeNode(result.x_pos, result.y_pos, result);

    this._networkSubject.next(this._network);
    return result;
  }

  /**
   * Edit the details of a node with specified id
   * @param id
   * @param nodeDetails
   * @returns
   */
  public editNodeDetails(nodeDetails: Node): Node {
    const res = this._network.editNodeDetails(nodeDetails);

    if (!res) {
      return;
    }

    // render updated node
    this.cytoscapeService.updateCytoscapeNode(res);
    this._networkSubject.next(this._network);
    return res;
  }

  /**
   * Remove an item from the network
   * @param item
   * @returns
   */
  public removeItem(item: SelectedGraphRef) {
    if (!item) {
      return;
    }

    // check the type of item to be remove
    switch (item.type) {
      case ElementType.EDGE:
        this.removeEdge(item.id);
        break;

      case ElementType.NODE:
        this.removeNode(item.id);
        break;

      default:
        break;
    }
  }

  /**
   * Remove a node with specified id
   * @param id
   */
  private removeNode(id: string): void {
    this._network.removeNode(id);
    this._networkSubject.next(this._network);
    this.cytoscapeService.removeCytoscapeNode(id);
  }

  /**
   * Returns the details of a node with a matching id
   * @param id
   * @returns
   */
  public getNodeById(id): Node {
    const res = this._network.getNodeById(id);
    this._networkSubject.next(this._network);
    return res;
  }

  /**
   * Add an edge between 2 nodes
   * @param edgeId
   * @param nodeA
   * @param nodeB
   */
  public addEdge(edge: EdgeObj): EdgeObj {
    const res = this._network.addEgde(edge);

    // check if edge created
    if (!res) {
      return;
    }

    // render edge
    this.cytoscapeService.createCytoscapeEdge(res.edgeId, res.nodeA, res.nodeB);

    this._networkSubject.next(this._network);
    return res;
  }

  /**
   * Remove an edge with specified id
   * @param id
   */
  private removeEdge(id: string): void {
    this._network.removeEdge(id);
    this._networkSubject.next(this._network);
    this.cytoscapeService.removeCytoscapeEdge(id);
  }

  /**
   * Get the network as JSON format
   * @returns
   */
  public getNetworkJson(): NetworkJson {
    return this._network.toJson();
  }
}
