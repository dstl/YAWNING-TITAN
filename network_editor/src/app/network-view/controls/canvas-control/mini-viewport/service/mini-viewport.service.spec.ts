import { TestBed } from '@angular/core/testing';

import { MiniViewportService } from './mini-viewport.service';
import { Subject, of } from 'rxjs';

describe('MiniViewportService', () => {
  let service: MiniViewportService;

  const rendererStub: any = {
    createRenderer: () => {
      return {
        appendChild: () => { }
      }
    }
  }

  const cytoscapeServiceStub: any = {
    cy: {}
  }

  const networkStub: any = {
    networkObservable: new Subject()
  }

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = new MiniViewportService(
      rendererStub,
      cytoscapeServiceStub,
      networkStub
    )
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('METHOD: init', () => {
    it('should initialise the viewport elements', () => {
      const boundingBoxInit = spyOn<any>(service, 'updateCyBoundingBox');
      const displayInitSpy = spyOn<any>(service, 'initViewportDisplay');
      const viewInitSpy = spyOn<any>(service, 'initViewportView');
      const updateSpy = spyOn<any>(service, 'listenToUpdates');

      service.init(document.createElement('div'));

      expect(boundingBoxInit).toHaveBeenCalled();
      expect(displayInitSpy).toHaveBeenCalled();
      expect(viewInitSpy).toHaveBeenCalled();
      expect(updateSpy).toHaveBeenCalled();
    });
  });

  describe('METHOD: updateCyBoundingBox', () => {
    it('should update the display bounding box', () => {
      service['_cy'] = {
        elements: () => {
          return {
            boundingBox: () => {
              return {
                x1: 0,
                y1: 0,
                x2: 300,
                y2: 200,
                w: 300,
                h: 200
              }
            }
          }
        }
      } as any;

      service['_viewportPanel'] = {
        offsetWidth: 600,
        offsetHeight: 300
      } as any;


      service['updateCyBoundingBox']();
      expect(service['_displayVal'].zoom.h).toBe(1.5);
      expect(service['_displayVal'].zoom.w).toBe(2);

    });
  });
});
