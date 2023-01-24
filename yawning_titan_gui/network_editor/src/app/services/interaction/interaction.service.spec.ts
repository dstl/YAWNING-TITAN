import { TestBed } from '@angular/core/testing';
import { CytoscapeService } from '../cytoscape/cytoscape.service';

import { InteractionService } from './interaction.service';

describe('InteractionService', () => {
  let service: InteractionService;

  const cytoscapeServiceStub: any = {
    deleteItem: () => { }
  }

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        { provide: CytoscapeService, useValue: cytoscapeServiceStub }
      ]
    });
    service = TestBed.inject(InteractionService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
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
    it('should trigger cytoscape to delete the selected item', () => {
      const spy = spyOn(service['cytoscapeService'], 'deleteItem');
      service['deleteItem']();
      expect(spy).toHaveBeenCalled();
    });
  });
});
