import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FilterPosesComponent } from './filter-poses.component';

describe('FilterPosesComponent', () => {
  let component: FilterPosesComponent;
  let fixture: ComponentFixture<FilterPosesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FilterPosesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FilterPosesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
