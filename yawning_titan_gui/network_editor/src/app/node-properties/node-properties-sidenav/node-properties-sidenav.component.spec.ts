import { NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NodePropertiesSidenavComponent } from './node-properties-sidenav.component';

describe('NodePropertiesSidenavComponent', () => {
  let component: NodePropertiesSidenavComponent;
  let fixture: ComponentFixture<NodePropertiesSidenavComponent>;

  const sidenavStub: any = {
    close: () => { },
    open: () => { }
  }

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [NodePropertiesSidenavComponent],
      schemas: [
        NO_ERRORS_SCHEMA
      ]
    })
      .compileComponents();

    fixture = TestBed.createComponent(NodePropertiesSidenavComponent);
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
      component.open({} as any);
      expect(spy).toHaveBeenCalled();
    });
  });
});
