import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GraphAutoLayoutComponent } from './graph-auto-layout.component';

describe('GraphAutoLayoutComponent', () => {
  let component: GraphAutoLayoutComponent;
  let fixture: ComponentFixture<GraphAutoLayoutComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GraphAutoLayoutComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GraphAutoLayoutComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
