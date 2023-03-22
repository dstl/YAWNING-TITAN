import { fakeAsync, TestBed, tick } from '@angular/core/testing';
import { CytoscapeService } from '../services/cytoscape/cytoscape.service';
import { ElementType } from '../services/cytoscape/graph-objects';
import { Network } from './network';

import { NetworkService } from './network.service';

describe('NetworkService', () => {
  let service: NetworkService;

  const cytoscapeServiceStub = {
    loadNetwork: () => { },
    createCytoscapeNode: () => { },
    updateCytoscapeNode: () => { },
    removeCytoscapeNode: () => { },
    createCytoscapeEdge: () => { },
    removeCytoscapeEdge: () => { }
  }

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        { provide: CytoscapeService, useValue: cytoscapeServiceStub }
      ]
    });
    service = TestBed.inject(NetworkService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('METHOD: loadNetwork', () => {
    it('should set the passed network as the new network', () => {
      const graphRenderSpy = spyOn(service['cytoscapeService'], 'loadNetwork');
      const networkEventSpy = spyOn(service['_networkSubject'], 'next');

      const network = new Network();

      service.loadNetwork(network);

      expect(service['nodeCount']).toBe(0);
      expect(graphRenderSpy).toHaveBeenCalledWith(network);
      expect(networkEventSpy).toHaveBeenCalledWith(network);
    });
  });

  describe('METHOD: updateNetworkSettings', () => {
    it('should do nothing if there are no network settings to update', () => {
      const networkUpdateSpy = spyOn(service['_network'], 'updateNetworkSettings').and.callFake(() => { });
      service.updateNetworkSettings(null);
      expect(networkUpdateSpy).not.toHaveBeenCalled();
    });

    it('should update network settings and apply the change to nodes', () => {
      const networkUpdateSpy = spyOn(service['_network'], 'updateNetworkSettings').and.callFake(() => { });
      const nodeUpdateSpy = spyOn<any>(service, 'applyNetworkSettingsToNodes');

      service.updateNetworkSettings({
        entryNode: null,
        highValueNode: null,
        vulnerability: null
      });

      expect(networkUpdateSpy).toHaveBeenCalled();
      expect(nodeUpdateSpy).toHaveBeenCalled();
    });
  });

  describe('METHOD: applyNetworkSettingsToNodes', () => {
    it('should edit all nodes', () => {
      const spy = spyOn<any>(service, 'editNodeDetails')

      const network = new Network();
      network.addNode(0, 0, 0);
      network.addNode(10, 10, 1);

      expect(network.nodeList.length).toBe(2);

      service['_network'] = network;

      service['applyNetworkSettingsToNodes']({
        entryNode: {
          set_random_entry_nodes: false,
          num_of_random_entry_nodes: 0,
          random_entry_node_preference: null
        },
        highValueNode: {
          set_random_high_value_nodes: false,
          num_of_random_high_value_nodes: 0,
          random_high_value_node_preference: null
        },
        vulnerability: {
          set_random_vulnerabilities: false,
          node_vulnerability_lower_bound: 0,
          node_vulnerability_upper_bound: 1
        }
      })

      expect(spy).toHaveBeenCalledTimes(2);
    });
  });

  describe('METHOD: addNode', () => {
    it('should do nothing if the node was not created', () => {
      spyOn(service['_network'], 'addNode').and.returnValue(null);

      const renderNodeSpy = spyOn(service['cytoscapeService'], 'createCytoscapeNode');
      const updateSpy = spyOn(service['_networkSubject'], 'next');

      service.addNode(null, null);

      expect(renderNodeSpy).not.toHaveBeenCalled();
      expect(updateSpy).not.toHaveBeenCalled();
    });

    it('should render the node and update', () => {
      spyOn(service['_network'], 'addNode').and.returnValue({
        uuid: 'id',
        name: 'node',
        x_pos: 0,
        y_pos: 0,
        entry_node: false,
        high_value_node: false,
        vulnerability: 0
      });

      const renderNodeSpy = spyOn(service['cytoscapeService'], 'createCytoscapeNode');
      const updateSpy = spyOn(service['_networkSubject'], 'next');

      service.addNode(null, null);

      expect(renderNodeSpy).toHaveBeenCalled();
      expect(updateSpy).toHaveBeenCalled();
    });
  });

  describe('METHOD: editNodeDetails', () => {
    it('should do nothing if editing did not work', () => {
      spyOn(service['_network'], 'editNodeDetails').and.returnValue(null);
      const renderNodeSpy = spyOn(service['cytoscapeService'], 'updateCytoscapeNode');
      const updateSpy = spyOn(service['_networkSubject'], 'next');

      service.editNodeDetails(null);

      expect(renderNodeSpy).not.toHaveBeenCalled();
      expect(updateSpy).not.toHaveBeenCalled();
    });

    it('should do nothing if editing did not work', () => {
      spyOn(service['_network'], 'editNodeDetails').and.returnValue({} as any);
      const renderNodeSpy = spyOn(service['cytoscapeService'], 'updateCytoscapeNode');
      const updateSpy = spyOn(service['_networkSubject'], 'next');

      service.editNodeDetails(null);

      expect(renderNodeSpy).toHaveBeenCalled();
      expect(updateSpy).toHaveBeenCalled();
    });
  });

  describe('METHOD: removeItem', () => {
    it('should do nothing if the parameter is empty', () => {
      const removeEdgeSpy = spyOn<any>(service, 'removeEdge');
      const removeNodeSpy = spyOn<any>(service, 'removeNode');

      service.removeItem(null);

      service.removeItem({
        id: '',
        type: null
      });

      expect(removeEdgeSpy).not.toHaveBeenCalled();
      expect(removeNodeSpy).not.toHaveBeenCalled();
    });

    it('should remove edge if the item being removed is an edge', () => {
      const removeEdgeSpy = spyOn<any>(service, 'removeEdge');
      const removeNodeSpy = spyOn<any>(service, 'removeNode');

      service.removeItem({
        id: '',
        type: ElementType.EDGE
      });

      expect(removeEdgeSpy).toHaveBeenCalled();
      expect(removeNodeSpy).not.toHaveBeenCalled();
    });

    it('should remove node if the item being removed is a node', () => {
      const removeEdgeSpy = spyOn<any>(service, 'removeEdge');
      const removeNodeSpy = spyOn<any>(service, 'removeNode');

      service.removeItem({
        id: '',
        type: ElementType.NODE
      });

      expect(removeEdgeSpy).not.toHaveBeenCalled();
      expect(removeNodeSpy).toHaveBeenCalled();
    });
  });

  describe('METHOD: removeNode', () => {
    it('should remove a node', () => {
      const removeSpy = spyOn(service['_network'], 'removeNode');
      const unrenderNode = spyOn(service['cytoscapeService'], 'removeCytoscapeNode');

      service['removeNode'](null);

      expect(removeSpy).toHaveBeenCalled();
      expect(unrenderNode).toHaveBeenCalled();
    });
  });

  describe('METHOD: getNodeById', () => {
    it('should return the node', () => {
      const spy = spyOn(service['_network'], 'getNodeById');
      service.getNodeById(null);
      expect(spy).toHaveBeenCalled();
    });
  });

  describe('METHOD: addEdge', () => {
    it('should do nothing if the edge was not created', () => {
      spyOn(service['_network'], 'addEgde').and.returnValue(null);
      const renderNodeSpy = spyOn(service['cytoscapeService'], 'createCytoscapeEdge');
      const updateSpy = spyOn(service['_networkSubject'], 'next');

      service.addEdge(null);

      expect(renderNodeSpy).not.toHaveBeenCalled();
      expect(updateSpy).not.toHaveBeenCalled();
    });

    it('should render the edge and update', () => {
      spyOn(service['_network'], 'addEgde').and.returnValue({
        edgeId: '',
        nodeA: '',
        nodeB: ''
      });
      const renderNodeSpy = spyOn(service['cytoscapeService'], 'createCytoscapeEdge');
      const updateSpy = spyOn(service['_networkSubject'], 'next');

      service.addEdge(null);

      expect(renderNodeSpy).toHaveBeenCalled();
      expect(updateSpy).toHaveBeenCalled();
    });
  });

  describe('METHOD: removeEdge', () => {
    it('should remove an edge', () => {
      const removeSpy = spyOn(service['_network'], 'removeEdge');
      const unrenderNode = spyOn(service['cytoscapeService'], 'removeCytoscapeEdge');

      service['removeEdge'](null);

      expect(removeSpy).toHaveBeenCalled();
      expect(unrenderNode).toHaveBeenCalled();
    });
  });

  describe('METHOD: getNetworkJson', () => {
    it('should get the network properties in JSON format', () => {
      const spy = spyOn(service['_network'], 'toJson');
      service.getNetworkJson();
      expect(spy).toHaveBeenCalled();
    });
  });
});
