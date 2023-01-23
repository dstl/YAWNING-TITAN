import { fakeAsync, tick } from '@angular/core/testing';
import { FormBuilder } from '@angular/forms';
import { Network } from '../network-class/network';

import { NodePropertiesService } from './node-properties.service';

describe('NodePropertiesService', () => {
  let service: NodePropertiesService;

  let cytoscapeService: any = {
    network: new Network()
  }

  beforeEach(() => {
    service = new NodePropertiesService(cytoscapeService, new FormBuilder())
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('METHOD: loadDetails', () => {
    it('should update the nodeDetailsSubject with the details of the given node', fakeAsync(() => {
      service.nodePropertiesFormGroupSubject.subscribe((res: any) => {
        expect(res.get('uuid').value).toBe('id');
        expect(res.get('name').value).toBe('name');
        expect(res.get('high_value_node').value).toBeFalsy();
        expect(res.get('entry_node').value).toBeFalsy();
        expect(res.get('x_pos').value).toBe(0);
        expect(res.get('y_pos').value).toBe(0);
      });

      service.loadDetails('id');
      tick();
    }));
  });
});
