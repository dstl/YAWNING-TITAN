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

  describe('METHOD: setNodeStyle', () => {
    it('should set the element styles', () => {
      let element = document.createElement('div');

      const styles = {
        'border-color': '#fff',
        'background-color': '#000',
        'background-image': 'test'
      }

      component['setNodeStyle'](element, styles);

      expect(element.style.borderColor).toBe('rgb(255, 255, 255)');
      expect(element.style.backgroundColor).toBe('rgb(0, 0, 0)');
      expect(element.style.backgroundPosition ).toBe('center center');
    });
  });
});
