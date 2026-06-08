import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SearchByPoseComponent } from './search-by-pose.component';

describe('SearchByPoseComponent', () => {
  let component: SearchByPoseComponent;
  let fixture: ComponentFixture<SearchByPoseComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SearchByPoseComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SearchByPoseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
