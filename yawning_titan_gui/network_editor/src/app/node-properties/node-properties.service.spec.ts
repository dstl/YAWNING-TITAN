import { fakeAsync, flush, tick } from '@angular/core/testing';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { of, Subject } from 'rxjs';

import { NodePropertiesService } from './node-properties.service';

describe('NodePropertiesService', () => {
  let service: NodePropertiesService;

  let networkServiceStub: any = {
    addNode: () => { },
    updateNode: () => { },
    editNodeDetails: () => { },
    getNodeById: () => { },
    networkObservable: new Subject()
  }

  let interactionServiceStub: any = {
    dragEvent: new Subject()
  }

  beforeEach(() => {
    service = new NodePropertiesService(
      networkServiceStub,
      interactionServiceStub,
      new FormBuilder()
    )
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should update input fields when the network settings are changed', () => {
    spyOn(service['networkService'], 'getNodeById').and.returnValue({
      uuid: 'id',
      name: 'node',
      x_pos: 0,
      y_pos: 0,
      high_value_node: true,
      entry_node: true,
      vulnerability: 0
    });

    service.loadDetails('id');

    networkServiceStub.networkObservable.next({
      networkSettings: {
        entryNode: { set_random_entry_nodes: true },
        highValueNode: { set_random_high_value_nodes: true },
        vulnerability: {
          set_random_vulnerabilities: true,
          node_vulnerability_lower_bound: 0.2
        }
      }
    });

    expect(service['_nodePropertiesFormGroup'].get('entry_node').value).toBeFalsy();
    expect(service['_nodePropertiesFormGroup'].get('high_value_node').value).toBeFalsy();
    expect(service['_nodePropertiesFormGroup'].get('vulnerability').value).toBe('0.20');
  });

  it('should update node positions when drag event updates', () => {
    const spy = spyOn(service, 'updateNodePositions').and.callFake(() => { });
    interactionServiceStub.dragEvent.next();
    expect(spy).toHaveBeenCalled();
  });

  describe('METHOD: loadDetails', () => {
    it('should do nothing if the node to be updated does not exist', fakeAsync(() => {
      const node = {
        uuid: 'id',
        name: 'name',
        high_value_node: true,
        entry_node: false,
        x_pos: 0,
        y_pos: 0,
        vulnerability: 0
      };

      service['networkService'].addNode(node.x_pos, node.y_pos, node);

      service.loadDetails('fake id');
      tick();

      expect(service['_nodePropertiesFormGroup']).toBeUndefined();
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

      service['networkService'].addNode(node.x_pos, node.y_pos, node);

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
      const spy = spyOn(service['networkService'], 'editNodeDetails');

      service['_nodePropertiesFormGroup'] = new FormBuilder().group({ test: new FormControl('', Validators.required) })

      service.updateNodeProperties();
      expect(spy).not.toHaveBeenCalled();
    });

    it('should update the node if the form is valid', () => {
      const spy = spyOn(service['networkService'], 'editNodeDetails');

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

  describe('METHOD: updateNodePositions', () => {
    it('should do nothing if the node being dragged is not what is displayed by the node properties', () => {
      spyOn(service['networkService'], 'getNodeById').and.returnValue({
        uuid: 'id',
        name: 'node',
        x_pos: 0,
        y_pos: 0,
        high_value_node: true,
        entry_node: true,
        vulnerability: 0
      });

      service.loadDetails('id');

      service.updateNodePositions({ id: 'not this one', position: { x: 10, y: 10 } });

      expect(service['_nodePropertiesFormGroup'].get('x_pos').value).toBe(0);
      expect(service['_nodePropertiesFormGroup'].get('y_pos').value).toBe(0);
    });

    it('should update input field if the node being dragged is what is displayed by the node properties', () => {
      spyOn(service['networkService'], 'getNodeById').and.returnValue({
        uuid: 'id',
        name: 'node',
        x_pos: 0,
        y_pos: 0,
        high_value_node: true,
        entry_node: true,
        vulnerability: 0
      });

      service.loadDetails('id');

      service.updateNodePositions({ id: 'id', position: { x: 10, y: 10 } });

      expect(service['_nodePropertiesFormGroup'].get('x_pos').value).toBe(10);
      expect(service['_nodePropertiesFormGroup'].get('y_pos').value).toBe(10);
    });
  });
});
