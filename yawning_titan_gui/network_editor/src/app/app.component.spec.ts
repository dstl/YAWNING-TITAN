import { NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { NODE_KEY_CONFIG } from 'src/app/app.tokens';
import { AppComponent } from './app.component';

import { CytoscapeService } from './services/cytoscape/cytoscape.service';
import { ImportService } from './services/export-import/import.service';
import { InteractionService } from './services/interaction/interaction.service';

describe('AppComponent', () => {
  let component: AppComponent;
  let fixture: ComponentFixture<AppComponent>;

  const stubCytoscapeService = {
    selectedElementEvent: of()
  }
  const stubIteractionService = {
    keyInput: () => { }
  }

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AppComponent],
      providers: [
        { provide: CytoscapeService, useValue: stubCytoscapeService },
        { provide: InteractionService, useValue: stubIteractionService }
      ],
      schemas: [
        NO_ERRORS_SCHEMA
      ]
    })
      .compileComponents();

    fixture = TestBed.createComponent(AppComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
