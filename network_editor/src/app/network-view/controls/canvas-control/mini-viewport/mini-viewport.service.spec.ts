import { TestBed } from '@angular/core/testing';

import { MiniViewportService } from './mini-viewport.service';

describe('MiniViewportService', () => {
  let service: MiniViewportService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MiniViewportService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
