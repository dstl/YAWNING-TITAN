import { ComponentFixture, fakeAsync, TestBed, tick } from '@angular/core/testing';
import { NO_ERRORS_SCHEMA } from '@angular/core';
import { CytoscapeService } from '../../services/cytoscape/cytoscape.service';

import { ControlsComponent } from './controls.component';
import { HttpClient } from '@angular/common/http';
import { of } from 'rxjs';
import { DJANGO_SAVE_URL } from '../../../app/app.tokens';
import { Network } from '../../../app/network-class/network';
import { test_network } from '../../../testing/test-network';

describe('ControlsComponent', () => {
  let component: ControlsComponent;
  let fixture: ComponentFixture<ControlsComponent>;

  let cytoscapeServiceStub: any = {
    getNetworkJson: () => test_network,
    resetView: () => { }
  }

  const stubHttp = {
    post: () => of()
  };

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ControlsComponent],
      providers: [
        { provide: CytoscapeService, useValue: cytoscapeServiceStub },
        { provide: HttpClient, useValue: stubHttp },
        { provide: DJANGO_SAVE_URL, useValue: 'http://localhost' }
      ],
      schemas: [
        NO_ERRORS_SCHEMA
      ]
    })
      .compileComponents();

    fixture = TestBed.createComponent(ControlsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should reset the cytoscape view', () => {
    const spy = spyOn(component['cytoscapeService'], 'resetView');

    component.resetView();
    expect(spy).toHaveBeenCalled();
  });

  describe('METHOD: saveNetwork', () => {
    it('should send a post request including the network json in the body', fakeAsync(() => {
      const spy = spyOn(component['http'], 'post').and.returnValue(of());

      component.saveNetwork();
      tick();
      expect(spy).toHaveBeenCalledWith('http://localhost', test_network);
    }));
  });
});
