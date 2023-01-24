import { fakeAsync, tick } from '@angular/core/testing';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { of, Subject } from 'rxjs';
import { Network } from '../network-class/network';

import { NodePropertiesService } from './node-properties.service';

describe('NodePropertiesService', () => {
  let service: NodePropertiesService;

  let cytoscapeService: any = {
    network: new Network(),
    elementDragEvent: new Subject(),
    updateNode: () => { }
  }

  beforeEach(() => {
    service = new NodePropertiesService(cytoscapeService, new FormBuilder())
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('METHOD: loadDetails', () => {
    it('should do nothing if the node to be updated does not exist', fakeAsync(() => {
      const spy = spyOn<any>(service, 'listenToNodePositionChange');

      const node = {
        uuid: 'id',
        name: 'name',
        high_value_node: true,
        entry_node: false,
        x_pos: 0,
        y_pos: 0,
        vulnerability: 0
      };

      service['cytoscapeService'].network.addNode(node);

      service.loadDetails('fake id');
      tick();

      expect(spy).not.toHaveBeenCalled();
    }));

    it('should update the nodeDetailsSubject with the details of the given node', fakeAsync(() => {
      const node = {
        uuid: 'id',
        name: 'name',
        high_value_node: true,
        entry_node: false,
        x_pos: 0,
        y_pos: 0,
        vulnerability: 0
      };

      service['cytoscapeService'].network.addNode(node);

      service.nodePropertiesFormGroupSubject.subscribe((res: any) => {
        expect(res.get('uuid').value).toBe(node.uuid);
        expect(res.get('name').value).toBe(node.name);
        expect(res.get('high_value_node').value).toBeTruthy();
        expect(res.get('entry_node').value).toBeFalsy();
        expect(res.get('x_pos').value).toBe(0);
        expect(res.get('y_pos').value).toBe(0);
      });

      service.loadDetails('id');
      tick();
    }));
  });

  describe('METHOD: updateNodeProperties', () => {
    it('should not update nodes unless the form is valid', () => {
      const spy = spyOn(service['cytoscapeService'], 'updateNode');

      service['_nodePropertiesFormGroup'] = new FormBuilder().group({ test: new FormControl('', Validators.required) })

      service.updateNodeProperties();
      expect(spy).not.toHaveBeenCalled();
    });

    it('should update the node if the form is valid', () => {
      const spy = spyOn(service['cytoscapeService'], 'updateNode');

      service['_nodePropertiesFormGroup'] = new FormBuilder().group({
        uuid: new FormControl('id'),
        name: new FormControl('name'),
        x_pos: new FormControl(0),
        y_pos: new FormControl(0),
        vulnerability: new FormControl(0),
        high_value_node: new FormControl(true),
        entry_node: new FormControl(true),
      })

      service.updateNodeProperties();
      expect(spy).toHaveBeenCalled();
    });
  });

  describe('METHOD: listenToNodePositionChange', () => {
    it('should not update the node if a different node is being dragged', fakeAsync(() => {
      const spy = spyOn(service, 'updateNodeProperties');

      service['_nodePropertiesFormGroup'] = new FormBuilder().group({
        uuid: new FormControl('id'),
        name: new FormControl('name'),
        x_pos: new FormControl(0),
        y_pos: new FormControl(0),
        vulnerability: new FormControl(0),
        high_value_node: new FormControl(true),
        entry_node: new FormControl(true),
      });

      service['listenToNodePositionChange']();
      cytoscapeService.elementDragEvent.next({
        id: 'diff_id',
        position: { x: 1, y: 1 }
      });
      tick();

      expect(spy).not.toHaveBeenCalled();
    }));

    it('should update the node if the node being dragged is the current item', fakeAsync(() => {
      const spy = spyOn(service, 'updateNodeProperties');

      service['_nodePropertiesFormGroup'] = new FormBuilder().group({
        uuid: new FormControl('id'),
        name: new FormControl('name'),
        x_pos: new FormControl(0),
        y_pos: new FormControl(0),
        vulnerability: new FormControl(0),
        high_value_node: new FormControl(true),
        entry_node: new FormControl(true),
      });

      service['listenToNodePositionChange']();
      cytoscapeService.elementDragEvent.next({
        id: 'id',
        position: { x: 1, y: 1 }
      });

      tick(200);

      expect(spy).toHaveBeenCalled();
    }));
  });
});
