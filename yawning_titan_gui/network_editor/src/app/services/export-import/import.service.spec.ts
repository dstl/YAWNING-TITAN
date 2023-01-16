import { fakeAsync, TestBed, tick } from '@angular/core/testing';
import { CytoscapeService } from '../cytoscape/cytoscape.service';

import { ImportService } from './import.service';

describe('ImportService', () => {
  let service: ImportService;

  let cytoscapeServiceStub: any = {
    loadNetwork: () => { }
  }

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        { provide: CytoscapeService, useValue: cytoscapeServiceStub }
      ]
    });
    service = TestBed.inject(ImportService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('METHOD: loadFile', () => {
    it('should do nothing if no event to process', () => {
      const spy = spyOn(service['cytoscapeService'], 'loadNetwork');
      service.loadFile(null);
      expect(spy).not.toHaveBeenCalled();
    });

    it('should throw an error if JSON is invalid', fakeAsync(() => {
      const spy = spyOn(service['cytoscapeService'], 'loadNetwork');
      const event = [{
        text: (): any => { }
      }];

      spyOn(event[0], 'text').and.returnValue(Promise.resolve('not_json'));

      expect(() => {
        service.loadFile(event);
        tick();
      }).toThrowError();
      expect(spy).not.toHaveBeenCalled();
    }));

    it('should load a network if the JSON is valid', fakeAsync(() => {
      const spy = spyOn(service['cytoscapeService'], 'loadNetwork');
      spyOn(JSON, 'parse').and.returnValue({})
      const event = [{
        text: (): any => { }
      }];

      spyOn(event[0], 'text').and.returnValue(Promise.resolve());

      service.loadFile(event);
      tick();
      expect(spy).toHaveBeenCalled();
    }));
  });

  describe('METHOD: loadNetworkFromWindow', () => {
    it('should do nothing if no event to process', () => {
      const spy = spyOn(service['cytoscapeService'], 'loadNetwork');
      service.loadNetworkFromWindow(null);
      expect(spy).not.toHaveBeenCalled();
    });

    it('should throw an error if JSON is invalid', () => {
      const spy = spyOn(service['cytoscapeService'], 'loadNetwork');

      expect(() => {
        service.loadNetworkFromWindow({ text: (): any => { } });
      }).toThrowError();
      expect(spy).not.toHaveBeenCalled();
    });

    it('should load a network if the JSON is valid', () => {
      const spy = spyOn(service['cytoscapeService'], 'loadNetwork');
      spyOn(JSON, 'parse').and.returnValue({});

      service.loadNetworkFromWindow({ text: (): any => { } });
      expect(spy).toHaveBeenCalled();
    });
  });
});
