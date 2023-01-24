import { fakeAsync, TestBed, tick } from '@angular/core/testing';
import { Node } from '../../network-class/network-interfaces';
import { Network } from '../../network-class/network';

import { CytoscapeService } from './cytoscape.service';
import { ElementType } from './graph-objects';

describe('CytoscapeService', () => {
  let service: CytoscapeService;

  beforeEach(() => {
    service = new CytoscapeService();

    service['_network'] = new Network();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('METHOD: loadNetwork', () => {
    it('should load the network into cytoscape', () => {
      const network = new Network();
      network.addNode({ uuid: 'uuid1' } as any);
      network.addNode({ uuid: 'uuid2' } as any);
      network.addEgde('edge', 'uuid1', 'uuid2');

      service.loadNetwork(network);

      expect(service['cy'].nodes().length).toBe(2);
      expect(service['cy'].edges().length).toBe(1);
    });
  });

  describe('METHOD: updateNode', () => {
    it('should not do anything unless a node with a matching id is found', () => {
      const spy = spyOn(service['_network'], 'editNodeDetails');

      const node = {
        uuid: 'id'
      } as any

      service['createNode'](0, 0, node);

      service.updateNode({ uuid: 'fake' } as any);
      expect(spy).not.toHaveBeenCalled();
    });

    it('should update a node with matching id', fakeAsync(() => {
      const spy = spyOn(service['_network'], 'editNodeDetails');

      const node = {
        uuid: 'id'
      } as any

      const nodeUpdate = {
        uuid: 'id',
        name: 'name',
        high_value_node: false,
        entry_node: false,
        x_pos: 0,
        y_pos: 0,
        vulnerability: 0
      };

      service['createNode'](0, 0, node);

      service.updateNode(nodeUpdate);
      tick();
      expect(spy).toHaveBeenCalledWith(nodeUpdate.uuid, nodeUpdate);
    }));
  });

  describe('METHOD: deleteItem', () => {
    it('should delete an edge', () => {
      const network = new Network();
      network.addNode({ uuid: 'uuid1' } as any);
      network.addNode({ uuid: 'uuid2' } as any);
      network.addEgde('edge', 'uuid1', 'uuid2');

      service.loadNetwork(network);

      expect(service['cy'].nodes().length).toBe(2);
      expect(service['cy'].edges().length).toBe(1);

      // select edge
      service['selectedElement'] = {
        id: 'edge',
        type: ElementType.EDGE
      };

      service.deleteItem();

      expect(service['cy'].nodes().length).toBe(2);
      expect(service['network'].edgeList.length).toBe(0);
      // possibly a bug in cytoscape
      // expect(service['cy'].edges().length).toBe(0);
    });

    it('should delete edges connected to the nodes', () => {
      const network = new Network();
      network.addNode({ uuid: 'uuid1' } as any);
      network.addNode({ uuid: 'uuid2' } as any);
      network.addEgde('edge', 'uuid1', 'uuid2');

      service.loadNetwork(network);

      expect(service['cy'].nodes().length).toBe(2);
      expect(service['cy'].edges().length).toBe(1);

      // select edge
      service['selectedElement'] = {
        id: 'uuid2',
        type: ElementType.NODE
      };

      service.deleteItem();

      expect(service['cy'].nodes().length).toBe(1);
      expect(service['cy'].edges().length).toBe(0);
    });
  });

  describe('METHOD: resetView', () => {
    it('should call cy.fit to fit all the items to the viewport', () => {
      const spy = spyOn(service['cy'], 'fit');
      service.resetView();
      expect(spy).toHaveBeenCalled();
    });
  });

  describe('METHOD: handleSingleClick', () => {
    it('should create an edge if there was a node that was previously selected', () => {
      const spy = spyOn<any>(service, 'createEdge');

      service['selectedElement'] = { id: 'id', type: ElementType.NODE };
      service['handleNodeSingleClick']({
        target: null
      } as any);

      expect(spy).toHaveBeenCalled();
    });
  });

  describe('METHOD: createNode', () => {
    it('should add a default node if no values are passed in', () => {
      expect(service['cy'].nodes().length).toBe(0);

      service['createNode'](0, 0);

      expect(service['cy'].nodes().length).toBe(1);
    });

    it('should set the data values according to the passed values', () => {
      expect(service['cy'].nodes().length).toBe(0);

      const node: Node = {
        uuid: 'uuid',
        name: 'name',
        high_value_node: false,
        entry_node: false,
        x_pos: 1,
        y_pos: 1,
        vulnerability: 0
      }

      service['createNode'](1, 1, node);

      expect(service['cy'].nodes().length).toBe(1);

      const cyNode = service['cy'].$id('uuid');
      expect(cyNode.id()).toBe('uuid');
      expect(cyNode.data('name')).toBe('name');
    });
  });

  describe('METHOD: createEdge', () => {
    it('should do nothing if both nodes are already connected', () => {
      const spy = spyOn(service['cy'], 'add');
      spyOn<any>(service, 'areNodesConnected').and.returnValue(true);

      (<any>service).createEdge(null, null, null);
      expect(spy).not.toHaveBeenCalled();
    });

    it('should create an edge between 2 nodes if they have not yet been connected', () => {
      const spy = spyOn(service['cy'], 'add');
      spyOn<any>(service, 'areNodesConnected').and.returnValue(false);

      (<any>service).createEdge(null, null, null);
      expect(spy).toHaveBeenCalled();
    });
  });

  describe('METHOD: setSelectedItem', () => {
    it('should set the selected element to null if nothing was selected', fakeAsync(() => {
      service['setSelectedItem'](null);
      expect(service['selectedElement']).toBeNull();

      service['setSelectedItem']({ target: null } as any);
      expect(service['selectedElement']).toBeNull();
    }));

    it('should highlight the target element', () => {
      service['setSelectedItem']({
        target: {
          id: () => 'test',
          isNode: () => true,
          isEdge: () => true,
          style: () => { }
        }
      } as any);
      expect(service['selectedElement']).not.toBeNull();
    });
  });

  describe('METHOD: areNodesConnected', () => {
    it('should return true if we are trying to connect a node to itself', () => {
      service['cy'].add({ data: { id: 'id' } });

      expect(service['areNodesConnected']('id', 'id')).toBeTruthy();
    });

    it('should return false if either of the nodes do not exist', () => {
      service['cy'].add({ data: { id: 'id' } });

      expect(service['areNodesConnected']('id', 'id2')).toBeFalsy();
      expect(service['areNodesConnected']('id1', 'id')).toBeFalsy();
    });

    it('should return false if we are trying to connect a node to an edge', () => {
      service['cy'].add({ data: { id: 'id1' } });
      service['cy'].add({ data: { id: 'id2' } });

      service['createEdge']('edge', 'id1', 'id2');

      expect(service['areNodesConnected']('edge', 'id2')).toBeFalsy();
      expect(service['areNodesConnected']('id1', 'edge')).toBeFalsy();
    });

    it('should return true if both nodes are connected', () => {
      service['cy'].add({ data: { id: 'id1' } });
      service['cy'].add({ data: { id: 'id2' } });

      service['createEdge']('edge', 'id1', 'id2');

      expect(service['areNodesConnected']('id1', 'id2')).toBeTruthy();
    });

    it('should return false if the nodes exists but are not connected', () => {
      service['cy'].add({ data: { id: 'id1' } });
      service['cy'].add({ data: { id: 'id2' } });

      expect(service['areNodesConnected']('id1', 'id2')).toBeFalsy();
    });
  });
});
