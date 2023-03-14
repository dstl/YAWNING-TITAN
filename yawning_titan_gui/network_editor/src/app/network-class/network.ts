import { NetworkDocMetadata, NetworkJson, NetworkSettings, Node, RandomEntryNodePreference, RandomHighValueNodePreference } from "./network-interfaces";
import { v4 as uuid } from 'uuid';
import { EdgeObj } from "../services/cytoscape/graph-objects";
import { roundNumber } from "../utils/utils";

export class Network {
  nodeList: Node[] = [];
  edgeList: { edgeId: string, nodeA: string, nodeB: string }[] = [];

  // network settings
  private _networkSettings: NetworkSettings;
  get networkSettings(): NetworkSettings {
    return this._networkSettings;
  }

  // document metadata
  private _documentMetadata: NetworkDocMetadata;
  get documentMetadata(): NetworkDocMetadata {
    return this._documentMetadata;
  }

  constructor(json?: any) {
    // if not able to load from JSON, set defaults
    if (!json) {
      this.setDefaultValues();
      return;
    }
    this.loadFromJson(json);
  }

  /**
   * Get node properties via id
   * @param id
   * @returns
   */
  public getNodeById(id: string): Node {
    if (!this.nodeList || !this.nodeList.length) {
      return null;
    }

    return this.nodeList.find(node => node.uuid == id);
  }

  /**
   * Load the network details from the JSON object
   * @param json
   * @returns
   */
  public loadFromJson(json: NetworkJson) {
    // check that the necessary properties exist
    if (
      !json.nodes || !json._doc_metadata
    ) {
      return;
    }

    // load network settings
    this.loadNetworkSettings(json);

    // load nodes
    this.loadNodesFromJson(json?.nodes);

    // load edges between nodes
    this.loadEdgesFromJson(json?.edges);

    // load the network's doc metadata
    this.loadNetworkDocMetadataFromJson(json?._doc_metadata)
  }

  /**
   * Sets the default values for metadata and network settings
   */
  private setDefaultValues() {
    this._networkSettings = {
      entryNode: {
        set_random_entry_nodes: false,
        random_entry_node_preference: RandomEntryNodePreference.NONE,
        num_of_random_entry_nodes: 0
      },
      highValueNode: {
        set_random_high_value_nodes: false,
        random_high_value_node_preference: RandomHighValueNodePreference.NONE,
        num_of_random_high_value_nodes: 0
      },
      vulnerability: {
        set_random_vulnerabilities: false,
        node_vulnerability_upper_bound: 1,
        node_vulnerability_lower_bound: 0
      }
    }

    this._documentMetadata = {
      uuid: uuid(),
      created_at: new Date(),
      updated_at: null,
      name: '',
      description: '',
      author: '',
      locked: false
    }
  }

  /**
   * Updates the network settings
   * @param networkSettings
   */
  public updateNetworkSettings(networkSettings: NetworkSettings) {
    this._networkSettings = networkSettings;
  }

  /**
   * Set the relevant network settings
   * @param network
   */
  private loadNetworkSettings(network: NetworkJson) {
    this._networkSettings = {
      entryNode: {
        set_random_entry_nodes: network?.set_random_entry_nodes,
        random_entry_node_preference: network?.random_entry_node_preference,
        num_of_random_entry_nodes: network?.num_of_random_entry_nodes
      },
      highValueNode: {
        set_random_high_value_nodes: network?.set_random_high_value_nodes,
        random_high_value_node_preference: network?.random_high_value_node_preference,
        num_of_random_high_value_nodes: network?.num_of_random_high_value_nodes
      },
      vulnerability: {
        set_random_vulnerabilities: network?.set_random_vulnerabilities,
        node_vulnerability_lower_bound: network?.node_vulnerability_lower_bound,
        node_vulnerability_upper_bound: network?.node_vulnerability_upper_bound
      }
    }
  }

  /**
   * Adds the nodes in the JSON object into the nodeList
   * @param nodes
   * @returns
   */
  private loadNodesFromJson(nodes = {}): void {
    const jsonNodes = Object.keys(nodes ? nodes : {});

    // do nothing if there are no nodes to load
    if (!jsonNodes?.length) {
      return;
    }

    jsonNodes.forEach(nodeUUID => {
      this.nodeList.push({
        uuid: nodes[`${nodeUUID}`]?.uuid,
        name: nodes[`${nodeUUID}`]?.name,
        high_value_node: nodes[`${nodeUUID}`]?.high_value_node,
        entry_node: nodes[`${nodeUUID}`]?.entry_node,
        x_pos: roundNumber(nodes[`${nodeUUID}`]?.x_pos, 0),
        y_pos: roundNumber(nodes[`${nodeUUID}`]?.y_pos, 0),
        vulnerability: roundNumber(nodes[`${nodeUUID}`]?.vulnerability),
      });
    });
  }

  /**
   * Adds the edges in the JSON object into the edgeList
   * @param edges
   * @returns
   */
  private loadEdgesFromJson(edges: any): void {
    const jsonEdges = Object.keys(edges ? edges : {});

    // do nothing if there are no edges to load
    if (!jsonEdges?.length) {
      return;
    }

    jsonEdges.forEach(nodeAuuid => {
      Object.keys(
        edges[`${nodeAuuid}`] ? edges[`${nodeAuuid}`] : {}
      ).forEach(nodeBuuid => this.addEgde({
        edgeId: uuid(),
        nodeA: nodeAuuid,
        nodeB: nodeBuuid
      }));
    });
  }

  /**
   * Set the network metadata from the JSON object
   * @param docMd
   * @returns
   */
  private loadNetworkDocMetadataFromJson(docMd: any): void {
    if (!docMd) {
      return;
    }

    this._documentMetadata = {
      uuid: docMd.uuid,
      created_at: new Date(docMd.created_at),
      updated_at: docMd.updatedAt ? new Date(docMd.updated_at) : null,
      name: docMd.name,
      description: docMd.description,
      author: docMd.author,
      locked: docMd.locked
    }
  }

  /**
   * Adds an edge between 2 nodes
   * @param nodeAID
   * @param nodeBID
   * @returns true when successful
   */
  public addEgde(edgeObj: EdgeObj): EdgeObj {
    // check that node A exists
    const nodeA = this.nodeList.find(node => node.uuid == edgeObj?.nodeA);

    // check that node B exists
    const nodeB = this.nodeList.find(node => node.uuid == edgeObj?.nodeB);

    if (!nodeA || !nodeB || nodeA == nodeB) {
      return;
    }

    // check that the connection does not exist already
    const aTob = this.edgeList.find(edge => edge.nodeA === nodeA.uuid && edge.nodeB == nodeB.uuid);
    const bToa = this.edgeList.find(edge => edge.nodeB === nodeA.uuid && edge.nodeA == nodeB.uuid);

    if (aTob || bToa) {
      return;
    }

    const edge = {
      edgeId: edgeObj?.edgeId ? edgeObj.edgeId : uuid(),
      nodeA: nodeA.uuid,
      nodeB: nodeB.uuid
    }

    this.edgeList.push(edge);

    return edge;
  }

  /**
   * Adds a node to the network
   * @param uuid
   * @param x_pos
   * @param y_pos
   * @returns true when successful
   */
  public addNode(x: number, y: number, nodeCount: number, nodeProperties?: Node): Node {
    // if no node properties are provided, create an empty node and add to network
    if (!nodeProperties) {
      nodeProperties = {
        uuid: uuid(),
        name: `node ${nodeCount}`,
        entry_node: false,
        high_value_node: false,
        x_pos: roundNumber(x, 0),
        y_pos: roundNumber(y, 0),
        vulnerability: 0
      }
    }

    // if uuid already exists, return
    if (!nodeProperties || !nodeProperties.uuid ||
      this.nodeList.find(node => node.uuid === nodeProperties.uuid)) {
      return;
    }

    const node = {
      uuid: nodeProperties.uuid,
      name: nodeProperties.name,
      high_value_node: nodeProperties.high_value_node,
      entry_node: nodeProperties.entry_node,
      x_pos: nodeProperties.x_pos,
      y_pos: nodeProperties.y_pos,
      vulnerability: nodeProperties.vulnerability
    }

    this.nodeList.push(node);

    return node;
  }

  /**
   * Edit the details of a given node uuid
   * @param uuid
   * @param details
   */
  public editNodeDetails(details: Node): Node {
    const matchingNode = this.nodeList.findIndex(node => node.uuid === details?.uuid);

    // find index returns -1 if matching node is not found
    if (matchingNode < 0) {
      return;
    }

    this.nodeList[matchingNode] = {
      uuid: details.uuid,
      name: details.name,
      entry_node: details.entry_node,
      high_value_node: details.high_value_node,
      vulnerability: roundNumber(details?.vulnerability, 6),
      x_pos: roundNumber(details?.x_pos),
      y_pos: roundNumber(details?.y_pos)
    };
    return this.nodeList[matchingNode];
  }

  /**
   * Removes an edge from the edge list
   * @param edgeId
   */
  public removeEdge(edgeId: string): void {
    this.edgeList = this.edgeList.filter(edge => edgeId != edge.edgeId);
  }

  /**
   * Removes a node (and its related edges) from the network
   * @param nodeId
   */
  public removeNode(nodeId: string): void {
    this.nodeList = this.nodeList.filter(node => nodeId != node.uuid);

    // remove the edge that connects to the node
    this.edgeList = this.edgeList.filter(edge => (edge.nodeA != nodeId && edge.nodeB != nodeId))
  }

  /**
   * Return a JSON object representation of the network
   * @returns
   */
  public toJson(): NetworkJson {
    const obj = {
      set_random_entry_nodes: this._networkSettings.entryNode.set_random_entry_nodes,
      random_entry_node_preference: this._networkSettings.entryNode.random_entry_node_preference,
      num_of_random_entry_nodes: this._networkSettings.entryNode.num_of_random_entry_nodes,

      set_random_high_value_nodes: this._networkSettings.highValueNode.set_random_high_value_nodes,
      random_high_value_node_preference: this._networkSettings.highValueNode.random_high_value_node_preference,
      num_of_random_high_value_nodes: this._networkSettings.highValueNode.num_of_random_high_value_nodes,

      set_random_vulnerabilities: this._networkSettings.vulnerability.set_random_vulnerabilities,
      node_vulnerability_lower_bound: this._networkSettings.vulnerability.node_vulnerability_lower_bound,
      node_vulnerability_upper_bound: this._networkSettings.vulnerability.node_vulnerability_upper_bound,

      nodes: this.nodesToJson(),
      edges: this.edgesToJson(),
      _doc_metadata: this.documentMetadata
    }

    return obj;
  }

  /**
   * Get the nodes in the JSON Record format
   * @returns
   */
  private nodesToJson(): Record<string, Node> {
    // convert to Record
    const nodeJson = {};

    // add each node as record
    this.nodeList.forEach(node => nodeJson[`${node.uuid}`] = node)

    return nodeJson;
  }

  /**
   * Get the edges in the JSON Record format
   * @returns
   */
  private edgesToJson(): Record<string, Record<string, any>> {
    // iterate through the nodes and add connected nodes
    const edgeJson = {}

    // iterate through the nodes
    this.nodeList.forEach(node => {
      const connections = this.edgeList.filter(edge => edge.nodeA == node.uuid || edge.nodeB == node.uuid);

      // if node does not have connection, skip
      if (!connections || !connections.length) {
        return;
      }

      const edgeTargets = {};
      // iterate through connections
      connections.forEach(connection => {
        // make sure to add the uuid of the other node, not the current one
        if (connection.nodeA == node.uuid) {
          edgeTargets[`${connection.nodeB}`] = {}
          return;
        }
        edgeTargets[`${connection.nodeA}`] = {}
      })

      // create the edge object
      edgeJson[`${node.uuid}`] = edgeTargets;
    });

    return edgeJson;
  }
}
