import { NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, fakeAsync, TestBed, tick } from '@angular/core/testing';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { Subject } from 'rxjs';

import { NodePropertiesComponent } from './node-properties.component';
import { NodePropertiesService } from './node-properties.service';

describe('NodePropertiesComponent', () => {
  let component: NodePropertiesComponent;
  let fixture: ComponentFixture<NodePropertiesComponent>;

  let nodePropertiesServiceStub: any = {
    loadDetails: () => { },
    nodePropertiesFormGroupSubject: new Subject(),
    updateNodeProperties: () => { },
    randomVulnerabilitiesOnReset: () => { },
    randomEntryNodesOnReset: () => { },
    randomHighValueNodesOnReset: () => { },
  }

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [NodePropertiesComponent],
      providers: [
        { provide: NodePropertiesService, useValue: nodePropertiesServiceStub }
      ],
      schemas: [
        NO_ERRORS_SCHEMA
      ]
    })
      .compileComponents();

    fixture = TestBed.createComponent(NodePropertiesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('METHOD: ngOnInit', () => {
    it('should get the vulnerability value', fakeAsync(() => {
      spyOn(component, 'updateNode').and.callFake(() => { });
      const formGroup = new FormBuilder().group({
        vulnerability: new FormControl(0)
      });

      nodePropertiesServiceStub.nodePropertiesFormGroupSubject.next(formGroup);

      tick();

      component.formGroup.get('vulnerability').setValue(0.5);
      component.formGroup.updateValueAndValidity();
      tick();

      // vulnerabilityVal should now be 0.5
      expect(component.vulnerabilityVal).toBe(0.5);
    }));
  });

  describe('ngOnChanges', () => {
    it('should load the details of the node if it was not the same as previous', () => {
      const spy = spyOn(component['nodePropertiesService'], 'loadDetails');
      const changeObj = {
        node: {
          currentValue: 'a',
          previousValue: 'b'
        }
      }
      component.ngOnChanges(changeObj as any);
      expect(spy).toHaveBeenCalled();
    });

    it('should not load the details of the node if it was the same as previous', () => {
      const spy = spyOn(component['nodePropertiesService'], 'loadDetails');
      const changeObj = {
        nodeId: {
          currentValue: 'a',
          previousValue: 'a'
        }
      }
      component.ngOnChanges(changeObj as any);
      expect(spy).not.toHaveBeenCalled();
    });
  });

  describe('METHOD: updateNode', () => {
    it('should call update node on the service', () => {
      const spy = spyOn(component['nodePropertiesService'], 'updateNodeProperties').and.callFake(() => { });

      component.formGroup = {
        valid: true, get: () => {
          return { value: '' }
        }
      } as any;
      component.updateNode();
      expect(spy).toHaveBeenCalled();
    });
  });

  describe('METHOD: closeSideNav', () => {
    it('should emit the close event', (done) => {
      component.close.subscribe(() => {
        expect(true);
        done();
      });

      component.closeSideNav();
    });
  });

  describe('METHOD: showVulnerabilitySlider', () => {
    it('should return the randomVulnerabilitiesOnReset value', () => {
      const spy = spyOn(component['nodePropertiesService'], 'randomVulnerabilitiesOnReset');
      component.showVulnerabilitySlider();
      expect(spy).toHaveBeenCalled();
    })
  });

  describe('METHOD: showEntryNodeToggle', () => {
    it('should return the randomEntryNodesOnReset value', () => {
      const spy = spyOn(component['nodePropertiesService'], 'randomEntryNodesOnReset');
      component.showEntryNodeToggle();
      expect(spy).toHaveBeenCalled();
    })
  });

  describe('METHOD: showHighValueNodeToggle', () => {
    it('should return the randomHighValueNodesOnReset value', () => {
      const spy = spyOn(component['nodePropertiesService'], 'randomHighValueNodesOnReset');
      component.showHighValueNodeToggle();
      expect(spy).toHaveBeenCalled();
    })
  });
});
