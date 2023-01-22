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

      expect(network.documentMetadata).toEqual({
        uuid: test_network._doc_metadata.uuid,
        created_at: new Date(test_network._doc_metadata.created_at),
        updated_at: null,
        name: test_network._doc_metadata.name,
        description: test_network._doc_metadata.description,
        author: test_network._doc_metadata.author,
        locked: test_network._doc_metadata.locked
      })
    });
  });

  describe('METHOD: addEdge', () => {
    it('should not do anything if the nodes do not exist', () => {
      const network = new Network();

      network.addEgde('id', 'fakeNodeA', 'fakeNodeB');

      expect(network.edgeList.length).toBe(0);
    });

    it('should add edges between 2 nodes', () => {
      const network = new Network();
      // add 2 nodes
      network.addNode({uuid: 'uuid1'} as any);
      network.addNode({uuid: 'uuid2'} as any);

      network.addEgde('edgeid', 'uuid1', 'uuid2');

      expect(network.edgeList.length).toBe(1);
    });
  });

  describe('METHOD: addNode', () => {
    it('should add the node if it does not exist', () => {
      const network = new Network();
      network.addNode({uuid: 'uuid1'} as any);

      expect(network.nodeList.length).toBe(1);
    });

    it('should not add the node if it already exists', () => {
      const network = new Network();
      network.addNode({uuid: 'uuid1'} as any);
      expect(network.nodeList.length).toBe(1);

      network.addNode({uuid: 'uuid1'} as any);
      expect(network.nodeList.length).toBe(1);
    });
  });

  describe('METHOD: removeEdge', () => {
    it('should remove the edge with the matching id', () => {
      const network = new Network();
      // add 2 nodes
      network.addNode({uuid: 'uuid1'} as any);
      network.addNode({uuid: 'uuid2'} as any);

      network.addEgde('edgeid', 'uuid1', 'uuid2');
      expect(network.edgeList.length).toBe(1);
      network.removeEdge('edgeid');
      expect(network.edgeList.length).toBe(0);
    });
  });

  describe('METHOD: removeNode', () => {
    it('should remove a node and any edges pointing to it', fakeAsync(() => {
      const network = new Network();
      // add 2 nodes
      network.addNode({uuid: 'uuid1'} as any);
      network.addNode({uuid: 'uuid2'} as any);
      expect(network.nodeList.length).toBe(2);

      network.addEgde('edgeid', 'uuid1', 'uuid2');
      expect(network.edgeList.length).toBe(1);

      // remove node 2
      network.removeNode('uuid2');
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
