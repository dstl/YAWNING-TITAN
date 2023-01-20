import { fakeAsync, tick } from '@angular/core/testing';

import { PropertiesEditorService } from './node-properties.service';

describe('PropertiesEditorService', () => {
  let service: PropertiesEditorService;

  const stubNodeData = {
    name: 'name',
    high_value_node: false,
    entry_node: false,
  }

  const stubNode = {
    id: () => 'id',
    data: (key: string) => stubNodeData[`${key}`],
    position: () => {
      return {
        x: 0,
        y: 0
      }
    }
  }

  let cytoscapeService: any = {
    cytoscapeObj: {
      nodes: () => {
        return {
          getElementById: () => stubNode
        }
      }
    }
  }

  beforeEach(() => {
    service = new PropertiesEditorService(cytoscapeService)
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('METHOD: loadDetails', () => {
    it('should update the nodeDetailsSubject with the details of the given node', fakeAsync(() => {
      service.nodeDetailsSubject.subscribe(res => {
        expect(res.uuid).toBe('id');
        expect(res.name).toBe('name');
        expect(res.high_value_node).toBeFalsy();
        expect(res.entry_node).toBeFalsy();
        expect(res.x_pos).toBe(0);
        expect(res.y_pos).toBe(0);
      });

      service.loadDetails('id');
      tick();
    }));
  });
});
