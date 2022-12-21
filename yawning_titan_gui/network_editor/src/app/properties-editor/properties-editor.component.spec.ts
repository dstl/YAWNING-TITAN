import { NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PropertiesEditorComponent } from './properties-editor.component';
import { PropertiesEditorService } from './properties-editor.service';

describe('PropertiesEditorComponent', () => {
  let component: PropertiesEditorComponent;
  let fixture: ComponentFixture<PropertiesEditorComponent>;

  let propertiesEditorServiceStub: any = {
    loadDetails: () => { }
  }

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [PropertiesEditorComponent],
      providers: [
        { provide: PropertiesEditorService, useValue: propertiesEditorServiceStub }
      ],
      schemas: [
        NO_ERRORS_SCHEMA
      ]
    })
      .compileComponents();

    fixture = TestBed.createComponent(PropertiesEditorComponent);
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
