import { TestBed } from '@angular/core/testing';

import { CytoscapeService } from './cytoscape.service';

describe('CytoscapeService', () => {
  let service: CytoscapeService;

  beforeEach(() => {
    service = new CytoscapeService();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
