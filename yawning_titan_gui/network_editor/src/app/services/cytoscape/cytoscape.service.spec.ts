import { Node } from 'src/app/network-class/network-interfaces';
import { Network } from '../../network-class/network';

import { CytoscapeService } from './cytoscape.service';
import { EdgeObj } from './graph-objects';

describe('CytoscapeService', () => {
  let service: CytoscapeService;

  beforeEach(() => {
    service = new CytoscapeService(null);

    service['_network'] = new Network();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should emit double click events', () => {
    service.doubleClickEvent.subscribe(() => expect(true).toBeTrue());
    service['doubleClickSubject'].next(null);
  });

  it('should emit single click events', () => {
    service.singleClickEvent.subscribe(() => expect(true).toBeTrue());
    service['singleClickSubject'].next(null);
  });

  it('should emit drag events', () => {
    service.dragEvent.subscribe(() => expect(true).toBeTrue());
    service['dragSubject'].next(null);
  });

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

  describe('METHOD: loadNetwork', () => {
    it('should load the network into cytoscape', () => {
      const network = new Network();
      network.addNode(node1.x_pos, node1.y_pos, 0, node1);
      network.addNode(node2.x_pos, node2.y_pos, 1, node2);
      network.addEgde({ edgeId: 'edgeid', nodeA: node1.uuid, nodeB: node2.uuid });

      service.loadNetwork(network);

      expect(service['cy'].nodes().length).toBe(2);
      expect(service['cy'].edges().length).toBe(1);
    });
  });

  describe('METHOD: resetView', () => {
    it('should call cy.fit to fit all the items to the viewport', () => {
      const spy = spyOn(service['cy'], 'fit');
      service.resetView();
      expect(spy).toHaveBeenCalled();
    });
  });

  describe('METHOD: createCytoscapeNode', () => {
    it('should add a node to the graph', () => {
      const node: Node = {
        uuid: 'id',
        name: 'name',
        x_pos: 0,
        y_pos: 0,
        entry_node: false,
        high_value_node: false,
        vulnerability: 0
      }

      const addSpy = spyOn(service['cy'], 'add').and.callFake(() => ({} as any));

      service.createCytoscapeNode(node.x_pos, node.y_pos, node);

      expect(addSpy).toHaveBeenCalledWith({
        data: {
          id: node.uuid,
          name: node.name
        },
        position: { x: node.x_pos, y: node.y_pos }
      })
    });
  });

  describe('METHOD: removeCytoscapeNode', () => {
    it('should delete the node and edges connected to it', () => {
      const spy = spyOn(service['cy'], '$id').and.returnValue({
        connectedEdges: () => {
          return {
            remove: () => { }
          }
        },
        remove: () => { }
      } as any);

      service.removeCytoscapeNode(null);
      expect(spy).toHaveBeenCalled();
    });
  });

  describe('METHOD: updateCytoscapeNode', () => {
    it('should update the node properties', () => {
      const spy = spyOn(service['cy'], '$id').and.returnValue({
        position: () => { },
        data: () => { }
      } as any);

      service.updateCytoscapeNode({ uuid: 'id' } as any);
      expect(spy).toHaveBeenCalled();
    });
  });

  describe('METHOD: createCytoscapeEdge', () => {
    it('should add the edge to the cytoscape graph', () => {
      const spy = spyOn(service['cy'], 'add');

      const edge: EdgeObj = {
        edgeId: 'id',
        nodeA: 'a',
        nodeB: 'b'
      }

      service.createCytoscapeEdge(edge.edgeId, edge.nodeA, edge.nodeB);
      expect(spy).toHaveBeenCalledWith({ data: { id: edge.edgeId, source: edge.nodeA, target: edge.nodeB } });
    });
  });

  describe('METHOD: removeCytoscapeEdge', () => {
    it('should remove the edge', () => {
      const spy = spyOn(service['cy'], '$id').and.returnValue({
        remove: () => { }
      } as any);

      service.removeCytoscapeEdge(null);
      expect(spy).toHaveBeenCalled();
    });
  });
});
