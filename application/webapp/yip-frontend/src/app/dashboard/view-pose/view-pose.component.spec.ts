import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewPoseComponent } from './view-pose.component';

describe('ViewPoseComponent', () => {
  let component: ViewPoseComponent;
  let fixture: ComponentFixture<ViewPoseComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ViewPoseComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ViewPoseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
