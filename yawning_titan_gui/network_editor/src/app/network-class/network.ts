import { NetworkDocMetadata, NetworkJson, Node } from "./network-interfaces";
import { v4 as uuid } from 'uuid';

export class Network {
  nodeList: Node[] = [];
  edgeList: { edgeId: string, nodeA: string, nodeB: string }[] = [];
  documentMetadata: NetworkDocMetadata;

  constructor(json?: any) {
    // if not able to load from JSON, do nothing
    if (!json) {
      return;
    }

    this.loadFromJson(json);
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

    // load nodes
    this.loadNodesFromJson(json?.nodes);

    // load edges between nodes
    this.loadEdgesFromJson(json?.edges);

    // load the network's doc metadata
    this.loadNetworkDocMetadataFromJson(json?._doc_metadata)
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
        classes: nodes[`${nodeUUID}`]?.classes,
        x_pos: nodes[`${nodeUUID}`]?.x_pos,
        y_pos: nodes[`${nodeUUID}`]?.y_pos,
        vulnerability: nodes[`${nodeUUID}`]?.vulnerability,
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
      ).forEach(nodeBuuid => this.addEgde(uuid(), nodeAuuid, nodeBuuid));
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

    this.documentMetadata = {
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
  public addEgde(edgeId: string, nodeAID: string, nodeBID: string): boolean {
    // check that node A exists
    const nodeA = this.nodeList.find(node => node.uuid == nodeAID);

    // check that node B exists
    const nodeB = this.nodeList.find(node => node.uuid == nodeBID);

    if (!nodeA || !nodeB || nodeA == nodeB) {
      return;
    }

    // check that the connection does not exist already
    const aTob = this.edgeList.find(edge => edge.nodeA === nodeA.uuid && edge.nodeB == nodeB.uuid);
    const bToa = this.edgeList.find(edge => edge.nodeB === nodeA.uuid && edge.nodeA == nodeB.uuid);

    if (aTob || bToa) {
      return;
    }

    this.edgeList.push({ edgeId: edgeId, nodeA: nodeA.uuid, nodeB: nodeB.uuid });

    return true;
  }

  /**
   * Adds a node to the network
   * @param uuid
   * @param x_pos
   * @param y_pos
   * @returns true when successful
   */
  public addNode(uuid: string, x_pos: number, y_pos: number): boolean {
    // if uuid already exists, return
    if (this.nodeList.find(node => node.uuid === uuid)) {
      return;
    }

    this.nodeList.push({
      uuid: uuid,
      name: null,
      high_value_node: false,
      entry_node: false,
      classes: "standard_node",
      x_pos: x_pos,
      y_pos: y_pos,
      vulnerability: 0
    });

    return true;
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
