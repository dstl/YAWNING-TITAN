import { NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PropertiesEditorSidenavComponent } from './properties-editor-sidenav.component';

describe('PropertiesEditorSidenavComponent', () => {
  let component: PropertiesEditorSidenavComponent;
  let fixture: ComponentFixture<PropertiesEditorSidenavComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PropertiesEditorSidenavComponent ],
      schemas: [
        NO_ERRORS_SCHEMA
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PropertiesEditorSidenavComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
