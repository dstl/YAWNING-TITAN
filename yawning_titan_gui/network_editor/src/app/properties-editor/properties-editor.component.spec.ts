import { NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PropertiesEditorComponent } from './properties-editor.component';
import { PropertiesEditorService } from './properties-editor.service';

describe('PropertiesEditorComponent', () => {
  let component: PropertiesEditorComponent;
  let fixture: ComponentFixture<PropertiesEditorComponent>;

  let propertiesEditorServiceStub: any = {

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
});
