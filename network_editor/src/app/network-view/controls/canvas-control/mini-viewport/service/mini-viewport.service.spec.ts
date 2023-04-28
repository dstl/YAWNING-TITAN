import { TestBed } from '@angular/core/testing';

import { MiniViewportService } from './mini-viewport.service';
import { Subject, of } from 'rxjs';
import { ViewportDisplay } from './viewport-classes/viewport-display';
import { ViewportView } from './viewport-classes/viewport-view';

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

  describe('METHOD: initViewportDisplay', () => {
    it('should create a viewport display instance and update the image', () => {
      const updateImageSpy = spyOn<any>(service, 'updateDisplayImage');
      expect(service['_viewportDisplay']).toBeUndefined();

      service['initViewportDisplay']();
      expect(service['_viewportDisplay']).toBeDefined();
      expect(updateImageSpy).toHaveBeenCalled();
    });
  });

  describe('METHOD: updateDisplayImage', () => {
    it('should return if the image is already being updated', () => {
      const updateBoundsSpy = spyOn<any>(service, 'updateCyBoundingBox');
      service['_updatingDisplay'] = true;
      service['updateDisplayImage']();
      expect(updateBoundsSpy).not.toHaveBeenCalled();
    });

    it('should update the image in the display', () => {
      service['_cy'] = {
        png: () => { }
      } as any;

      service['_viewportDisplay'] = new ViewportDisplay(document.createElement('div'), document.createElement('div'));
      service['_viewportPanel'] = document.createElement('div');
      service['_displayBoundingBox'] = { w: 0, h: 0, x1: 0, x2: 0, y1: 0, y2: 0 };
      const updateBoundsSpy = spyOn<any>(service, 'updateCyBoundingBox');
      const cytoscapeSpy = spyOn<any>(service['_cy'], 'png');
      const updateImgSpy = spyOn<any>(service['_viewportDisplay'], 'updateImage');

      service['updateDisplayImage']();
      expect(updateBoundsSpy).toHaveBeenCalled();
      expect(cytoscapeSpy).toHaveBeenCalled();
      expect(updateImgSpy).toHaveBeenCalled();
    });
  });

  describe('METHOD: initViewportView', () => {
    it('should create a viewport view instance and update the view', () => {
      const updateViewSpy = spyOn<any>(service, 'updateView').and.callFake(() => { });
      service['_viewportDisplay'] = new ViewportDisplay(document.createElement('div'), document.createElement('div'));
      expect(service['_viewportView']).toBeUndefined();

      service['initViewportView']();
      expect(service['_viewportView']).toBeDefined();
      expect(updateViewSpy).toHaveBeenCalled();
    });
  });

  describe('METHOD: updateView', () => {
    it('should update the view position', () => {
      const graph = {
        w: 100, h: 100, x1: 0, x2: 100, y1: 0, y2: 100
      }
      const view = {
        w: 100, h: 100, x1: 0, x2: 100, y1: 0, y2: 100
      }

      service['_cy'] = {
        pan: () => { return { x: 0, y: 0 } },
        zoom: () => 1,
        elements: () => {
          return {
            renderedBoundingBox: () => {
              return graph
            }
          }
        },
        extent: () => view
      } as any

      const expectedGraphExt = {
        zoom: 1,
        pan: { x: 0, y: 0 },
        bb: graph
      }

      const expectedView = {
        zoom: 1,
        pan: { x: 0, y: 0 },
        bb: view
      }

      service['_viewportView'] = new ViewportView(
        document.createElement('div'),
        document.createElement('div'),
        document.createElement('div')
      )

      const updateViewPositionSpy = spyOn<any>(service['_viewportView'], 'updateViewPosition').and.callFake(function () {
        expect(arguments[0]).toEqual(expectedView);
        expect(arguments[1]).toEqual(expectedGraphExt);
      });

      service['updateView']();
      expect(updateViewPositionSpy).toHaveBeenCalled();
    });
  });
});
