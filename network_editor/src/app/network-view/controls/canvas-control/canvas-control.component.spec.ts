import { NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CytoscapeService } from 'src/app/services/cytoscape/cytoscape.service';

import { CanvasControlComponent } from './canvas-control.component';

describe('CanvasControlComponent', () => {
  let component: CanvasControlComponent;
  let fixture: ComponentFixture<CanvasControlComponent>;

  const stubCytoscapeService = {
    resetView: () => { }
  }

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [CanvasControlComponent],
      providers: [
        { provide: CytoscapeService, useValue: stubCytoscapeService }
      ],
      schemas: [
        NO_ERRORS_SCHEMA
      ]
    })
      .compileComponents();

    fixture = TestBed.createComponent(CanvasControlComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('METHOD: resetView', () => {
    it('should call resetView in cytoscapeService', () => {
      const spy = spyOn(component['cytoscapeService'], 'resetView');
      component.resetView();
      expect(spy).toHaveBeenCalled();
    });
  });
});
