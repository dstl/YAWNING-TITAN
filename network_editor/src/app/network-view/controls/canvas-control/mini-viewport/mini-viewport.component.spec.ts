import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MiniViewportComponent } from './mini-viewport.component';

describe('MiniViewportComponent', () => {
  let component: MiniViewportComponent;
  let fixture: ComponentFixture<MiniViewportComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MiniViewportComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MiniViewportComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
