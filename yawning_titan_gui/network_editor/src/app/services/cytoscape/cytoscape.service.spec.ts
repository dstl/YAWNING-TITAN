import { Network } from '../../network-class/network';

import { CytoscapeService } from './cytoscape.service';

describe('CytoscapeService', () => {
  let service: CytoscapeService;

  beforeEach(() => {
    service = new CytoscapeService(null);

    service['_network'] = new Network();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
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
});
