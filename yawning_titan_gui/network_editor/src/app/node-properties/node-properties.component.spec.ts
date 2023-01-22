import { NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Subject } from 'rxjs';

import { NodePropertiesComponent } from './node-properties.component';
import { PropertiesEditorService } from './node-properties.service';

describe('NodePropertiesComponent', () => {
  let component: NodePropertiesComponent;
  let fixture: ComponentFixture<NodePropertiesComponent>;

  let propertiesEditorServiceStub: any = {
    loadDetails: () => { },
    nodePropertiesFormGroupSubject: new Subject()
  }

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [NodePropertiesComponent],
      providers: [
        { provide: PropertiesEditorService, useValue: propertiesEditorServiceStub }
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

  describe('ngOnChanges', () => {
    it('should load the details of the node if it was not the same as previous', () => {
      const spy = spyOn(component['propertiesEditorService'], 'loadDetails');
      const changeObj = {
        nodeId: {
          currentValue: 'a',
          previousValue: 'b'
        }
      }
      component.ngOnChanges(changeObj as any);
      expect(spy).toHaveBeenCalled();
    });
    it('should not load the details of the node if it was the same as previous', () => {
      const spy = spyOn(component['propertiesEditorService'], 'loadDetails');
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
});
