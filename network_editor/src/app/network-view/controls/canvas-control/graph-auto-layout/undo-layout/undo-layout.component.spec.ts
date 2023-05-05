import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UndoLayoutComponent } from './undo-layout.component';
import { MAT_SNACK_BAR_DATA, MatSnackBarRef } from '@angular/material/snack-bar';
import { NetworkService } from '../../../../../network-class/network.service';

describe('UndoLayoutComponent', () => {
  let component: UndoLayoutComponent;
  let fixture: ComponentFixture<UndoLayoutComponent>;

  const networkStub = {
    loadNetwork: () => { }
  }

  const snackbarRefStub = {
    dismiss: () => { }
  }

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [UndoLayoutComponent],
      providers: [
        { provide: MAT_SNACK_BAR_DATA, useValue: '' },
        { provide: NetworkService, useValue: networkStub },
        { provide: MatSnackBarRef, useValue: snackbarRefStub }
      ]
    })
      .compileComponents();

    fixture = TestBed.createComponent(UndoLayoutComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('METHOD: dismissSnackbar', () => {
    it('should close the snackbar', () => {
      const spy = spyOn(component['snackBarRef'], 'dismiss');
      component.dismissSnackbar();
      expect(spy).toHaveBeenCalled();
    });
  });

  describe('METHOD: undoLayout', () => {
    it('should reload the previous network', () => {
      const reloadSpy = spyOn(component['networkService'], 'loadNetwork');
      const dismissSpy = spyOn(component['snackBarRef'], 'dismiss');

      component.undoLayout();
      expect(reloadSpy).toHaveBeenCalled();
      expect(dismissSpy).toHaveBeenCalled();
    });
  });
});
