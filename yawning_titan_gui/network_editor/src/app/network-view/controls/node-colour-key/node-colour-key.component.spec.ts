import { NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { NODE_KEY_CONFIG } from 'src/app/app.tokens';

import { NodeColourKeyComponent } from './node-colour-key.component';

describe('NodeColourKeyComponent', () => {
  let component: NodeColourKeyComponent;
  let fixture: ComponentFixture<NodeColourKeyComponent>;

  const stubConfig = {}

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [NodeColourKeyComponent],
      providers: [
        { provide: NODE_KEY_CONFIG, useValue: stubConfig }
      ],
      schemas: [
        NO_ERRORS_SCHEMA
      ]
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
