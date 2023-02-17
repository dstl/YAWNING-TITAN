import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NodeColourKeyItemComponent } from './node-colour-key-item.component';

describe('NodeColourKeyItemComponent', () => {
  let component: NodeColourKeyItemComponent;
  let fixture: ComponentFixture<NodeColourKeyItemComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NodeColourKeyItemComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NodeColourKeyItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
