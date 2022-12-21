import { NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MatSidenav } from '@angular/material/sidenav';

import { PropertiesEditorSidenavComponent } from './properties-editor-sidenav.component';

describe('PropertiesEditorSidenavComponent', () => {
  let component: PropertiesEditorSidenavComponent;
  let fixture: ComponentFixture<PropertiesEditorSidenavComponent>;

  const sidenavStub: any = {
    close: () => { },
    open: () => { }
  }

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [PropertiesEditorSidenavComponent],
      schemas: [
        NO_ERRORS_SCHEMA
      ]
    })
      .compileComponents();

    fixture = TestBed.createComponent(PropertiesEditorSidenavComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    component.sidenav = sidenavStub;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('METHOD: close', () => {
    it('should close the sidenav', () => {
      const spy = spyOn(component.sidenav, 'close');
      component.close();
      expect(spy).toHaveBeenCalled();
    });
  });

  describe('METHOD: open', () => {
    it('should open the sidenav', () => {
      const spy = spyOn(component.sidenav, 'open');
      component.open('');
      expect(spy).toHaveBeenCalled();
    });
  });
});
