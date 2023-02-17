import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NodeColourKeyComponent } from './node-colour-key.component';

describe('NodeColourKeyComponent', () => {
  let component: NodeColourKeyComponent;
  let fixture: ComponentFixture<NodeColourKeyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NodeColourKeyComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NodeColourKeyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
