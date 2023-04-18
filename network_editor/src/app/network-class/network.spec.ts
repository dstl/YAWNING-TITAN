import { Network } from './network';
import { test_network } from '../../testing/test-network';
import { fakeAsync, tick } from '@angular/core/testing';

describe('Network', () => {

  it('should create an instance', () => {
    expect(new Network()).toBeTruthy();
  });

  it('should load the json if the class was instantiated with a json parameter', () => {
    const spy = spyOn(Network.prototype, 'loadFromJson').and.callFake(() => { });

    new Network({});
    expect(spy).toHaveBeenCalled();
  });

  it('should not call loadFromJson if empty network is instantiated', () => {
    const spy = spyOn(Network.prototype, 'loadFromJson').and.callFake(() => { });

    new Network();
    expect(spy).not.toHaveBeenCalled();
  });

  describe('METHOD: getNodeById', () => {
    it('should return null if no node is found', () => {
      const network = new Network();
      expect(network.getNodeById('id')).toBeNull();
    });

    it('should return the correct node details', () => {
      const network = new Network();
      const node = {
        uuid: 'id',
        name: 'name',
        high_value_node: false,
        entry_node: false,
        x_pos: 0,
        y_pos: 0,
        vulnerability: 0
      };

      network.addNode(node.x_pos, node.y_pos, 0, node);

      expect(network.getNodeById('id')).toEqual(node)
    });
  });

  describe('METHOD: loadFromJson', () => {
    it('should do nothing if the JSON object does not have any nodes and a doc metadata to load', () => {
      const loadNodeSpy = spyOn<any>(Network.prototype, 'loadNodesFromJson').and.callFake(() => { });
      const loadEdgeSpy = spyOn<any>(Network.prototype, 'loadEdgesFromJson').and.callFake(() => { });
      const loadMdSpy = spyOn<any>(Network.prototype, 'loadNetworkDocMetadataFromJson').and.callFake(() => { });

      const network = new Network();
      network.loadFromJson({} as any);
      expect(loadNodeSpy).not.toHaveBeenCalled();
      expect(loadEdgeSpy).not.toHaveBeenCalled();
      expect(loadMdSpy).not.toHaveBeenCalled();
    });

    it('should parse the json', () => {
      const loadNodeSpy = spyOn<any>(Network.prototype, 'loadNodesFromJson').and.callFake(() => { });
      const loadEdgeSpy = spyOn<any>(Network.prototype, 'loadEdgesFromJson').and.callFake(() => { });
      const loadMdSpy = spyOn<any>(Network.prototype, 'loadNetworkDocMetadataFromJson').and.callFake(() => { });

      const network = new Network();
      network.loadFromJson(test_network as any);
      expect(loadNodeSpy).toHaveBeenCalledWith(test_network.nodes);
      expect(loadEdgeSpy).toHaveBeenCalledWith(test_network.edges);
      expect(loadMdSpy).toHaveBeenCalledWith(test_network._doc_metadata);
    });
  });

  describe('METHOD: loadNodesFromJson', () => {
    it('should do nothing if there are no nodes', () => {
      const network = new Network();
      network['loadNodesFromJson'](null);

      expect(network.nodeList).toEqual([]);
    });

    it('should add nodes to the node list', () => {
      const network = new Network();
      network['loadNodesFromJson'](test_network.nodes);

      expect(network.nodeList.length).toBe(18);
    });
  });

  describe('METHOD: loadEdgesFromJson', () => {
    it('should do nothing if there are no edges', () => {
      const network = new Network();
      network['loadEdgesFromJson'](null);

      expect(network.nodeList).toEqual([]);
    });

    it('should add edges to the edge list', () => {
      const addEgdeSpy = spyOn(Network.prototype, 'addEgde').and.callThrough();
      const network = new Network();
      network['loadNodesFromJson'](test_network.nodes);
      network['loadEdgesFromJson'](test_network.edges);

      expect(addEgdeSpy).toHaveBeenCalledTimes(34);
      expect(network.edgeList.length).toBe(17);
    });
  });

  describe('METHOD: loadNetworkDocMetadataFromJson', () => {
    it('should load the network metadata', () => {
      const network = new Network(test_network);

      expect(network.documentMetadata.uuid).toEqual(test_network._doc_metadata.uuid);
      expect(network.documentMetadata.name).toEqual(test_network._doc_metadata.name);
      expect(network.documentMetadata.description).toEqual(test_network._doc_metadata.description);
      expect(network.documentMetadata.author).toEqual(test_network._doc_metadata.author);
      expect(network.documentMetadata.locked).toEqual(test_network._doc_metadata.locked);
      expect(network.documentMetadata.created_at).toEqual(test_network._doc_metadata.created_at);
    });
  });

  describe('METHOD: addEdge', () => {
    it('should not do anything if the nodes do not exist', () => {
      const network = new Network();

      network.addEgde({ edgeId: 'id', nodeA: 'fakeNodeA', nodeB: 'fakeNodeB' });

      expect(network.edgeList.length).toBe(0);
    });

    it('should add edges between 2 nodes', () => {
      const network = new Network();

      const nodeA = {
        uuid: 'idA',
        name: 'nameA',
        high_value_node: false,
        entry_node: false,
        x_pos: 0,
        y_pos: 0,
        vulnerability: 0
      };

      const nodeB = {
        uuid: 'idB',
        name: 'nameB',
        high_value_node: false,
        entry_node: false,
        x_pos: 10,
        y_pos: 10,
        vulnerability: 0
      };

      // add 2 nodes
      network.addNode(nodeA.x_pos, nodeA.y_pos, 0, nodeA);
      network.addNode(nodeB.x_pos, nodeB.y_pos, 0, nodeB);

      network.addEgde({ edgeId: 'edgeid', nodeA: nodeA.uuid, nodeB: nodeB.uuid });

      expect(network.edgeList.length).toBe(1);
    });
  });

  describe('METHOD: addNode', () => {
    const node = {
      uuid: 'id',
      name: 'name',
      high_value_node: false,
      entry_node: false,
      x_pos: 0,
      y_pos: 0,
      vulnerability: 0
    };

    it('should add the node if it does not exist', () => {
      const network = new Network();
      network.addNode(node.x_pos, node.y_pos, 0, node);

      expect(network.nodeList.length).toBe(1);
    });

    it('should not add the node if it already exists', () => {
      const network = new Network();
      network.addNode(node.x_pos, node.y_pos, 0, node);
      expect(network.nodeList.length).toBe(1);

      network.addNode(node.x_pos, node.y_pos, 0, node);
      expect(network.nodeList.length).toBe(1);
    });
  });

  describe('METHOD: editNodeDetails', () => {
    it('should change nothing if the node is not found', () => {
      const network = new Network();

      network.editNodeDetails({
        uuid: 'id',
        name: 'name',
        high_value_node: false,
        entry_node: false,
        x_pos: 0,
        y_pos: 0,
        vulnerability: 0
      });

      expect(network.nodeList).toEqual([]);
    });

    it('should change the correct node', () => {
      const base = {
        name: 'name',
        high_value_node: false,
        entry_node: false,
        x_pos: 0,
        y_pos: 0,
        vulnerability: 0
      }

      const node1 = {
        uuid: 'id1',
        ...base
      }

      const node2 = {
        uuid: 'id2',
        ...base
      }

      const update = {
        uuid: 'id2',
        name: 'updates',
        high_value_node: true,
        entry_node: true,
        x_pos: 10,
        y_pos: 10,
        vulnerability: 0.5
      }

      const network = new Network();
      network.addNode(node1.x_pos, node1.y_pos, 0, node1);
      network.addNode(node2.x_pos, node2.y_pos, 1, node2);
      expect(network.nodeList).toEqual([node1, node2]);

      // update node 2
      network.editNodeDetails(update);
      expect(network.nodeList).toEqual([node1, update]);
    });
  });

  describe('METHOD: removeEdge', () => {
    it('should remove the edge with the matching id', () => {
      const base = {
        name: 'name',
        high_value_node: false,
        entry_node: false,
        x_pos: 0,
        y_pos: 0,
        vulnerability: 0
      }

      const node1 = {
        uuid: 'id1',
        ...base
      }

      const node2 = {
        uuid: 'id2',
        ...base
      }

      const network = new Network();
      // add 2 nodes
      network.addNode(node1.x_pos, node1.y_pos, 0, node1);
      network.addNode(node2.x_pos, node2.y_pos, 1, node2);

      network.addEgde({ edgeId: 'edgeid', nodeA: node1.uuid, nodeB: node2.uuid });
      expect(network.edgeList.length).toBe(1);
      network.removeEdge('edgeid');
      expect(network.edgeList.length).toBe(0);
    });
  });

  describe('METHOD: removeNode', () => {
    it('should remove a node and any edges pointing to it', fakeAsync(() => {
      const base = {
        name: 'name',
        high_value_node: false,
        entry_node: false,
        x_pos: 0,
        y_pos: 0,
        vulnerability: 0
      }

      const node1 = {
        uuid: 'id1',
        ...base
      }

      const node2 = {
        uuid: 'id2',
        ...base
      }

      const network = new Network();
      // add 2 nodes
      network.addNode(node1.x_pos, node1.y_pos, 0, node1);
      network.addNode(node2.x_pos, node2.y_pos, 1, node2);
      expect(network.nodeList.length).toBe(2);

      network.addEgde({ edgeId: 'edgeid', nodeA: node1.uuid, nodeB: node2.uuid });
      expect(network.edgeList.length).toBe(1);

      // remove node 2
      network.removeNode('id2');
      tick();
      expect(network.nodeList.length).toBe(1);
      expect(network.edgeList.length).toBe(0);
      expect(!!network.nodeList.find(node => node.uuid == 'uuid2')).toBeFalsy();
    }));
  });

  describe('METHOD: toJson', () => {
    it('should return the network as a JSON object', () => {
      const nodeSpy = spyOn<any>(Network.prototype, 'nodesToJson').and.callThrough();
      const edgeSpy = spyOn<any>(Network.prototype, 'edgesToJson').and.callThrough();

      const network = new Network(test_network);
      const json = network.toJson();
      expect(nodeSpy).toHaveBeenCalled();
      expect(edgeSpy).toHaveBeenCalled();
      expect(json.nodes["64265a12-5201-4bc8-82db-927c24d03363"]).toEqual(test_network.nodes["64265a12-5201-4bc8-82db-927c24d03363"]);
    });
  });
});
