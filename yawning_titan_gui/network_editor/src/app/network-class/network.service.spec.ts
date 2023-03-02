import { TestBed } from '@angular/core/testing';
import { CytoscapeService } from '../services/cytoscape/cytoscape.service';

import { NetworkService } from './network.service';

describe('NetworkService', () => {
  let service: NetworkService;

  const cytoscapeServiceStub = {

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
});
