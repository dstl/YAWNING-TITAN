import { TestBed } from '@angular/core/testing';
import { Subject } from 'rxjs';
import { NetworkService } from 'src/app/network-class/network.service';
import { CytoscapeService } from '../cytoscape/cytoscape.service';
import { ElementType } from '../cytoscape/graph-objects';

import { InteractionService } from './interaction.service';

describe('InteractionService', () => {
  let service: InteractionService;

  const cytoscapeServiceStub: any = {
    doubleClickEvent: new Subject(),
    singleClickEvent: new Subject(),
    dragEvent: new Subject()
  }

  const networkServiceStub = {
    addNode: () => { },
    addEdge: () => { },
    removeItem: () => { },
    editNodeDetails: () => { },
    getNodeById: () => { }
  }

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        { provide: CytoscapeService, useValue: cytoscapeServiceStub },
        { provide: NetworkService, useValue: networkServiceStub }
      ]
    });
    service = TestBed.inject(InteractionService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should listen to double click events in cytoscape canvas', () => {
    const spy = spyOn<any>(service, 'handleDoubleClick').and.callFake(() => { });
    cytoscapeServiceStub.doubleClickEvent.next();
    expect(spy).toHaveBeenCalled();
  });

  it('should listen to single click events in cytoscape canvas', () => {
    const spy = spyOn<any>(service, 'handleSingleClick').and.callFake(() => { });
    cytoscapeServiceStub.singleClickEvent.next();
    expect(spy).toHaveBeenCalled();
  });

  it('should listen to drag events in cytoscape canvas', () => {
    const spy = spyOn<any>(service, 'handleDrag').and.callFake(() => { });
    cytoscapeServiceStub.dragEvent.next();
    expect(spy).toHaveBeenCalled();
  });

  describe('METHOD: handleDoubleClick', () => {
    it('should add a node', () => {
      const addSpy = spyOn(service['networkService'], 'addNode').and.callFake(() => null);
      service['handleDoubleClick']({ target: {} as any, position: { x: 0, y: 0 } } as any);
      expect(addSpy).toHaveBeenCalled();
    })
  });

  describe('METHOD: handleSingleClick', () => {
    it('should call handleEdge creation if the target of the click is a node', () => {
      const handleEdgeCreationSpy = spyOn<any>(service, 'handleEdgeCreation');

      service['handleSingleClick']({ target: { isNode: () => true } } as any)

      expect(handleEdgeCreationSpy).toHaveBeenCalled();
    });

    it('should set the selected subject to null if the thing being clicked is neither edge or node', () => {
      const selectedSpy = spyOn<any>(service['selectedItemSubject'], 'next');
      service['handleSingleClick']({ target: {} } as any);

      expect(selectedSpy).toHaveBeenCalledWith(null);
    });

    it('should set the selected subject', () => {
      const selectedSpy = spyOn<any>(service['selectedItemSubject'], 'next');
      service['handleSingleClick']({
        target: {
          id: () => 'id',
          isNode: () => true,
          isEdge: () => false
        }
      } as any);

      expect(selectedSpy).toHaveBeenCalledWith({
        id: 'id',
        type: ElementType.NODE
      });
    });
  });

  describe('METHOd: handleDrag', () => {
    it('should update node positions', () => {
      const updateSpy = spyOn(service['networkService'], 'editNodeDetails');
      spyOn(service['networkService'], 'getNodeById').and.returnValue({
        uuid: 'id',
        name: 'name',
        x_pos: 0,
        y_pos: 0,
        entry_node: false,
        high_value_node: false,
        vulnerability: 0
      });

      service['handleDrag']({
        target: {
          id: () => 'id',
          position: () => {
            return {
              x: 0,
              y: 0
            }
          }
        }
      } as any)
      expect(updateSpy).toHaveBeenCalled();
    });
  });

  describe('METHOD: handleEdgeCreation', () => {
    it('should not do anything if an edge was not created', () => {
      spyOn(service['networkService'], 'addEdge').and.returnValue(null);
      const selectedItemSpy = spyOn<any>(service['selectedItemSubject'], 'next');
      service['_selectedItem'] = { id: 'id', type: ElementType.NODE }
      service['handleEdgeCreation']({
        target: {
          id: () => 'targetId'
        }
      } as any);

      expect(selectedItemSpy).not.toHaveBeenCalled();
    });

    it('should add an edge', () => {
      spyOn(service['networkService'], 'addEdge').and.returnValue({} as any);
      const selectedItemSpy = spyOn<any>(service['selectedItemSubject'], 'next');
      service['_selectedItem'] = { id: 'id', type: ElementType.NODE }
      service['handleEdgeCreation']({
        target: {
          id: () => 'targetId'
        }
      } as any);

      expect(selectedItemSpy).toHaveBeenCalledWith(null);
    });
  });

  describe('METHOD: setInputFocusStatus', () => {
    it('should update the input focus state', () => {
      service.setInputFocusStatus(true);
      expect(service['inputFocus']).toBeTruthy();
      service.setInputFocusStatus(false);
      expect(service['inputFocus']).toBeFalsy();
    });
  });

  describe('METHOD: keyInput', () => {
    it('should not do anything if the user is typing in an input field', () => {
      const deleteSpy = spyOn<any>(service, 'deleteItem');

      service.setInputFocusStatus(true);
      service.keyInput({ key: 'Delete' } as any);
      expect(deleteSpy).not.toHaveBeenCalled();
    });

    it('should delete the selected item if the user is not typing', () => {
      const deleteSpy = spyOn<any>(service, 'deleteItem');

      service.setInputFocusStatus(false);
      service.keyInput({ key: 'Delete' } as any);
      expect(deleteSpy).toHaveBeenCalled();
    });

    it('should handle shift key inputs', () => {
      const shiftSpy = spyOn<any>(service, 'handleShiftKeyInput');

      service.setInputFocusStatus(false);
      service.keyInput({ key: 'Enter', shiftKey: true } as any);
      expect(shiftSpy).toHaveBeenCalled();
    });

    it('should handle control key inputs', () => {
      const shiftSpy = spyOn<any>(service, 'handleControlKeyInput');

      service.setInputFocusStatus(false);
      service.keyInput({ key: 'Enter', ctrlKey: true } as any);
      expect(shiftSpy).toHaveBeenCalled();
    });
  });

  describe('METHOD: deleteItem', () => {
    it('should remove the item from the network', () => {
      const spy = spyOn(service['networkService'], 'removeItem');
      service['deleteItem']();
      expect(spy).toHaveBeenCalled();
    });
  })
});
