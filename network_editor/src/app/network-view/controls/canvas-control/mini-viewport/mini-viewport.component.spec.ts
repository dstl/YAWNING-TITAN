import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MiniViewportComponent } from './mini-viewport.component';
import { Subject } from 'rxjs';
import { CytoscapeService } from 'src/app/services/cytoscape/cytoscape.service';
import { MiniViewportService } from './service/mini-viewport.service';

describe('MiniViewportComponent', () => {
  let component: MiniViewportComponent;
  let fixture: ComponentFixture<MiniViewportComponent>;

  const cytoscapeServiceStub: any = {
    cytoscapeInstance: new Subject()
  }

  const viewportServiceStub: any = {
    init: () => { }
  }

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [MiniViewportComponent],
      providers: [
        { provide: CytoscapeService, useValue: cytoscapeServiceStub },
        { provide: MiniViewportService, useValue: viewportServiceStub },
      ]
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
