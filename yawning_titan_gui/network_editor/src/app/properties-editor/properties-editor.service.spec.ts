import { TestBed } from '@angular/core/testing';

import { PropertiesEditorService } from './properties-editor.service';

describe('PropertiesEditorService', () => {
  let service: PropertiesEditorService;

  let cytoscapeService: any = {}

  beforeEach(() => {
    service = new PropertiesEditorService(cytoscapeService)
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
