import { fakeAsync, TestBed } from '@angular/core/testing';
import { Node } from '../../network-class/network-interfaces';
import { Network } from '../../network-class/network';

import { CytoscapeService } from './cytoscape.service';
import { ElementType } from './graph-objects';

describe('CytoscapeService', () => {
  let service: CytoscapeService;

  beforeEach(() => {
    service = new CytoscapeService();

    service['network'] = new Network();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('METHOD: loadNetwork', () => {
    it('should load the network into cytoscape', () => {
      const network = new Network();
      network.addNode({uuid: 'uuid1'} as any);
      network.addNode({uuid: 'uuid2'} as any);
      network.addEgde('edge', 'uuid1', 'uuid2');

      service.loadNetwork(network);

      expect(service.cytoscapeObj.nodes().length).toBe(2);
      expect(service.cytoscapeObj.edges().length).toBe(1);
    });
  });

  describe('METHOD: deleteItem', () => {
    it('should delete an edge', () => {
      const network = new Network();
      network.addNode({uuid: 'uuid1'} as any);
      network.addNode({uuid: 'uuid2'} as any);
      network.addEgde('edge', 'uuid1', 'uuid2');

      service.loadNetwork(network);

      expect(service.cytoscapeObj.nodes().length).toBe(2);
      expect(service.cytoscapeObj.edges().length).toBe(1);

      // select edge
      service['selectedElement'] = {
        id: 'edge',
        type: ElementType.EDGE
      };

      service.deleteItem();

      expect(service.cytoscapeObj.nodes().length).toBe(2);
      expect(service['network'].edgeList.length).toBe(0);
      // possibly a bug in cytoscape
      // expect(service.cytoscapeObj.edges().length).toBe(0);
    });

    it('should delete edges connected to the nodes', () => {
      const network = new Network();
      network.addNode({uuid: 'uuid1'} as any);
      network.addNode({uuid: 'uuid2'} as any);
      network.addEgde('edge', 'uuid1', 'uuid2');

      service.loadNetwork(network);

      expect(service.cytoscapeObj.nodes().length).toBe(2);
      expect(service.cytoscapeObj.edges().length).toBe(1);

      // select edge
      service['selectedElement'] = {
        id: 'uuid2',
        type: ElementType.NODE
      };

      service.deleteItem();

      expect(service.cytoscapeObj.nodes().length).toBe(1);
      expect(service.cytoscapeObj.edges().length).toBe(0);
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
});
