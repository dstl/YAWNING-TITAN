import { TestBed } from '@angular/core/testing';
import { CytoscapeService } from '../cytoscape/cytoscape.service';

import { InteractionService } from './interaction.service';

describe('InteractionService', () => {
  let service: InteractionService;

  const cytoscapeServiceStub: any = {

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
});
