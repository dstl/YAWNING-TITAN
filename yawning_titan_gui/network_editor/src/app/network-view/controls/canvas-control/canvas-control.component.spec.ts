import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CanvasControlComponent } from './canvas-control.component';

describe('CanvasControlComponent', () => {
  let component: CanvasControlComponent;
  let fixture: ComponentFixture<CanvasControlComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CanvasControlComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CanvasControlComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
