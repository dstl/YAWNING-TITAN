import { NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CytoscapeService } from '../services/cytoscape/cytoscape.service';

import { NetworkViewComponent } from './network-view.component';

describe('NetworkViewComponent', () => {
  let component: NetworkViewComponent;
  let fixture: ComponentFixture<NetworkViewComponent>;

  let cytoscapeServiceStub: any = {

  }

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [NetworkViewComponent],
      providers: [
        { provide: CytoscapeService, cytoscapeServiceStub }
      ],
      schemas: [
        NO_ERRORS_SCHEMA
      ]
    })
      .compileComponents();

    fixture = TestBed.createComponent(NetworkViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call the import service when a load file event is triggered', () => {
    const spy = spyOn(component['importService'], 'loadFile');

    component.loadFile({});
    expect(spy).toHaveBeenCalled();
  });
});
