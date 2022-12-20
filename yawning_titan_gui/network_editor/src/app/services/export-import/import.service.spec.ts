import { TestBed } from '@angular/core/testing';
import { CytoscapeService } from '../cytoscape/cytoscape.service';

import { ImportService } from './import.service';

describe('ImportService', () => {
  let service: ImportService;

  let cytoscapeServiceStub: any = {

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
});
